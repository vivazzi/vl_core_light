from django import forms
from vl_core.mixins import TemplateFormMixin


class TemplateForm(TemplateFormMixin, forms.ModelForm):
    class Meta:
        exclude = ()
