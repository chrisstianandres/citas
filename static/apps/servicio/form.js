$(document).ready(function () {
    validador();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del servicio",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
        },
    });
    $("#form_serv").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del servicio",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_duracion').TouchSpin({
            min: 1,
            max: 4,
            step: 1,
            prefix: 'Hora/as',
            buttondown_class: 'btn btn-white btn-info btn-bold btn-xs',
            buttonup_class: 'btn btn-white btn-info btn-bold btn-xs',
        });

        $('#id_precio').TouchSpin({
            min: 0.50,
            max: 1000.00,
            step: 0.01,
            decimals: 2,
            prefix: '$',
            buttondown_class: 'btn btn-white btn-info btn-bold btn-xs',
            buttonup_class: 'btn btn-white btn-info btn-bold btn-xs',
        });

    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    $('#id_descripcion').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });


    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este servicio?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este servicio!', 'far fa-smile-wink', function () {
                        window.location.href = '/servicio/lista'
                    });
                });
        }
    });

});
