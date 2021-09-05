var check = 0;
var user_tipo = parseInt($('#user_tipo').val());

function graficos() {
    var ctx = document.getElementById('myChart').getContext('2d');
    const skipped = (ctx, value) => ctx.p0.skip || ctx.p1.skip ? value : undefined;
    const down = (ctx, value) => ctx.p0.parsed.y > ctx.p1.parsed.y ? value : undefined;
    $.ajax({
        url: '/transaccion/chart',
        type: 'POST',
        data: {'action': 'chart'},
        dataSrc: "",
    }).done(function (data) {
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                    'Noviembre', 'Diciembre'],
                datasets: [{
                    label: 'Ventas del año ' + data['year'],
                    data: data['ventas'],
                    borderColor: 'rgb(75, 192, 192)',
                    segment: {
                        borderColor: ctx => skipped(ctx, 'rgb(0,0,0,0.2)') || down(ctx, 'rgb(192,75,75)'),
                        borderDash: ctx => skipped(ctx, [6, 6]),
                    }
                }]
            },
            options: {
                fill: false,
                interaction: {
                    intersect: false
                },
                radius: 0,
                title: {
                    display: true,
                    text: 'Compras y ventas del año ' + data['year'] + ' en Dolares Americanos'
                }
            }
        });
        $('#citas_dia').html(data['tarjets'].data.citas_dia);
        $('#citas_semana_hoy').html(data['tarjets'].data.citas_semana_hoy);
        $('#total_empleados').html(data['tarjets'].data.total_empleados);
        $('#recaudacion_dia').html('$ ' + data['tarjets'].data.recaudacion_dia);
        $('#recaudacion_semana').html('$ ' + data['tarjets'].data.recaudacion_semana);
        var indicador = [], item = [];
        $.each(data['carrusel'], function (key, value) {
            if (key === 0) {
                indicador.push('<li data-target="#myCarousel" data-slide-to="' + key + '" class="active"></li>');
                item.push('<div class="item active"><img src="' + value.imagen + '" alt="' + value.nombre + '" style="width:100%;">' +
                    '<div class="carousel-caption"><h2>' + value.nombre + '</h2><p>' + value.descripcion + '</p></div></div>')
            } else {
                indicador.push('<li data-target="#myCarousel" data-slide-to="' + key + '"></li>');
                item.push('<div class="item"><img src="' + value.imagen + '" alt="' + value.nombre + '" style="width:100%;">' +
                    '<div class="carousel-caption"><h2>' + value.nombre + '</h2><p>' + value.descripcion + '</p></div></div>')
            }
        });
        $('.carousel-indicators').html(indicador);
        $('.carousel-inner').html(item);
        $('#citas_not').html(data['tarjets'].data.citas_not);
    });
}

function cliente() {
    $.ajax({
        url: '/transaccion/chart',
        type: 'POST',
        data: {'action': 'chart'},
        dataSrc: "",
    }).done(function (data) {
        var indicador = [], item = [];
        $.each(data['carrusel'], function (key, value) {
            if (key === 0) {
                indicador.push('<li data-target="#myCarousel" data-slide-to="' + key + '" class="active"></li>');
                item.push('<div class="item active"><img src="' + value.imagen + '" alt="' + value.nombre + '" style="width:100%;">' +
                    '<div class="carousel-caption"><h2>' + value.nombre + '</h2><p>' + value.descripcion + '</p></div></div>')
            } else {
                indicador.push('<li data-target="#myCarousel" data-slide-to="' + key + '"></li>');
                item.push('<div class="item"><img src="' + value.imagen + '" alt="' + value.nombre + '" style="width:100%;">' +
                    '<div class="carousel-caption"><h2>' + value.nombre + '</h2><p>' + value.descripcion + '</p></div></div>')
            }
        });
        $('.carousel-indicators').html(indicador);
        $('.carousel-inner').html(item);
        $('#citas_not').html(data['tarjets'].data.citas_not);
    });
}
$(function () {
    if (user_tipo === 1) {
        graficos();
        $('#stock_table').Datatable();
    } else {
        cliente();
    }

});
