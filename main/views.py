# Create your views here.
import time
import os
import random
try:
    import simplejson
except ImportError:
    from django.utils import simplejson as simplejson

from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.db.models import Count, F
from filetransfers.api import prepare_upload
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.ext import webapp

from main import models
from main import forms


# CONSTANTS
UPLOADED_IMAGES_LOC = os.path.join(settings.MEDIA_ROOT, 'user_images')
COORDINATE_NAMES = ['x1','y1','width','height']
ALREADY_VOTED_QUOTES = ["Damn..you've already voted", 
                        "You have voted already, Time to get a job now.",
                        "U NO VOTE FOR 1 more than 1",
                        "CANT VOTE. U MAD?"]


#### End Constants

def handle_uploaded_file(request):
    form = forms.UploadForm(request.POST, request.FILES)#{'image':f, 'question':'doo'})
    a = form.save()
    return a
    #file_name = '%s.jpeg'%time.time()
    #destination = open(os.path.join(UPLOADED_IMAGES_LOC, file_name), 'wb+')
    #for chunk in f.chunks():
    #    destination.write(chunk)
    #destination.close()
    #return file_name


def get_image_from_datastore(idx):
    photo = models.UserImage.objects.get(id=idx)
    return photo.image
   

def index(request):
    """first page. will show a nice UI and an imagefield."""
    # preparing the app engine specific crap.
    view_url = reverse('main.views.show_image')
    upload_url, upload_data = prepare_upload(request, view_url)
    form = forms.UploadForm()
    return render_to_response('index.html',
            {'form': form, 'upload_url': upload_url, 'upload_data': upload_data},
            context_instance=RequestContext(request))


@csrf_exempt
def show_image(request):
    """Second page, Will accept a post request and return a jsonresponse with
    the image data and and all the js."""
    formobj = handle_uploaded_file(request)#request.FILES.get('imageFile')
    #FIXME: this needs to be changed if not using app engine
    context = {'user_image_id': formobj.id, 'title': ''}
    return render_to_response('show_image.html', context,
            context_instance=RequestContext(request))


def serve_user_image(request, image_id):
    """ """
    image = get_image_from_datastore(image_id)
    if image:
        response = HttpResponse(image)
        response['Content-Type'] = 'image/jpeg'
        return response


#TODO: this is a ajax call so raise errors if any 
def submit_poll(request, image_id):
    """View for retrieving and storing image poll data in a db.
    will return a page showing the poll and an ability to let them share."""
    option_data = {}
    data = request.POST.copy()
    if not data:
        return HttpResponse("no options?")
    poll_question = data.get('question')
    if poll_question:
        del data['question']
    keys = set(i.split('[')[0].strip() for i in data.keys())
    for key in keys:
        coordinates = ','.join(data[key+'['+i+']'] for i in
                COORDINATE_NAMES)
        option_data[key] = [data[key+'[note]'], coordinates]
    #save the options
    user_image = models.UserImage.objects.get(id=image_id)
    user_image.question = poll_question
    user_image.save()
    for option in option_data.values():
        models.Options(poll_id=user_image, option_name=option[0],
                coordinates=option[1], users=[0,], votes=0).save()
    return HttpResponse('success')


def show_poll(request, poll_id=None):
    """show the complete poll here..with the ability to
    vote for results."""
    if poll_id:
        user_image = models.UserImage.objects.get(id=poll_id)
    else:
        
        user_images = models.UserImage.objects.values('id').all()
        user_image = models.UserImage.objects.get(
            id=user_images[random.randint(0, len(user_images))]['id'])
    options = models.Options.objects.filter(poll_id=user_image)
    user_options = {}
    for option in options:
        user_options[option.id] = dict(zip(COORDINATE_NAMES,
            option.coordinates.split(','))+
            [('note', option.option_name)])
    user_options = simplejson.dumps(user_options)
    return render_to_response('show_poll.html', dict(user_image=user_image,
        user_options=user_options), context_instance=RequestContext(request))


def vote(request, poll_id):
    option_id = request.POST.get('vote_option')
    response_dict = {}
    if request.method != 'POST' or not option_id:
        response_dict['error'] = 'o.O Hey Snooper..leave this site alone :)'
        return HttpResponse(simplejson.dumps(response_dict))
    # checks to do:
    #   1 user<=>1 vote
    #   if the option belong to the poll or not
    option = models.Options.objects.filter(id=option_id)
    poll = models.UserImage.objects.get(id=poll_id)
    user = request.user
    if not user.is_authenticated():
        user = request.META['REMOTE_ADDR']
    old_users = option[0].users
    if user in old_users:
        foo = dict(models.Options.objects.filter(poll_id=poll).values_list('option_name', 'votes'))
        response_dict['total_votes'] = foo
        response_dict['error'] = random.sample(ALREADY_VOTED_QUOTES, 1)[0]
        return HttpResponse(simplejson.dumps(response_dict))
    try:
        option.update(votes = F('votes')+1)
        old_users.append(user)
        option.update(users = old_users)
    except:
        response_dict['error'] = 'Bleh...shit happened'
        return HttpResponse(simplejson.dumps(response_dict))
    foo = dict(models.Options.objects.filter(poll_id=poll).values_list('option_name', 'votes'))
    response_dict['total_votes'] = foo
    response_dict['success'] = True
    return HttpResponse(simplejson.dumps(response_dict))


def poll_list(request):
    #TODO: comeup with an algorithm for sorting the results based on 
    # number of votes and created_date
    poll_list = UserImage.objects.all()
    return render_to_response('poll_list.html',dict(poll_list=poll_list),
            context_instance=RequestContext(request))


def poll_browse(request):
    """
    3 parts:
    if no param: show newest
    if key: show particular
    if random: show random
    """
    user_image = models.UserImage.objects.get(id=poll_id)
    options = models.Options.objects.filter(poll_id=user_image)
    user_options = {}
    for option in options:
        user_options[option.id] = dict(zip(COORDINATE_NAMES,
            option.coordinates.split(','))+
            [('note', option.option_name)])
    user_options = simplejson.dumps(user_options)
    return render_to_response('show_poll.html', dict(user_image=user_image,
        user_options=user_options), context_instance=RequestContext(request))
