var user_tipo = $('input[name="user_tipo"]').val();
$(document).ready(function () {
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_cedula').attr('readonly', 'true');

    }

    validador();

    $("#form").validate({
        rules: {
            username: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
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
            avatar: {
                required: false
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
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },
            password: {
                required: true,
                minlength: 5
            },


        },
        messages: {
            username: {
                required: "Por favor ingresa un nombre de usuario",
                minlength: "Debe ingresar al menos tres letras"
            },
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
                // validar: 'Cedula no valida para Ecuador'
            },
            email: "Debe ingresar un correo valido",
            password: {
                required: "Debe Ingresar una contraseña",
                minlength: "Tu contraseña debe tener al menos 5 digitos"
            },
            telefono: {
                required: "Por favor ingresa tu numero convencional",
                minlength: "Tu numero de documento debe tener al menos 9 digitos",
                maxlength: "Tu numero de documento debe tener al menos 9 digitos",
                digits: "Debe ingresar unicamente numeros",
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


    $('#id_first_name').keypress(function (e) {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });
    $('#id_last_name').keypress(function (e) {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });
    $('#id_cedula').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Solo numeros").show().fadeOut("slow");
            return false;
        }
    });//Para solo numeros
    $('#id_telefono').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Solo numeros").show().fadeOut("slow");
            return false;
        }
    });//Para solo numeros
    $('#id_celular').keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Solo numeros").show().fadeOut("slow");
            return false;
        }
    });//Para solo numeros
    $('#id_direccion').keypress(function (e) {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });  //Para solo letras
    if (user_tipo === '0') {
        $('#id_groups').select2({
            theme: 'classic',
        }).prop('disabled', true);
    } else {
        $('#id_groups').select2({
            theme: 'classic',
            language: {
                inputTooShort: function () {
                    return "Ingresa al menos un caracter...";
                },
                "noResults": function () {
                    return "Sin resultados";
                },
                "searching": function () {
                    return "Buscando...";
                }
            },
            placeholder: 'Buscar...',
        });
    }


        //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este usuario?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este usuario!', 'far fa-smile-wink', function () {
                        window.location.href = '/persona/usuario/lista'
                    });
                });
        }
    });
});
