from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка на категорию")

    def get_absolute_url(self):
        return reverse("shop:category_product", args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products', verbose_name="Категория товара")
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="Ссылка на товар")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена товара")
    available = models.BooleanField(default=True, verbose_name="Наличие на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title} | {self.category}"

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)


class Comments(models.Model):

    RATING_NEUTRAL = '0'
    RATING_BAD = '1'
    RATING_COOL = '2'
    RATING_GOOD = '3'
    RATING_PERFECT = '4'
    RATING_AMAZING = '5'

    RATING_CHOICE = (
        (RATING_NEUTRAL, 0),
        (RATING_BAD, 1),
        (RATING_COOL, 2),
        (RATING_GOOD, 3),
        (RATING_PERFECT, 4),
        (RATING_AMAZING, 5),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    star_count = models.CharField(max_length=120, choices=RATING_CHOICE, default=RATING_NEUTRAL,
                                  verbose_name="Рейтинг")
    comment = models.TextField(max_length=5000, verbose_name="Текст комментария")
    likes = models.ManyToManyField(User, related_name="comment_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="comments_dislikes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария")
    is_valid = models.BooleanField(default=True, verbose_name="Допустить к публикации")

    def __str__(self):
        return f"{self.author} | {self.star_count}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class UserProfile(models.Model):

    LOCATION_SELECT = (
        ('NO', 'Unknown'),
        ('EU', 'Europe'),
        ('USA', 'United States of America'),
        ('JP', 'Japan'),
        ('FR', 'Franca'),
        ('CN', 'China'),
        ('AE', 'United Arab Emirates')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name="Профиль")
    picture = models.ImageField(upload_to='profile/pictures/', default='default-profile.jpg',
                                blank=True)
    quote = models.CharField(max_length=350, blank=True, null=True, verbose_name="Описание/Цитата")
    location = models.CharField(max_length=40, choices=LOCATION_SELECT, default='NO',
                                verbose_name="Страна")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания аккаунта")

    def __unicode__(self):
        return self.user

    def get_absolute_url(self):
        return reverse('shop:profile_view', kwargs={'id': self.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

