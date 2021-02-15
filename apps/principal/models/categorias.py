from django.db import models

class Categoria(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Subcategoria(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=80)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"
