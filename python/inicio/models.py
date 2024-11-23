from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, help_text="Título del post")
    content_markdown = models.TextField(help_text="Contenido en formato Markdown")
    content_html = models.TextField(editable=False, help_text="Contenido renderizado en HTML")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última fecha de actualización")

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para convertir el contenido Markdown en HTML
        antes de guardar el objeto en la base de datos.
        """
        from markdown2 import markdown  # Usamos la librería markdown2 para convertir Markdown a HTML
        self.content_html = markdown(self.content_markdown)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.JSONField()  # Almacena el JSON generado por Editor.js
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


