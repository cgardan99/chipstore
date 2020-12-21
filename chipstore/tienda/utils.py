from .models import Tienda
import html2text
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def crear_objeto_tienda(tienda, respuesta):
    target = Tienda.objects.get(nombre="TARGET")
    bby = Tienda.objects.get(nombre="BESTBUY")
    objeto = []
    if tienda == "BESTBUY":
        try:
            for producto in respuesta["products"]:
                objeto.append({
                    "tienda": "BESTBUY",
                    "url": producto["url"],
                    "sku": producto["sku"],
                    "thumbnail": producto["image"],
                    "nombre": producto["name"],
                    "precio": producto["salePrice"],
                    "descripcion": producto["shortDescription"]
                })
        except KeyError:
            pass
    elif tienda == "TARGET":
        try:
            for producto in respuesta["products"]:
                img = producto["images"][0]
                objeto.append({
                    "tienda": "TARGET",
                    "url": target.base_web_url + producto["url"],
                    "sku": producto["tcin"],
                    "precio": producto["price"]["formatted_current_price"],
                    "thumbnail": img["base_url"] + img["primary"],
                    "nombre": producto["title"],
                    "descripcion": producto["description"]
                })
        except KeyError:
            pass
    return objeto


def enviar_correo(subject, context, to, from_email):
    body = render_to_string("tienda/email_compra.html", context)
    text_body = html2text.html2text(body)
    email_message = EmailMultiAlternatives(subject, text_body, "admin@thechip.store", [to])
    email_message.attach_alternative(body, 'text/html')
    email_message.send()
