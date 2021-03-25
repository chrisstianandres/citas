var calendar;
$(function () {

    /* initialize the external events
        -----------------------------------------------------------------*/

    // $('#external-events div.external-event').each(function() {
    //
    // 	// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
    // 	// it doesn't need to have a start or end
    // 	var eventObject = {
    // 		title: $.trim($(this).text()) // use the element's text as the event title
    // 	};
    //
    // 	// store the Event Object in the DOM element so we can get to it later
    // 	$(this).data('eventObject', eventObject);
    //
    // 	// make the event draggable using jQuery UI
    // 	$(this).draggable({
    // 		zIndex: 999,
    // 		revert: true,      // will cause the event to go back to its
    // 		revertDuration: 0  //  original position after the drag
    // 	});
    //
    // });


    /* initialize the calendar
    -----------------------------------------------------------------*/

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();


    // calendar = $('#calendar').fullCalendar(
    //     {
    //         //isRTL: true,
    //         //firstDay: 1,// >> change first day of week
    //
    //         buttonHtml: {
    //             prev: '<i class="ace-icon fa fa-chevron-left"></i>',
    //             next: '<i class="ace-icon fa fa-chevron-right"></i>'
    //         },
    //
    //         header: {
    //             left: 'prev,next today',
    //             center: 'title',
    //             right: 'month,agendaWeek,agendaDay'
    //         },
    //         events: [
    //             // {
    //             // title: 'All Day Event',
    //             // start: new Date(y, m, 1),
    //             // className: 'label-important'
    //             // },
    //             // {
    //             // title: 'Long Event',
    //             // start: moment().subtract(5, 'days').format('YYYY-MM-DD'),
    //             // end: moment().subtract(1, 'days').format('YYYY-MM-DD'),
    //             // className: 'label-success'
    //             // },
    //             // {
    //             // title: 'Some Event',
    //             // start: new Date(y, m, d-3, 16, 0),
    //             // allDay: false,
    //             // className: 'label-info'
    //             // }
    //         ]
    //         ,
    //
    //         /**eventResize: function(event, delta, revertFunc) {
    //
    // 		alert(event.title + " end is now " + event.end.format());
    //
    // 		if (!confirm("is this okay?")) {
    // 			revertFunc();
    // 		}
    //
    // 	},*/
    //
    //         // editable: true,
    //         // droppable: true, // this allows things to be dropped onto the calendar !!!
    //         // drop: function(date) { // this function is called when something is dropped
    //         //
    //         // 	// retrieve the dropped element's stored Event Object
    //         // 	var originalEventObject = $(this).data('eventObject');
    //         // 	var $extraEventClass = $(this).attr('data-class');
    //         //
    //         //
    //         // 	// we need to copy it, so that multiple events don't have a reference to the same object
    //         // 	var copiedEventObject = $.extend({}, originalEventObject);
    //         //
    //         // 	// assign it the date that was reported
    //         // 	copiedEventObject.start = date;
    //         // 	copiedEventObject.allDay = false;
    //         // 	if($extraEventClass) copiedEventObject['className'] = [$extraEventClass];
    //         //
    //         // 	// render the event on the calendar
    //         // 	// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
    //         // 	$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
    //         //
    //         // 	// is the "remove after drop" checkbox checked?
    //         // 	if ($('#drop-remove').is(':checked')) {
    //         // 		// if so, remove the element from the "Draggable Events" list
    //         // 		$(this).remove();
    //         // 	}
    //         //
    //         // }
    //         // ,
    //         // selectable: true,
    //         // selectHelper: true,
    //         // select: function(start, end, allDay) {
    //         //
    //         // 	bootbox.prompt("New Event Title:", function(title) {
    //         // 		if (title !== null) {
    //         // 			calendar.fullCalendar('renderEvent',
    //         // 				{
    //         // 					title: title,
    //         // 					start: start,
    //         // 					end: end,
    //         // 					allDay: allDay,
    //         // 					className: 'label-info'
    //         // 				},
    //         // 				true // make the event "stick"
    //         // 			);
    //         // 		}
    //         // 	});
    //         //
    //         //
    //         // 	calendar.fullCalendar('unselect');
    //         // }
    //         // ,
    //         // eventClick: function(calEvent, jsEvent, view) {
    //         //
    //         // 	//display a modal
    //         // 	var modal =
    //         // 	'<div class="modal fade">\
    //         // 	  <div class="modal-dialog">\
    //         // 	   <div class="modal-content">\
    //         // 		 <div class="modal-body">\
    //         // 		   <button type="button" class="close" data-dismiss="modal" style="margin-top:-10px;">&times;</button>\
    //         // 		   <form class="no-margin">\
    //         // 			  <label>Change event name &nbsp;</label>\
    //         // 			  <input class="middle" autocomplete="off" type="text" value="' + calEvent.title + '" />\
    //         // 			 <button type="submit" class="btn btn-sm btn-success"><i class="ace-icon fa fa-check"></i> Save</button>\
    //         // 		   </form>\
    //         // 		 </div>\
    //         // 		 <div class="modal-footer">\
    //         // 			<button type="button" class="btn btn-sm btn-danger" data-action="delete"><i class="ace-icon fa fa-trash-o"></i> Delete Event</button>\
    //         // 			<button type="button" class="btn btn-sm" data-dismiss="modal"><i class="ace-icon fa fa-times"></i> Cancel</button>\
    //         // 		 </div>\
    //         // 	  </div>\
    //         // 	 </div>\
    //         // 	</div>';
    //         //
    //         //
    //         // 	var modal = $(modal).appendTo('body');
    //         // 	modal.find('form').on('submit', function(ev){
    //         // 		ev.preventDefault();
    //         //
    //         // 		calEvent.title = $(this).find("input[type=text]").val();
    //         // 		calendar.fullCalendar('updateEvent', calEvent);
    //         // 		modal.modal("hide");
    //         // 	});
    //         // 	modal.find('button[data-action=delete]').on('click', function() {
    //         // 		calendar.fullCalendar('removeEvents' , function(ev){
    //         // 			return (ev._id === calEvent._id);
    //         // 		});
    //         // 		modal.modal("hide");
    //         // 	});
    //         //
    //         // 	modal.modal('show').on('hidden', function(){
    //         // 		modal.remove();
    //         // 	});
    //         //
    //         //
    //         // 	//console.log(calEvent.id);
    //         // 	//console.log(jsEvent);
    //         // 	//console.log(view);
    //         //
    //         // 	// change the border color just for fun
    //         // 	//$(this).css('border-color', 'red');
    //         //
    //         // }
    //
    //     }
    // );

    cargar_eventos();
});

