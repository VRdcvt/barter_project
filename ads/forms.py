from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }

class ProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)

        # Кастомный label
        self.fields['ad_receiver'].label_from_instance = lambda obj: f"id {obj.id} ({obj.title})"

    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'comment']
    
    def clean(self):
        cleaned_data = super().clean()
        ad_receiver = cleaned_data.get('ad_receiver')
        
        # Дополнительные проверки можно добавить здесь
        if ad_receiver and not ad_receiver.is_active:
            raise forms.ValidationError("Выбранное объявление неактивно")
        
        return cleaned_data

class StatusUpdateForm(forms.Form):
    new_status = forms.ChoiceField(
        choices=ExchangeProposal.STATUS_CHOICES,
        label="Новый статус"
    )
    proposal_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )