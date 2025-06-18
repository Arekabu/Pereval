from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator


class User(models.Model):
    fam = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    otc = models.CharField(max_length=50, verbose_name='Отчество')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc or ""}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Coords(models.Model):
    latitude = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        verbose_name='Широта',
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )

    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        verbose_name='Долгота',
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f'{self.latitude}, {self.longitude}, {self.height}.'

    class Meta:
        verbose_name='Координаты'
        verbose_name_plural = 'Координаты'


class Pereval(models.Model):

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("pending", "На проверке"),
        ("accepted", "Принят"),
        ("rejected", "Отклонён"),
    ]

    LEVEL_CHOICES = [
        ('', 'Не указано'),
        ('1A', '1A'), ('1B', '1B'), ('1C', '1C'),
        ('2A', '2A'), ('2B', '2B'), ('2C', '2C'),
        ('3A', '3A'), ('3B', '3B'), ('3C', '3C'),
    ]

    title = models.CharField(max_length=100)
    beauty_title = models.CharField(max_length=19, blank=True, null=True)
    other_titles = models.CharField(max_length=100, blank=True, null=True)
    connect = models.TextField(max_length=250, blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)

    winter = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Зима"
    )
    summer = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Лето"
    )
    autumn = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Осень"
    )
    spring = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Весна"
    )

    status = models.CharField(max_length=19, choices=STATUS_CHOICES, default='new')


class Image(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images', verbose_name="Перевал")

    data = models.ImageField(
        upload_to='pereval_images/%Y/%m/%d/',
        verbose_name="Изображение",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ],
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255, verbose_name="Название изображения", blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Изображение перевала"
        verbose_name_plural = "Изображения перевалов"

    def __str__(self):
        return f"{self.title} (Перевал: {self.pereval.title})"
