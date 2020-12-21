import json
import requests
from datetime import datetime
from django.shortcuts import redirect
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse, exceptions
from django.contrib import messages
from chipstore.tienda.models import Item, Compra, ItemCompra, Tienda, WhishList, ItemWhishList
from .utils import crear_objeto_tienda, enviar_correo
from django.template.response import TemplateResponse

TARGET_URI = "https://www.target.com/"


class HomeView(generic.TemplateView):
    template_name = "pages/home.html"

    def post(self, request, *args, **kwargs):
        busqueda = request._post["busqueda"]
        return redirect(reverse("tienda:resultados", kwargs={"busqueda": busqueda}))


class EliminarCarritoView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            item = ItemCompra.objects.get(id=kwargs["id"])
            item.delete()
        except ItemCompra.DoesNotExist:
            pass
        return redirect(
            reverse("tienda:carrito")
        )


class CarritoView(generic.TemplateView):
    template_name = "tienda/carrito.html"

    def get_context_data(self, **kwargs):
        context = super(CarritoView, self).get_context_data(**kwargs)
        try:
            context["carrito"] = Compra.objects.get(
                usuario=self.request.user, confirmado=False
            )
        except Compra.DoesNotExist:
            context["carrito"] = None
        return context

    def post(self, request, *args, **kwargs):
        compra = Compra.objects.get(usuario=self.request.user, confirmado=False)
        compra.confirmado = True
        compra.fecha = datetime.now()
        compra.total = request._post["total"]
        compra.save()
        context = {"carrito": compra}
        enviar_correo(
            "[The Chip Store] Gracias por su compra.",
            context,
            request.user.email,
            "admin@thechip.store",
        )
        return TemplateResponse(
            request, "tienda/compra_confirmada.html", context={"carrito": compra}
        )


class WishlistView(generic.TemplateView):
    template_name = "tienda/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        try:
            context["wishlist"] = WhishList.objects.get(
                usuario=self.request.user
            )
        except WhishList.DoesNotExist:
            context["wishlist"] = None
        return context


class EliminarItemWishlistView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            item = ItemWhishList.objects.get(id=kwargs["id"])
            item.delete()
        except Compra.DoesNotExist:
            pass
        return redirect(
            reverse("tienda:wishlist")
        )


class ItemWishToCompraView(generic.View):
    def get(self, request, *args, **kwargs):
        item = ItemWhishList.objects.get(id=kwargs["id"])
        cantidad = int(kwargs["cantidad"])
        if cantidad > 0:
            compra, compra_creada = Compra.objects.get_or_create(
                usuario=request.user, confirmado=False
            )
            ic, ic_created = ItemCompra.objects.get_or_create(compra=compra, item=item.item)
            if ic_created:
                ic.cantidad = cantidad
            else:
                ic.cantidad += int(cantidad)
            ic.save()
            item.delete()
            messages.success(request, "Se ha enviado al carrito.")
        else:
            messages.error(request, "No puede quedarse en 0 el artículo.")
        return redirect(
            reverse("tienda:wishlist")
        )


class DetalleCompraView(generic.TemplateView):
    template_name = "tienda/compra.html"

    def get_context_data(self, **kwargs):
        context = super(DetalleCompraView, self).get_context_data(**kwargs)
        try:
            context["carrito"] = Compra.objects.get(id=kwargs["id"])
        except Compra.DoesNotExist:
            context["carrito"] = None
        return context


class ResultsView(generic.TemplateView):
    template_name = "tienda/busqueda.html"

    def post(self, request, *args, **kwargs):
        busqueda = request._post["busqueda"]
        try:
            return redirect(reverse("tienda:resultados", kwargs={"busqueda": busqueda}))
        except exceptions.NoReverseMatch:
            return redirect(reverse("tienda:resultados", kwargs={"busqueda": kwargs["busqueda"]}))

    def request_api(self, url, params, headers={}, timeout=3):
        try:
            req = requests.get(url, params=params, headers=headers, timeout=timeout,)
            return req.json()
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException):
            return []

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context["resultados"] = []
        busqueda = kwargs["busqueda"]
        for tienda in Tienda.objects.all():
            if tienda.nombre == "TARGET":
                headers = {
                    "x-rapidapi-key": tienda.api_key,
                    "x-rapidapi-host": tienda.base_api_url.split("https://")[1],
                }
                base_url = tienda.base_api_url + '/product/search'
                params = {
                    'store_id': '2475',
                    'keyword': busqueda,
                    'sponsored': '1',
                    'limit': '50',
                    'offset': '0'
                }
                respuesta = self.request_api(base_url, params, headers)
                context["resultados"] += crear_objeto_tienda(
                    tienda.nombre, respuesta
                )
            elif tienda.nombre == "BESTBUY":
                base_url = tienda.base_api_url + '/v1/products(search={})'.format(busqueda)
                for i in range(1, 4):
                    params = {
                        'format': 'json', 'page': i,
                        'show': 'sku,salePrice,name,url,image,shortDescription',
                        'apiKey': tienda.api_key
                    }
                    respuesta = self.request_api(base_url, params)
                    context["resultados"] += crear_objeto_tienda(
                        tienda.nombre, respuesta
                    )
        context["n_resultados"] = len(context["resultados"])
        context["busqueda"] = kwargs["busqueda"]
        return context


class AgregarCarritoView(generic.View):
    def post(self, request, *args, **kwargs):
        payload = request._post
        precio = payload["precio"].split("$")
        precio_final = float("".join(precio))
        item, item_creado = Item.objects.get_or_create(
            sku=payload["sku"],
            nombre=payload["nombre"],
            uri=payload["url"],
            foto=payload["imagen"],
            descripcion=payload["descripcion"],
            precio=precio_final,
            tienda=Tienda.objects.get(nombre=payload["tienda"]),
        )
        compra, compra_creada = Compra.objects.get_or_create(
            usuario=request.user, confirmado=False
        )
        ic, ic_created = ItemCompra.objects.get_or_create(compra=compra, item=item)
        if ic_created:
            ic.cantidad = payload["cantidad"]
        else:
            ic.cantidad += int(payload["cantidad"])
        ic.save()
        return JsonResponse({"status": "Ítems añadidos al carrito."})


class AgregarWishlistView(generic.View):
    def post(self, request, *args, **kwargs):
        payload = request._post
        precio = payload["precio"].split("$")
        precio_final = float("".join(precio))
        item, item_creado = Item.objects.get_or_create(
            sku=payload["sku"],
            nombre=payload["nombre"],
            uri=payload["url"],
            foto=payload["imagen"],
            descripcion=payload["descripcion"],
            precio=precio_final,
            tienda=Tienda.objects.get(nombre=payload["tienda"]),
        )
        wishlist, wishlist_creada = WhishList.objects.get_or_create(
            usuario=request.user
        )
        iw, iw_created = ItemWhishList.objects.get_or_create(whishlist=wishlist, item=item)
        if iw_created:
            iw.cantidad = payload["cantidad"]
        else:
            iw.cantidad += int(payload["cantidad"])
        iw.save()
        return JsonResponse({"status": "Ítems añadidos al carrito."})
