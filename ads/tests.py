from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ad, ExchangeProposal

# Получаем модель пользователя
User = get_user_model()

class AdModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестового пользователя и объявления
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.ad = Ad.objects.create(
            user=cls.user,
            title='Test Ad',
            description='Test Description',
            category='electronics',
            condition='new'
        )

    def test_ad_creation(self):
        # Проверка правильности сохранения объявления
        self.assertEqual(self.ad.title, 'Test Ad')
        self.assertEqual(self.ad.user.username, 'testuser')

    def test_ad_list_view(self):
        # Проверка отображения объявления в списке
        response = self.client.get(reverse('ad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')

    def test_ad_detail_view(self):
        # Проверка детального просмотра объявления
        response = self.client.get(reverse('ad_detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Description')

    def test_ad_update_view(self):
        # Проверка обновления объявления авторизованным пользователем
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('ad_update', args=[self.ad.id]), {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'category': 'furniture',
            'condition': 'used'
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_ad_delete_view(self):
        # Проверка удаления объявления авторизованным пользователем
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('ad_delete', args=[self.ad.id]))
        self.assertRedirects(response, reverse('ad_list'))
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

class ExchangeProposalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание двух пользователей и двух объявлений
        cls.user1 = User.objects.create_user(username='user1', password='12345')
        cls.user2 = User.objects.create_user(username='user2', password='12345')

        cls.ad1 = Ad.objects.create(
            user=cls.user1,
            title='Ad 1',
            description='Desc 1',
            category='electronics',
            condition='new'
        )
        cls.ad2 = Ad.objects.create(
            user=cls.user2,
            title='Ad 2',
            description='Desc 2',
            category='furniture',
            condition='used'
        )

    def test_proposal_creation_view(self):
        # Проверка создания предложения обмена от user1 к user2
        self.client.login(username='user1', password='12345')
        response = self.client.post(reverse('exchange_proposals'), {
            'create_proposal': 1,
            'ad_sender_id': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Test proposal'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        proposal = ExchangeProposal.objects.first()
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_receiver, self.ad2)

    def test_proposal_status_update(self):
        # Проверка обновления статуса предложения (принятие)
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Proposal',
            status='pending'
        )
        self.client.login(username='user2', password='12345')
        response = self.client.post(reverse('update_proposal_status', args=[proposal.id, 'accepted']))
        self.assertEqual(response.status_code, 302)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')
