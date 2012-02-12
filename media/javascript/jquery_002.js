(function($) {

	$.fn.imgNotes = function(n, mode) {
	
		if(undefined != n){
			notes = n;
		} 

		if(undefined == mode){
			mode = 'view'
		} 
		image = this;

		imgOffset = $(image).offset();
	
        for (note in notes){
            appendnote(note, notes[note], imgOffset, mode)
        }
		//$(notes).each(function(){
		//	appendnote(this);
		//});	
	
		$(image).hover(
			function(){
				$('.note').show();
			},
			function(){
				$('.note').hide();
			}
		);

		addnoteevents();
		
		$(window).resize(function () {
			$('.note').remove();

			imgOffset = $(image).offset();

			$(notes).each(function(){
				appendnote(this);
			});

			addnoteevents();

		});
	} 
	
	function addnoteevents() {
		$('.note').hover(
			function(){
				$('.note').show();
				$(this).next('.notep').show();
				$(this).next('.notep').css("z-index", 10000);
			},
			function(){
				$('.note').show();
				$(this).next('.notep').hide();
				$(this).next('.notep').css("z-index", 0);
			}
		);
	}


	function appendnote(noteId, noteData, imgOffset, mode){
		note_left  = parseInt(imgOffset.left) + parseInt(noteData.x1);
		note_top   = parseInt(imgOffset.top) + parseInt(noteData.y1);
		note_p_top = note_top + parseInt(noteData.height)+5;
						
        if (mode=='edit'){
		    note_area_div = $("<div class='note' id='"+noteId+"' ondblclick='javascript:showDeleteNote(this)'></div>").css({ left: note_left + 'px', top: note_top + 'px', width: noteData.width + 'px', height: noteData.height + 'px' });
        }
        else if(mode=='view'){
		    note_area_div = $("<div class='note' id='"+noteId+"' onclick='javascript:voteDaalo(this)'></div>").css({ left: note_left + 'px', top: note_top + 'px', width: noteData.width + 'px', height: noteData.height + 'px' });
        }
		
		note_text_div = $('<div class="notep" >'+noteData.note+'</div>').css({ left: note_left + 'px', top: note_p_top + 'px'});
	
		$('body').append(note_area_div);
		$('body').append(note_text_div);
	}

    function deleteNote(noteData){
    }

// End the closure
})(jQuery);
