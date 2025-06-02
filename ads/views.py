from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
import logging

# Получаем логгер
logger = logging.getLogger(__name__)

def ad_list(request):
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')
    
    # Получаем choices из модели
    category_choices = Ad.CATEGORY_CHOICES
    condition_choices = Ad.CONDITION_CHOICES
    
    # Фильтрация
    search_query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query))
    
    if category:
        ads = ads.filter(category=category)
    
    if condition:
        ads = ads.filter(condition=condition)
    
    # Пагинация
    paginator = Paginator(ads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_choices': category_choices,
        'condition_choices': condition_choices,
    })

@login_required
def exchange_proposals(request):
    form = ProposalForm(request.POST or None, user=request.user)

    # Создание предложения
    if request.method == 'POST' and 'create_proposal' in request.POST:
        if form.is_valid():
            try:
                ad_sender_id = request.POST.get('ad_sender_id')
                if not ad_sender_id:
                    messages.error(request, 'Не выбрано ваше объявление для обмена')
                    return redirect('exchange_proposals')
                ad_sender = get_object_or_404(Ad, pk=ad_sender_id, user=request.user)

                proposal = form.save(commit=False)
                proposal.ad_sender = ad_sender
                proposal.status = 'pending'
                proposal.save()

                messages.success(request, 'Предложение обмена успешно создано!')
                return redirect('exchange_proposals')
            except (ObjectDoesNotExist, ValidationError, IntegrityError) as e:
                messages.error(request, f'Ошибка при создании предложения: {str(e)}')
            except Exception as e:
                logger.exception("Неизвестная ошибка при создании предложения обмена: %s", str(e))
                messages.error(request, 'Произошла непредвиденная ошибка. Попробуйте позже.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    # Фильтрация
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    ).select_related('ad_sender__user', 'ad_receiver__user').order_by('-created_at')

    filter_type = request.GET.get('type', 'all')
    if filter_type == 'sent':
        proposals = proposals.filter(ad_sender__user=request.user)
    elif filter_type == 'received':
        proposals = proposals.filter(ad_receiver__user=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        proposals = proposals.filter(status=status_filter)

    # 🔹 Фильтрация по username отправителя/получателя
    sender_user = request.GET.get('sender_user')
    receiver_user = request.GET.get('receiver_user')

    if sender_user:
        proposals = proposals.filter(ad_sender__user__username=sender_user)
    if receiver_user:
        proposals = proposals.filter(ad_receiver__user__username=receiver_user)

    # 🔹 Списки уникальных пользователей
    unique_senders = sorted(set(p.ad_sender.user.username for p in proposals))
    unique_receivers = sorted(set(p.ad_receiver.user.username for p in proposals))

    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'proposals': page_obj.object_list,
        'current_filter': filter_type,
        'status_filter': status_filter,
        'status_choices': ExchangeProposal.STATUS_CHOICES,
        'sender_user': sender_user,
        'receiver_user': receiver_user,
        'unique_senders': unique_senders,
        'unique_receivers': unique_receivers,
    }

    return render(request, 'ads/exchange_proposals.html', context)


@login_required
def ad_create(request):
    if request.method == 'POST':
        # пользователь нажал "Подтвердить"
        if 'confirm' in request.POST:
            form = AdForm(request.POST)
            if form.is_valid():
                ad = form.save(commit=False)
                ad.user = request.user
                ad.save()
                messages.success(request, 'Объявление успешно создано!')
                return redirect('ad_detail', pk=ad.pk)

        # пользователь нажал "Сохранить", но мы ещё не сохраняем
        elif 'preview' in request.POST:
            form = AdForm(request.POST)
            if form.is_valid():
                ad_preview = form.save(commit=False)
                return render(request, 'ads/ad_confirm_create.html', {
                    'form': form,
                    'ad_preview': ad_preview
                })
    else:
        form = AdForm()

    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    
    return render(request, 'ads/ad_update.html', {'form': form})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление успешно удалено!')
        return redirect('ad_list')
    
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def ad_delete_by_id(request):
    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        try:
            ad = Ad.objects.get(pk=ad_id, user=request.user)
            ad.delete()
            messages.success(request, f'Объявление с ID {ad_id} успешно удалено.')
        except Ad.DoesNotExist:
            messages.error(request, f'Объявление с ID {ad_id} не найдено или не принадлежит вам.')
    return redirect('ad_list')

@login_required
def ad_edit_by_id(request):
    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')
        try:
            ad = Ad.objects.get(pk=ad_id, user=request.user)
            return redirect('ad_update', pk=ad.pk)
        except Ad.DoesNotExist:
            messages.error(request, f'Объявление с ID {ad_id} не найдено или не принадлежит вам.')
    return redirect('ad_list')

@login_required
def update_proposal_status(request, pk, status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    
    if not proposal.can_be_updated_by(request.user):
        messages.error(request, 'У вас нет прав для изменения этого предложения')
        return redirect('ad_list')
    
    if status in [ExchangeProposal.STATUS_ACCEPTED, ExchangeProposal.STATUS_REJECTED]:
        proposal.status = status
        proposal.save()
        messages.success(request, f'Предложение {proposal.get_status_display().lower()}!')
    
    return redirect('exchange_proposals')

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})