from django.db import models
from django.contrib.auth import get_user_model
from chipstore.utils.common import get_image_directory_path

User = get_user_model()


class Tienda(models.Model):
    TIENDA_CHOICES = (
        ("BESTBUY", "Best Buy"),
        ("TARGET", "Target")
    )
    nombre = models.CharField('Tienda disponible de dispositivo', max_length=80, choices=TIENDA_CHOICES, unique=True)
    api_key = models.CharField(max_length=80)
    base_api_url = models.URLField()
    base_web_url = models.URLField()

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"

    def __str__(self):
        return self.nombre


class Item(models.Model):
    sku = models.CharField(max_length=80, unique=True)
    nombre = models.CharField(max_length=150, blank=True)
    uri = models.URLField(max_length=400)
    foto = models.ImageField(upload_to=get_image_directory_path)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.nombre if self.nombre else self.descripcion[:15]


class Compra(models.Model):
    item = models.ManyToManyField(Item, through="ItemCompra")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    fecha = models.DateField(null=True)
    total = models.FloatField(null=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        value = "{} de {}"
        if self.confirmado:
            return value.format("Compra", self.usuario.name)
        return value.format("Carrito", self.usuario.name)


class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)

    class Meta:
        verbose_name = "ItemCompra"
        verbose_name_plural = "ItemCompras"

    def __str__(self):
        pass


class WhishList(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, through="ItemWhishList")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "WhishList"
        verbose_name_plural = "WhishLists"

    def __str__(self):
        value = "{} de {}"
        return value.format("WishList", self.usuario.name)


class ItemWhishList(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    whishlist = models.ForeignKey(WhishList, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=True)

    class Meta:
        verbose_name = "ItemWhishList"
        verbose_name_plural = "ItemWhishLists"

    def __str__(self):
        pass
