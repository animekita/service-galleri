from django import forms
from django.utils.translation import ugettext_lazy as _

from uni_form.helpers import FormHelper, Submit, Fieldset, Layout, HTML

from selvbetjening.viewhelpers.forms.helpers import InlineFieldset

from models import Collection, Photographer, Picture

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)

        submit = Submit(self.submit_value, self.submit_value)

        layout = Layout(InlineFieldset(_('Event'), 'name', 'description'))

        self.helper = FormHelper()
        self.helper.add_input(submit)
        self.helper.add_layout(layout)

class CreateCollectionForm(CollectionForm):
    submit_value = _('Add event')

class EditCollectionForm(CollectionForm):
    submit_value = _('Edit event')

class PhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer

    def __init__(self, *args, **kwargs):
        super(PhotographerForm, self).__init__(*args, **kwargs)


        submit = Submit(self.submit_value, self.submit_value)

        layout = Layout(InlineFieldset(_('Photographer'), 'name', 'description'))

        helper = FormHelper()
        helper.add_input(submit)
        helper.add_layout(layout)

class CreatePhotographerForm(PhotographerForm):
    submit_value = _('Add photographer')

class EditPhotographerForm(PhotographerForm):
    submit_value = _('Edit photographer')

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture

    submit = Submit(_('Edit picture'), _('Edit picture'))

    layout = Layout(InlineFieldset(_('Picture'), 'original', 'caption', 'collection', 'photographer'))

    helper = FormHelper()
    helper.add_input(submit)
    helper.add_layout(layout)

class UploadImagesToForm(forms.Form):
    collection = forms.ModelChoiceField(queryset=Collection.objects.all(),
                                        empty_label=None)

    photographer = forms.ModelChoiceField(queryset=Photographer.objects.all(),
                                          empty_label=None)

    submit = Submit(_('Upload images'), _('Upload images'))

    layout = Layout(InlineFieldset(_('Upload images to'), 'collection', 'photographer'))

    helper = FormHelper()
    helper.add_input(submit)
    helper.add_layout(layout)

