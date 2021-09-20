var calendar;
var action_submit = 'add', id = '', duration_edit, user_tipo = $('#user_tipo').val(), search_citas;
var disabledtimes_mapping = [];
var citas = {
    items: {
        fecha_reserva: '',
        cliente: '',
        duracion: '',
        hora_inicio: '',
        minuto_inicio: '',
        hora_fin: '',
        minuto_fin: '',
        empleado: '',
        servicio: [],

    }
};


var ventas = {
    items: {
        fecha: '',
        venta: '',
        cliente: '',
        duracion: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        detalle: []
    },
    add: function (data, empleado) {
        var array;
        array = {
            'nombre': data.nombre,
            'tipo': 'Servicio',
            'duracion': (data.duracion) / 60,
            'categoria': data.categoria.nombre,
            'presentacion': 'N/A',
            'stock': 'N/A',
            'cantidad': 1,
            'precio': data.precio,
            'subtotal': 1,
            'id': data.id,
            'empleado': empleado
        };
        this.items.detalle.push(array);
        this.list();
    },
    list: function () {
        localStorage.setItem('cita', JSON.stringify(ventas.items));
    },

};


$(function () {
    if (user_tipo === '0') {
        search_citas = 'search_citas_cliente';
        $('#id_user').val($('#user').val()).prop('disabled', true).trigger("chosen:updated");
    } else {
        search_citas = 'search_citas'
    }
    $('#new').on('click', function () {
        mostrar();
    });
    $('#cancel_new').on('click', function () {
        ocultar();
    });

    $('#id_new_cli').on('click', function () {
        $('#modal_person').modal('show');
    });

    cargar_eventos();
    $('#id_empleado')
        .on('change', function () {
            if ($(this).val() !== '' || null) {
                set_horas('search_horario_empleado', $(this).val(), '');
            }
        });

    $('#id_servicio')
        .on('change', function () {
            if ($(this).val() !== null) {
                $('#id_empleado').prop('disabled', false).trigger("chosen:updated");
                $.ajax({
                    dataType: 'JSON',
                    type: 'POST',
                    url: window.location.pathname,
                    data: {'action': 'search_servicio_cita', 'ids': JSON.stringify($(this).chosen('option:selected').val())},
                }).done(function (data) {
                    if (!data.hasOwnProperty('error')) {
                        $.each(data, function (index, value) {
                            $('#duracion_res').fadeIn();
                            $('#id_duracion_serv').val(value);
                            if (value>8){
                                menssaje_error('Error','Los servicios que elegiste superan nuestro horario laboral' );
                                $('#id_empleado').prop('disabled', true).trigger("chosen:updated");
                            }
                            if ($('#id_empleado').val() !== '' || null) {
                                if ($('#id_duracion_serv').val() > duration_edit) {
                                    set_horas('search_horario_empleado', $('#id_empleado').val(), '');
                                    $('#id_fecha_reserva').val(null);
                                } else {
                                    set_horas('search_horario_empleado', $('#id_empleado').val(), id);
                                }
                            }
                        });
                        return false;
                    }
                    menssaje_error('Error!', data.error, 'far fa-times-circle');
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                })
            } else {
                $('#duracion_res').fadeOut();
                $('#id_duracion_serv').val(0);
                $('#id_empleado').prop('disabled', true).trigger("chosen:updated");
                $("#id_fecha_reserva").datetimepicker('remove');
                $('#fecha_res').fadeOut()
            }
        });

    $('#form_cita').on('submit', function (e) {
        e.preventDefault();
        let labor_hour = new Date();
        let dta = $("#id_fecha_reserva").data("datetimepicker").getDate();
        labor_hour.setHours(18, 0, 0);
        labor_hour.setUTCFullYear(parseInt(dta.getFullYear()), parseInt(dta.getMonth()), parseInt(dta.getDate()));
        dta.setHours(dta.getHours()+parseInt($('#id_duracion_serv').val()), 0, 0);
        if (parseInt($('#id_duracion_serv').val()) > 8 || dta > labor_hour){
             menssaje_error('ERROR', 'Los servicios que elegiste superan nuestro horario laboral')
        } else if ($('#id_user').val() === '') {
            menssaje_error('Error!', 'Por favor elija un cliente', '', function () {
            })
        } else if ($('#id_servicio').val() === null) {
            menssaje_error('Error!', 'Por favor elija un servicio', '', function () {
            })
        } else if ($('#id_empleado').val() === '') {
            menssaje_error('Error!', 'Por favor elija un empleado', '', function () {
            })
        } else if ($('#fecha_res').show() && $('#id_fecha_reserva').val() === '') {
            menssaje_error('Error!', 'Por favor elija una fecha', '', function () {
            })
        } else {
            var dur = parseInt($('#id_duracion_serv').val());
            var date = $("#id_fecha_reserva").data("datetimepicker").getDate(),
                formatted = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
                hours = date.getHours(), minutes = date.getMinutes();
            var fin = dur;

            var parametros;
            citas.items.servicio = [];
            citas.items.fecha_reserva = formatted;
            citas.items.hora_inicio = hours;
            citas.items.minuto_inicio = minutes;
            citas.items.hora_fin = hours + fin;
            citas.items.minuto_fin = minutes;
            citas.items.servicio.push($('#id_servicio').chosen('option:selected').val());
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

    $('#cancel_cita').on('click', function (e) {
        e.preventDefault();
        var parametros = {'action': 'anular', 'id': id};
        save_estado('Anular cita', window.location.pathname, 'Esta seguro que desea anular esta cita?', parametros, function () {
            window.location.reload();
        })
    });


    $('#form_person').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'save_user');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este cliente?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                        $('#modal_person').modal('hide');
                        $('#id_user')
                            .append("<option value='" + response['id'] + "' selected='selected'>" + response['full_name'] + "</option>")
                            .trigger("chosen:updated");
                    });
                });
        }
    });
    $('#modal_person')
        .on('hidden.bs.modal', function (e) {
            e.preventDefault();
            reset('#form_person');
            $('#form_person').trigger("reset");
        });
    validador();
    $("#form_person").validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            last_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            cedula: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true,
                validar: true
            },
            email: {
                required: true,
                email: true
            },
            telefono: {
                required: false,
                minlength: 9,
                maxlength: 9,
                digits: true
            },
            celular: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            first_name: {
                required: "Por favor ingresa tus nombres",
                minlength: "Debe ingresar al menos tres letras",
                maxlength: "Debe ingresar maximo 50 caracteres",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos tres letras",
                maxlength: "Debe ingresar maximo 50 caracteres",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Por favor ingresa tu numero de cedula",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
                validar: "Numero de cedula no valido para Ecuador"
            },
            email: "Debe ingresar un correo valido",
            telefono: {
                minlength: "Tu numero de telefono 9 digitos",
                maxlength: "Tu numero de tener no mas 9 digitos",
                digits: "Debe ingresar unicamente numeros",
            },
            celular: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de celular debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de celular debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Por favor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_first_name').keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    }).keyup(function (e) {
        var changue = titleCase($(this).val());
        $(this).val(changue);
    });
    $('#id_last_name').keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    }).keyup(function (e) {
        var changue = titleCase($(this).val());
        $(this).val(changue);
    });
    $('#id_cedula').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros
    $('#id_telefono').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros
    $('#id_celular').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros

});

