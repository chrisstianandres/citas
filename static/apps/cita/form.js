var calendar;
var disabledtimes_mapping = [];
var citas = {
    items: {
        fecha_reserva: '',
        cliente: '',
        duracion: '',
        hora_inicio:'',
        hora_fin: '',
        empleado: '',

    }
};

function formatDate(datestr) {
    var date = new Date(datestr);
    var day = date.getDate();
    day = day > 9 ? day : "0" + day;
    var month = date.getMonth() + 1;
    month = month > 9 ? month : "0" + month;
    return month + "/" + day + "/" + date.getFullYear();
}

$(function () {
    cargar_eventos();

    $('#id_empleado').on('change', function () {
        if ($(this).val() !== '' || null) {
            $.ajax({
                dataType: 'JSON',
                type: 'POST',
                url: window.location.pathname,
                data: {'action': 'search_horario_empleado', 'id': $(this).val()},
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    $.each(data, function (index, value) {
                        console.log(value);
                        //03/26/2021:13
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_inicio));
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_fin - 1));
                        console.log(disabledtimes_mapping);
                        $('#fecha_res').show();
                        $("#id_fecha_reserva").datetimepicker({
                            format: 'yyyy-mm-dd hh:ii',
                            autoclose: true,
                            language: 'es',
                            daysOfWeekDisabled: [6],
                            hoursDisabled: ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
                                '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',],
                            startDate: new Date(),
                            showMinute: false,
                            minutesDisabled: ["05", "10", "15", "20", "20", "25", "30", "35", "40", "45", "50", "55",],
                            onRenderHour: function (date) {
                                if (disabledtimes_mapping.indexOf(formatDate(date) + ":" + date.getUTCHours()) > -1) {
                                    console.log(true);
                                    return ['disabled'];
                                }
                            }
                        });

                    })
                }
                menssaje_error('Error!', data.error, 'far fa-times-circle');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            })
        }
    });


    $('#id_servicio').on('change', function () {
        if ($(this).val() !== '' || null) {
            $.ajax({
                dataType: 'JSON',
                type: 'POST',
                url: window.location.pathname,
                data: {'action': 'search_servicio_cita', 'id': $(this).val()},
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    $.each(data, function (index, value) {
                        console.log(value);
                        $('#duracion_res').show();
                        $('#id_duracion_serv').val(value.duracion);

                    })
                }
                menssaje_error('Error!', data.error, 'far fa-times-circle');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            })
        } else {
            $('#duracion_res').hide();
            $('#id_duracion_serv').val();
        }
    });

    $('#form').on('submit', function (e) {
        e.preventDefault();
        var dur = $('#id_duracion_serv').val();
        var date = $("#id_fecha_reserva").data("datetimepicker").getDate(),
            formatted = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
            hours = date.getHours();
        var fin = dur/60;

        var parametros;
        citas.items.fecha_reserva = formatted;
        citas.items.hora_inicio = hours;
        citas.items.hora_fin = hours+fin;
        citas.items.servicio = $('#id_servicio').val();
        citas.items.cliente = $('#id_user').val();
        citas.items.empleado = $('#id_empleado').val();
        citas.items.duracion = dur;
        parametros = {'cita': JSON.stringify(citas.items)};
        parametros['action'] = 'add';
        save_with_ajax('Alerta!', window.location.pathname, 'Esta seguro que desea guardar esta cita?',
            parametros, function () {
            window.location.reload();

            })


    })
});


function cargar_eventos() {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'action': 'search_citas'},
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var calendarEl = document.getElementById('calendar');

            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                locale: 'es',
                headerToolbar: {
                    start: 'prev,next today',
                    center: 'title',
                    end: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                buttonText: {
                    today: 'hoy',
                    month: 'mes',
                    week: 'semana',
                    day: 'dia',
                    list: 'lista'
                },
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
                },
                eventDidMount: function (info) {
                    $(info.el).popover({
                        title: 'Cliente: ' + info.event.title,
                        placement: "bottom",
                        trigger: "hover",
                        content: info.event.extendedProps.description
                    });
                },
            });

            calendar.render();
            $.each(data, function (key, value) {
                var date = new Date(value.venta.fecha_reserva + 'T' + parseInt(value.venta.hora_inicio) + ':00:00');
                var date_end = new Date(value.venta.fecha_reserva + 'T' + parseInt(value.venta.hora_fin) + ':00:00');
                calendar.addEvent({
                    title: value.venta.user.full_name,
                    start: date,
                    end: date_end,
                    allDay: false,
                    description: value.servicio.nombre + ' con ' + value.empleado.full_name_list + ' desde las: ' +
                        parseInt(value.venta.hora_inicio) + ':00' + ' hasta las ' + parseInt(value.venta.hora_fin) + ':00',
                });
            });

            return false;
        }
        menssaje_error('Error!', data.error, 'far fa-times-circle');
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    })

}
