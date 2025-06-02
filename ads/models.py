from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

# Получаем модель пользователя
User = get_user_model()

class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у')
    ]
    
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('furniture', 'Мебель'),
        ('other', 'Другое')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name="Пользователь"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL изображения")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, verbose_name="Состояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']
    
    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse('ad_detail', kwargs={'pk': self.pk})


class ExchangeProposal(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_ACCEPTED, 'Принята'),
        (STATUS_REJECTED, 'Отклонена'),
    ]
    
    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name="Отправляющее объявление"
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name="Получающее объявление"
    )
    comment = models.TextField(verbose_name="Комментарий")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Предложение {self.pk}: {self.ad_sender_id} → {self.ad_receiver_id}"
    
    def can_be_updated_by(self, user):
        """Проверяет, может ли пользователь изменять предложение"""
        if not user or not user.pk:
            return False
        return user.pk in {self.ad_receiver.user_id, self.ad_sender.user_id}