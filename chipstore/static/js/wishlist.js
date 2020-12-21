$(window).on("load", function () {
    var cantidades = $(".cantidad");
    for (var i = 0; i < cantidades.length; i++) {
        var cantidad = $(`#cantidad-${i}`).val();
        var precio = $(`#precio-${i}`).html();
        var st = parseFloat(cantidad)*parseFloat(precio);
        $(`#subtotal-${i}`).html(numberWithCommas(st.toFixed(2)));
    }
});

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function enviaracarrito(item, id) {
    var item = item;
    var cantidad =  $(`#cantidad-${item}`).val();
    window.location.assign(`../to_carrito/${id}/${cantidad}`);
}
