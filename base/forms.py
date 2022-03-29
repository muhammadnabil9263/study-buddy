from django.forms import ModelForm, Textarea ,ModelChoiceField

from .models import Room , Topic


class RoomForm(ModelForm):
    topic = ModelChoiceField(queryset=Topic.objects.all() , empty_label="choose topic")
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'description': Textarea(attrs={"placeholder": "Write about your study group..."}),

        }
