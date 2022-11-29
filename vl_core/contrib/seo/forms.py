from django import forms


class SEOForm(forms.ModelForm):
    class Meta:
        exclude = ()
        widgets = {
            'meta_tags': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            'meta_desc': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }
