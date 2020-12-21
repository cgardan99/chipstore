from django.urls import path, re_path

from chipstore.tienda.views import (
    HomeView,
    ResultsView,
    AgregarCarritoView,
    CarritoView,
    EliminarCarritoView,
    DetalleCompraView,
    AgregarWishlistView,
    WishlistView,
    ItemWishToCompraView,
    EliminarItemWishlistView
)

app_name = "tienda"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    re_path(r"resultados/(?P<busqueda>\w+)", ResultsView.as_view(), name="resultados"),
    path("agregar_carrito", AgregarCarritoView.as_view(), name="agregar_carrito"),
    path("agregar_wishlist", AgregarWishlistView.as_view(), name="agregar_wishlist"),
    re_path(
        r"eilminar_carrito/(?P<id>\d+)",
        EliminarCarritoView.as_view(),
        name="eliminar",
    ),
    path("carrito/", CarritoView.as_view(), name="carrito"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    re_path(r"compra/(?P<id>\d+)", DetalleCompraView.as_view(), name="detalle_compra"),
    re_path(
        r"to_carrito/(?P<id>\d+)/(?P<cantidad>\d+)",
        ItemWishToCompraView.as_view(),
        name="cambiar_a_carrito",
    ),
    re_path(
        r"eliminar_wishlist/(?P<id>\d+)",
        EliminarItemWishlistView.as_view(),
        name="eliminar_wishlist",
    ),
]
