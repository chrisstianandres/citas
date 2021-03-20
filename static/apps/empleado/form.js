$(document).ready(function () {
    var action = $('#action').val();
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_cedula').attr('readonly', 'true');
    }

    validador();

    $("#form").validate({
        rules: {
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            apellidos: {
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
                val_ced: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
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
            },


        },
        messages: {
            nombres: {
                required: "Por favor ingresa tus nombres",
                minlength: "Debe ingresar al menos un nombre",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            apellidos: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Por favor ingresa tu numero de cedula",
                minlength: "Tu numero de cedula debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de cedula debe tener maximo 10 digitos",
                val_ced: "Numero de cedula no valido para Ecuador",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Por favor ingresa tu numero de telefono",
                minlength: "Tu numero de telefono debe tener al menos 9 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de telefono debe tener maximo 9 digitos",
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
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            apellidos: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            cedula: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
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
            },


        },
        messages: {
            nombres: {
                required: "Por favor ingresa tus nombres",
                minlength: "Debe ingresar al menos un nombre",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            apellidos: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Por favor ingresa tu numero de documento",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Por favor ingresa tu numero de telefono",
                minlength: "Tu numero de documento debe tener al menos 9 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 9 digitos",
            },
            celular: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Por favor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_nombres').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });



    //enviar formulario
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este empleado?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este empleado!', 'far fa-smile-wink', function () {
                        window.location.href='/empleado/lista';
                    });
                });
        }
    });


});



