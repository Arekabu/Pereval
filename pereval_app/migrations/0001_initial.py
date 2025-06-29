# Generated by Django 5.2.3 on 2025-06-16 13:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=7, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=8, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Долгота')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
            options={
                'verbose_name': 'Координаты',
                'verbose_name_plural': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('otc', models.CharField(max_length=50, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('beauty_title', models.CharField(blank=True, max_length=19, null=True)),
                ('other_titles', models.CharField(blank=True, max_length=100, null=True)),
                ('connect', models.TextField(blank=True, max_length=250, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('winter', models.CharField(blank=True, choices=[('', 'Не указано'), ('1A', '1A'), ('1B', '1B'), ('1C', '1C'), ('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'), ('3B', '3B'), ('3C', '3C')], max_length=2, null=True, verbose_name='Зима')),
                ('summer', models.CharField(blank=True, choices=[('', 'Не указано'), ('1A', '1A'), ('1B', '1B'), ('1C', '1C'), ('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'), ('3B', '3B'), ('3C', '3C')], max_length=2, null=True, verbose_name='Лето')),
                ('autumn', models.CharField(blank=True, choices=[('', 'Не указано'), ('1A', '1A'), ('1B', '1B'), ('1C', '1C'), ('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'), ('3B', '3B'), ('3C', '3C')], max_length=2, null=True, verbose_name='Осень')),
                ('spring', models.CharField(blank=True, choices=[('', 'Не указано'), ('1A', '1A'), ('1B', '1B'), ('1C', '1C'), ('2A', '2A'), ('2B', '2B'), ('2C', '2C'), ('3A', '3A'), ('3B', '3B'), ('3C', '3C')], max_length=2, null=True, verbose_name='Весна')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('pending', 'На проверке'), ('accepted', 'Принят'), ('rejected', 'Отклонён')], default='new', max_length=19)),
                ('coords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.coords')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ImageField(blank=True, null=True, upload_to='pereval_images/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Изображение')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название изображения')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval_app.pereval', verbose_name='Перевал')),
            ],
            options={
                'verbose_name': 'Изображение перевала',
                'verbose_name_plural': 'Изображения перевалов',
            },
        ),
    ]
