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
            categoria: {
                required: true
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
            categoria: {
                required: "Por favor selecciona una categoria"
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
            categoria: {
                required: true
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
            categoria: {
                required: "Por favor selecciona una categoria"
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
        }).keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros;

        $('#id_precio').TouchSpin({
            min: 2.50,
            max: 200.00,
            step: 0.01,
            decimals: 2,
            prefix: '$',
            buttondown_class: 'btn btn-white btn-info btn-bold btn-xs',
            buttonup_class: 'btn btn-white btn-info btn-bold btn-xs',
        }).keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros;

    $('#id_nombre').keyup(function () {
        var changue = titleCase($(this).val());
        $(this).val(changue);
    }).keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras

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
