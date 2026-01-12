from django import forms
from apps.personnel.models import Personnel
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet du message'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message ici...', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        # On affiche tous les personnels par défaut
        self.fields['recipient'].queryset = Personnel.objects.all()
