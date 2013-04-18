from django import forms
from django.utils.translation import ugettext_lazy as _

from uni_form.helpers import FormHelper, Submit, Layout

from selvbetjening.viewbase.forms.helpers import InlineFieldset
from selvbetjening.viewbase.forms import widgets

from models import Collection, Photographer

class BaseCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseCollectionForm, self).__init__(*args, **kwargs)

        submit = Submit(self.submit_value, self.submit_value)

        layout = Layout(InlineFieldset(_('Event'), 'slug', 'name', 'description', 'date', 'group'))

        self.helper = FormHelper()
        self.helper.add_input(submit)
        self.helper.add_layout(layout)

    date = forms.DateField(widget=widgets.UniformSelectDateWidget(
        years=range(2000, 2080)))

    class Meta:
        model = Collection

class CreateCollectionForm(BaseCollectionForm):
    submit_value = _('Add event')

class EditCollectionForm(BaseCollectionForm):
    submit_value = _('Edit event')

class BasePhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = ('user', 'slug', 'name', 'description')

    def __init__(self, *args, **kwargs):
        super(BasePhotographerForm, self).__init__(*args, **kwargs)

        submit = Submit(self.submit_value, self.submit_value)

        layout = Layout(InlineFieldset(_('Photographer'), *self.Meta.fields))

        self.helper = FormHelper()
        self.helper.add_input(submit)
        self.helper.add_layout(layout)

class CreatePhotographerForm(BasePhotographerForm):
    submit_value = _('Add photographer')

class LimitedEditPhotographerForm(BasePhotographerForm):
    submit_value = _('Edit photographer')

    class Meta(BasePhotographerForm.Meta):
        fields = ('name', 'description')

class EditPhotographerForm(BasePhotographerForm):
    submit_value = _('Edit photographer')

class UploadImagesToForm(forms.Form):
    def __init__(self, photographers, *args, **kwargs):
        super(UploadImagesToForm, self).__init__(*args, **kwargs)

        self.fields['photographer'] = \
            forms.ModelChoiceField(queryset=photographers, empty_label=None)

    submit = Submit(_('Upload images'), _('Upload images'))

    layout = Layout(InlineFieldset(_('Upload images as'), 'photographer'))

    helper = FormHelper()
    helper.add_input(submit)
    helper.add_layout(layout)

