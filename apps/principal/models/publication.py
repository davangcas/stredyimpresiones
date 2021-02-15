from django.db import models

from apps.administracion.models import Producto

class Publication(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Imagen', upload_to="publicacion/%y/%m")
    title = models.CharField(verbose_name="Nombre", max_length=80)
    date_created = models.DateTimeField(verbose_name="Fecha de publicación", auto_now_add=True)
    detail = models.CharField(verbose_name="Descripción", max_length=1000, default="Ninguna")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'