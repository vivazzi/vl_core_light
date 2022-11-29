from django import forms
from django.core import management
from django.utils.translation import gettext as _


class RunManagementCommandForm(forms.Form):
    commands = [(f'{app}.{command}', command) for command, app in management.get_commands().items()]
    command = forms.ChoiceField(label=_('Commands'), choices=commands)
    params = forms.CharField(label=_('Parameters'), required=False)
