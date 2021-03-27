var calendar;
var action_submit = 'add', id = '';
var disabledtimes_mapping = [];
var citas = {
    items: {
        fecha_reserva: '',
        cliente: '',
        duracion: '',
        hora_inicio: '',
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
    $('#id_user').chosen({no_results_text: "No se encontraron resultados para: "});
    $('#id_empleado')
        .on('change', function () {
            if ($(this).val() !== '' || null) {
                set_horas('search_horario_empleado', $(this).val(), '');
            }
        })
        .chosen({no_results_text: "No se encontraron resultados para: "});

    $('#id_servicio')
        .on('change', function () {
            if ($(this).val() !== '' || null) {
                $('#id_empleado').prop('disabled', false).trigger("chosen:updated");
                $.ajax({
                    dataType: 'JSON',
                    type: 'POST',
                    url: window.location.pathname,
                    data: {'action': 'search_servicio_cita', 'id': $(this).val()},
                }).done(function (data) {
                    if (!data.hasOwnProperty('error')) {
                        $.each(data, function (index, value) {
                            $('#duracion_res').fadeIn();
                            $('#id_duracion_serv').val(value.duracion);
                        });
                        return false;
                    }
                    menssaje_error('Error!', data.error, 'far fa-times-circle');
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                })
            } else {
                $('#duracion_res').fadeOut();
                $('#id_duracion_serv').val();
                $('#id_empleado').prop('disabled', 'disabled').trigger("chosen:updated");
                $("#id_fecha_reserva").datetimepicker('remove');
                $('#fecha_res').fadeOut()
            }
        })
        .chosen({no_results_text: "No se encontraron resultados para: "});

    $('#form').on('submit', function (e) {
        e.preventDefault();
        var isvalid = $(this).valid();
        if (isvalid) {
            var dur = $('#id_duracion_serv').val();
            var date = $("#id_fecha_reserva").data("datetimepicker").getDate(),
                formatted = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
                hours = date.getHours();
            var fin = dur / 60;

            var parametros;
            citas.items.fecha_reserva = formatted;
            citas.items.hora_inicio = hours;
            citas.items.hora_fin = hours + fin;
            citas.items.servicio = $('#id_servicio').val();
            citas.items.cliente = $('#id_user').val();
            citas.items.empleado = $('#id_empleado').val();
            citas.items.duracion = dur;
            parametros = {'cita': JSON.stringify(citas.items), 'id': id};
            parametros['action'] = action_submit;
            save_with_ajax('Alerta!', window.location.pathname, 'Esta seguro que desea guardar esta cita?',
                parametros, function () {
                    window.location.reload();
                })
        }
    });

    validador();
    $("#form").validate({
        rules: {
            user: {
                required: true,
            },
            empleado: {
                required: true,
            },
            fecha_reserva: {
                required: true,
            },
            servicio: {
                required: true,
            }
        },
        messages: {
            user: {
                required: "Elije un cliente"
            },
            servicio: {
                required: "Elije un servicio"
            },
            empleado: {
                required: "Elije un empleado"
            },
            fecha_reserva: {
                required: "Elije una fecha y hora para la cita"
            },
        }
    });

    $('#cancel_cita').on('click', function (e) {
        e.preventDefault();
        var parametros = {'action': 'anular', 'id': id};
        save_estado('Anular cita', window.location.pathname, 'Esta seguro que desea anular esta cita?', parametros, function () {
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
                    var dataHoje = new Date();
                    // if (event.start < dataHoje && event.end > dataHoje) {
                    //     //event.color = "#FFB347"; //Em andamento
                    //     element.css('background-color', '#FFB347');
                    // } else if (event.start < dataHoje && event.end < dataHoje) {
                    //     //event.color = "#77DD77"; //Concluído OK
                    //     element.css('background-color', '#77DD77');
                    // } else if (event.start > dataHoje && event.end > dataHoje) {
                    //     //event.color = "#AEC6CF"; //Não iniciado
                    //     element.css('background-color', '#AEC6CF');
                    // }
                },
                eventClick: function (info) {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: window.location.pathname,
                        data: {'action': 'edit_event', 'id': info.event.id},
                    }).done(function (data) {
                            var today = new Date(), string, hora_inicio,
                                hora_hoy = today.getHours() + ':' + today.getMinutes();
                            if (!data.hasOwnProperty('error')) {
                                if (today.getMonth() + 1 < 10) {
                                    string = today.getFullYear() + '-' + '0' + (today.getMonth() + 1) + '-' + today.getDate();
                                } else {
                                    string = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
                                }
                                var val_fecha = data[0].venta.fecha_reserva >= string;
                                if (val_fecha) {
                                    if (data[0].venta.fecha_reserva === string) {
                                        if (parseInt(data[0].venta.hora_inicio) + ':00' >= hora_hoy) {
                                            printpdf('Atencion!', 'Esta seguro que desea editar esta cita?', function () {
                                                set_data(data[0], hora_inicio);
                                            }, function () {
                                            });
                                        } else {
                                            menssaje_error('Alerta!', 'Solo puede editar citas que aun esten vigentes', '', function () {
                                            })
                                        }
                                    } else {
                                        printpdf('Atencion!', 'Esta seguro que desea editar esta cita?', function () {
                                            set_data(data[0], hora_inicio);
                                        }, function () {
                                        });
                                    }

                                } else {
                                    menssaje_error('Alerta!', 'Solo puede editar citas que aun esten vigentes', '', function () {
                                    })
                                }
                                return false;
                            }
                            menssaje_error('Error!', data.error, 'far fa-times-circle');
                        }
                    ).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                }
            });
            calendar.render();
            $.each(data, function (key, value) {
                var hora_inicio;
                var hora_fin;
                if (parseInt(value.venta.hora_inicio) < 10) {
                    hora_inicio = '0' + parseInt(value.venta.hora_inicio)
                } else {
                    hora_inicio = parseInt(value.venta.hora_inicio)
                }
                if (parseInt(value.venta.hora_fin) < 10) {
                    hora_fin = '0' + parseInt(value.venta.hora_fin)
                } else {
                    hora_fin = parseInt(value.venta.hora_fin)
                }
                var date = new Date(value.venta.fecha_reserva + 'T' + hora_inicio + ':00:00');
                var date_end = new Date(value.venta.fecha_reserva + 'T' + hora_fin + ':00:00');
                calendar.addEvent({
                    id: value.venta.id,
                    title: value.venta.user.full_name,
                    start: date,
                    className: value.classname,
                    // end: date_end,
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

function set_horas(action, id, exclude) {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'action': action, 'id': id, 'exclude': exclude},
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var dur = $('#id_duracion_serv').val();
            $.each(data, function (index, value) {
                if (dur > 60) {
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_inicio));
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_fin - 1));
                    for (var i = 1; i < (dur / 60); i++) {
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_inicio - i));
                    }
                } else {
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_inicio));
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + parseInt(value.venta.hora_fin - 1));
                }
            });
            $('#fecha_res').fadeIn();
            $("#id_fecha_reserva").datetimepicker({
                format: 'yyyy-mm-dd hh:ii',
                autoclose: true,
                language: 'es',
                daysOfWeekDisabled: [0],
                hoursDisabled: ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
                    '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00'],
                startDate: new Date(),
                showMinute: false,
                minutesDisabled: ["05", "10", "15", "20", "20", "25", "30", "35", "40", "45", "50", "55",],
                onRenderHour: function (date) {
                    if (disabledtimes_mapping.indexOf(formatDate(date) + ":" + date.getUTCHours()) > -1) {
                        return ['disabled'];
                    }
                }
            });
            return false;
        }
        menssaje_error('Error!', data.error, 'far fa-times-circle');
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    })
}

