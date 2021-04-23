var action = $('#action').val();
$(document).ready(function () {
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_cedula').attr('readonly', 'true');
    }

    validador();
    $("#form").validate({
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
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos tres letras",
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
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos tres letras",
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


    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este cliente?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                        window.location.href = '/persona/cliente/lista'
                    });
                });
        }
    });


});



