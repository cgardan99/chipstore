$(window).on("load", function () {
    var cantidades = $(".cantidad");
    var total = 0;
    for (var i = 0; i < cantidades.length; i++) {
        var cantidad = $(`#cantidad-${i}`).html();
        var precio = $(`#precio-${i}`).html();
        var st = parseFloat(cantidad)*parseFloat(precio);
        total += st;
        $(`#subtotal-${i}`).html(numberWithCommas(st.toFixed(2)));
    }
    $("#grand_total").html(numberWithCommas(total.toFixed(2)));
    $("#total").val(total.toFixed(2));
});

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