function set_data(data, hora_inicio) {
    $.isLoading({
        text: "<strong>" + 'Cargando..' + "</strong>",
        tpl: '<span class="isloading-wrapper %wrapper%"><i class="fa fa-refresh fa-2x fa-spin"></i><br>%text%</span>',
    });
    setTimeout(function () {
        $.isLoading('hide');
        action_submit = 'edit';
        id = data.id;
        $('#new_cita').fadeIn();
        $('#cancel_cita').fadeIn();
        $('#id_user').val(data.venta.user.id).trigger("chosen:updated");
        $('#id_servicio').val(data.servicio.id).trigger("chosen:updated");
        $('#duracion_res').fadeIn();
        $('#id_duracion_serv').val(data.servicio.duracion);
        $('#id_empleado').val(data.empleado.id).prop('disabled', false).trigger("chosen:updated");
        set_horas('search_horario_empleado_edit', data.empleado.id, data.venta.id);
        if (parseInt(data.venta.hora_inicio) < 10) {
            hora_inicio = '0' + parseInt(data.venta.hora_inicio)
        } else {
            hora_inicio = parseInt(data.venta.hora_inicio)
        }
        var date = new Date(data.venta.fecha_reserva + 'T' + hora_inicio + ':00:00');
        setTimeout(function () {
            $("#id_fecha_reserva").data("datetimepicker").setDate(date);
        }, 800);
    }, 2000);


}