function cargar_eventos() {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'action': search_citas},
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var calendarEl = document.getElementById('calendar');
            calendar = new FullCalendar.Calendar(calendarEl, {
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
                        placement: "auto left",
                        html:true,
                        trigger: 'hover',
                        container: 'body',
                        content: info.event.extendedProps.description,
                        template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
                    });
                },
                eventClick: function (info) {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: window.location.pathname,
                        data: {'action': 'edit_event', 'id': info.event.id},
                    })
                        .done(function (data) {
                                var today = new Date(), string, hora_inicio;
                                var mes, dia;
                                hora_hoy = today.getHours() + ':' + today.getMinutes();
                                if (!data.hasOwnProperty('error')) {
                                    if (today.getMonth() + 1 < 10) {
                                        mes = '0' + (today.getMonth() + 1);
                                    } else {
                                        mes = (today.getMonth() + 1);
                                    }
                                    if (today.getDate() + 1 < 10) {
                                        dia = '0' + (today.getDate());
                                    } else {
                                        dia = today.getDate();
                                    }
                                    string = string = today.getFullYear() + '-' + mes + '-' + dia;
                                    var val_fecha = data[0].venta.fecha_reserva >= string;
                                    if (val_fecha) {
                                        if (data[0].venta.fecha_reserva === string) {
                                            if (data[0].venta.hora_inicio + ':00' >= hora_hoy) {
                                                preguntar('Atencion!', 'Que desea hacer con este cita?', function () {
                                                    set_data(data[0], hora_inicio);
                                                }, function () {
                                                    localStorage.clear();
                                                    ventas.items.cliente = data[0].venta.user.id;
                                                    ventas.items.venta = data[0].venta.id;
                                                    ventas.add(data[0].servicio, data[0].empleado);
                                                    window.location.href = '/transaccion/venta/nuevo'
                                                });
                                            } else {
                                                menssaje_error('Alerta!', 'Solo puede editar citas que aun esten vigentes', '', function () {
                                                })
                                            }
                                        } else {
                                            preguntar2('Atencion!', 'Esta seguro que desea editar esta cita?', function () {
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
                value.venta.minuto_inicio = value.venta.minuto_inicio > 9 ? value.venta.minuto_inicio : "0" + value.venta.minuto_inicio;
                value.venta.minuto_fin = value.venta.minuto_fin > 9 ? value.venta.minuto_fin : "0" + value.venta.minuto_fin;
                value.venta.hora_inicio = value.venta.hora_inicio > 9 ? value.venta.hora_inicio : "0" + value.venta.hora_inicio;
                value.venta.hora_fin = value.venta.hora_fin > 9 ? value.venta.hora_fin : "0" + value.venta.hora_fin;
                var date = new Date(value.venta.fecha_reserva + 'T' + value.venta.hora_inicio + ':' + value.venta.minuto_inicio + ':00');
                var date_end = new Date(value.venta.fecha_reserva + 'T' + value.venta.hora_fin + ':' + value.venta.minuto_fin + ':00');
                var clase = value.classname, cncel = '', color = 'green';
                if (value.venta.citacancelada === true) {
                    clase = 'label-danger';
                    cncel = 'NO REALIZADA ';
                    color = 'red'
                }
                let descr= '<b>'+cncel+'</b> Cita con: '+ value.empleado.full_name_list+ ' desde '+ parseInt(value.venta.hora_inicio) + ':' + value.venta.minuto_inicio + ' hasta las ' +
                    parseInt(value.venta.hora_fin) + ':' + value.venta.minuto_fin+ ' los servicios de:  <br>';
                $.each(value.servicios, function (key, value) {
                    let ch = '<b>'+value.servicio.nombre+'</b><br>';
                    descr += ch;
                });
                calendar.addEvent({
                    id: value.venta.id,
                    title: value.venta.user.full_name,
                    start: date,
                    className: clase,
                    end: date_end,
                    color: color,
                    allDay: false,
                    description: descr,
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
    disabledtimes_mapping = [];
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'action': action, 'id': id, 'exclude': exclude},
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            var dur = $('#id_duracion_serv').val();
            $.each(data, function (index, value) {
                var alter_hora, ch;
                if (value.venta.hora_inicio + 1 <= value.venta.hora_fin) {
                    alter_hora = value.venta.hora_fin - 1;
                }
                alter_hora = alter_hora > 9 ? alter_hora : "0" + alter_hora;
                value.venta.hora_inicio = value.venta.hora_inicio > 9 ? value.venta.hora_inicio : "0" + value.venta.hora_inicio;
                if (dur > 1) {
                    ch = value.venta.hora_fin - 1;
                    ch = ch > 9 ? ch : "0" + ch;
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + value.venta.hora_inicio);
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + ch);
                    for (var i = 1; i < dur; i++) {
                        ch = value.venta.hora_inicio - i;
                        ch = ch > 9 ? ch : "0" + ch;
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + ch);
                    }
                    for (var a = 1; a < value.servicio.duracion; a++) {
                        ch = value.venta.hora_fin - a;
                        ch = ch > 9 ? ch : "0" + ch;
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + ch);
                    }
                } else {
                    // console.log(value.fecha_reserva + ':' + value.venta.hora_inicio);
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + value.venta.hora_inicio);
                    disabledtimes_mapping.push(value.fecha_reserva + ':' + alter_hora);
                    for (var b = 1; b < value.servicio.duracion; b++) {
                        ch = value.venta.hora_fin - b;
                        ch = ch > 9 ? ch : "0" + ch;
                        disabledtimes_mapping.push(value.fecha_reserva + ':' + ch);
                    }
                }
            });
            $('#fecha_res').fadeIn();
            $("#id_fecha_reserva").datetimepicker({
                format: 'yyyy-mm-dd hh:00',
                autoclose: true,
                language: 'es',
                today: true,
                daysOfWeekDisabled: [0],
                hoursDisabled: ['18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4', '5', '6', '7'],
                startDate: new Date(),
                showMinute: false,
                datesDisabled: ['2021-11-15 19:00'],
                minutesDisabled: ["05", "10", "15", "20", "20", "25", "30", "35", "40", "45", "50", "55"],
                onRenderHour: function (date) {
                    var hora = date.getUTCHours() > 9 ? date.getUTCHours() : "0" + date.getUTCHours();
                    if (disabledtimes_mapping.indexOf(formatDate(date) + ":" + hora) > -1) {
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
        mostrar();
        $('#cancel_new').fadeOut();
        $.isLoading('hide');
        action_submit = 'edit';
        id = data.id;
        $('#new_cita').fadeIn();
        $('#cancel_cita').fadeIn();
        $('#id_user').val(data.venta.user.id).trigger("chosen:updated");
        $('#id_servicio').val(data.servicio.id).trigger("chosen:updated");
        $('#duracion_res').fadeIn();
        $('#cancel_edit').fadeIn();
        $('#id_duracion_serv').val(data.servicio.duracion);
        duration_edit = data.servicio.duracion;
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

function formatDate(datestr) {
    var date = new Date(datestr);
    var day = date.getDate();
    day = day > 9 ? day : "0" + day;
    var month = date.getMonth() + 1;
    month = month > 9 ? month : "0" + month;
    return month + "/" + day + "/" + date.getFullYear();
}

function mostrar() {
    $('#agenda_calendar').removeClass('col-lg-12').addClass('col-lg-9');
    calendar.destroy();
    cargar_eventos();
    $('#new').fadeOut();
    $('#formulario_cita').fadeIn();
    $('#id_empleado').chosen({no_results_text: "No se encontraron resultados para: "});
    $('#id_servicio').chosen({
        no_results_text: "No se encontraron resultados para: ",
        placeholder_text_multiple: "Selecciona uno o mas servicios.....",
    });
    $('#id_user').chosen({no_results_text: "No se encontraron resultados para: "});

}

function ocultar() {
    calendar.destroy();
    cargar_eventos();
    $('#new').fadeIn();
    $('#agenda_calendar').removeClass('col-lg-9').addClass('col-lg-12');
    $('#formulario_cita').fadeOut();
    $('#id_empleado').chosen('destroy');
    $('#id_servicio').chosen('destroy');
    $('#id_user').chosen('destroy');

}


