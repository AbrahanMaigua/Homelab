# Generated by Django 4.2.16 on 2024-11-16 01:13

from django.db import migrations, models
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', django_editorjs.fields.EditorJsField()),
            ],
        ),
    ]
