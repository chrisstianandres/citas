$(document).ready(function () {

    validador();

    if ($('#id_num_doc').val() !== '' || null) {
        $('#id_num_doc').prop('readonly', true);
        $('#id_tipo').attr('disabled', true);
    }

    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 5,
                maxlength: 50,
                lettersonly: true,
            },
            tipo: {
                required: true
            },
            num_doc: {
                required: true,
                tipo: true,
                digits: true,
                val_ced: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                minlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },


        },
        messages: {
            nombre: {
                required: "Por favor ingresa tus nombres y apellidos",
                minlength: "Debe ingresar al menos un nombre y un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            num_doc: {
                required: "Por favor ingresa tu numero de documento",
                tipo: "Error en el numero de digitos (10 para cedula o 13 para ruc)",
                // minlength: "Numero de digitos deficiente (10 para cedula)",
                digits: "Debe ingresar unicamente numeros",
                val_ced: "Numero de documento no valido para Ecuador",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Porfavor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });
    $("#form_person").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 5,
                maxlength: 50,
                lettersonly: true,
            },
            tipo: {
                required: true
            },
            num_doc: {
                required: true,
                tipo: true,
                digits: true,
                val_ced: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
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
            nombre: {
                required: "Por favor ingresa tus nombres y apellidos",
                minlength: "Debe ingresar al menos un nombre y un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            num_doc: {
                required: "Por favor ingresa tu numero de documento",
                tipo: "Error en el numero de digitos (10 para cedula o 13 para ruc)",
                // minlength: "Numero de digitos deficiente (10 para cedula)",
                digits: "Debe ingresar unicamente numeros",
                val_ced: "Numero de documento no valido para Ecuador",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de celular debe tener 10 digitos",
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

    $('#id_nombres').keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        })
        .keyup(function (e) {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        });


    $('#id_apellidos')
        .keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        })
        .keyup(function (e) {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        });

    function titleCase(texto) {
        const re = /(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])(?:([a-záéíóúüñ])|([A-ZÁÉÍÓÚÜÑ]))|([A-ZÁÉÍÓÚÜÑ]+)/gu;
        return texto.replace(re,
            (m, caracterPrevio, minuscInicial, mayuscInicial, mayuscIntermedias) => {
                const locale = ['es', 'gl', 'ca', 'pt', 'en'];
                if (mayuscIntermedias)
                    return mayuscIntermedias.toLocaleLowerCase(locale);
                return caracterPrevio + (minuscInicial ? minuscInicial.toLocaleUpperCase(locale) : mayuscInicial);
            }
        );
    }

    //enviar formulario
    $('#form').on('submit', function (e) {
        e.preventDefault();
        $('select[name="tipo"]').prop('disabled', false);
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este proveedor?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este proveedor!', 'far fa-smile-wink', function () {
                        window.location.href = '/proveedor/lista';
                    });
                });
        }
    });

});