function cargar_eventos() {
    var calendarEl = document.getElementById('calendar');

    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'action': 'search_citas'},
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                headerToolbar: {
                    center: 'addEventButton'
                },
                // customButtons: {
                //     addEventButton: {
                //         text: 'add event...',
                //         click: function () {
                //             var dateStr = prompt('Enter a date in YYYY-MM-DD format');
                //             var date = new Date(dateStr + 'T00:00:00'); // will be in local time
                //
                //             if (!isNaN(date.valueOf())) { // valid?
                //
                //                 alert('Great. Now, update your database...');
                //             } else {
                //                 alert('Invalid date.');
                //             }
                //         }
                //     }
                // }
                businessHours: {
                    // days of week. an array of zero-based day of week integers (0=Sunday)
                    daysOfWeek: [1, 2, 3, 4, 5, 6], // Monday - Thursday

                    startTime: '08:00', // a start time (10am in this example)
                    endTime: '18:00', // an end time (6pm in this example)
                },
                eventTimeFormat: { // like '14:30:00'
                    hour: '2-digit',
                    minute: '2-digit',
                    meridiem: false
                }
            });
            calendar.render();
            $.each(data, function (key, value) {
                console.log(value);
                var titulo = value.venta.user.full_name;
                var date = new Date(value.venta.fecha_reserva + 'T20:' + value.servicio.duracion + ':00');
                calendar.addEvent({
                    title: '',
                    start: date,
                    end: '2021-03-24T20:30:00',
                    allDay: false,
                    description: 'save the date! Join us for our Annual Membership Conference. Breakfast will be served beginning at 7:30 a.m. Featuring The EFEC Belief System & Our Pledge lunch',
                });
            });

            return false;
        }
        menssaje_error('Error!', data.error, 'far fa-times-circle');
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    })

}