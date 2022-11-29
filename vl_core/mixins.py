from django.db.models import Max
from django.template.loader import select_template
from django.urls import reverse

from vl_core.template_pool import template_pool


class AdminUrlsMixin:
    def get_admin_absolute_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.id,))

    @classmethod
    def get_admin_changelist_url(cls):
        return reverse(f'admin:{cls._meta.app_label}_{cls._meta.model_name}_changelist')


class RenderTemplateMixin:
    template_is_not_found = 'vl_core/template_is_not_found.html'

    def get_render_template(self, context, instance, placeholder):
        if instance.template:
            template_class = template_pool.get_template(instance, instance.template)
            if template_class:
                required_template = template_class().get_template(instance, context)
                template = select_template([required_template, self.template_is_not_found]).template.name

                if template == self.template_is_not_found:
                    context['required_template'] = required_template

                return template

        return self.render_template

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        if instance.template:
            template_class = template_pool.get_template(instance, instance.template)
            if template_class:
                context.update(template_class().get_context(instance=instance, plugin_context=context))

        return context

    def get_cache_expiration(self, request, instance, placeholder):
        template_class = template_pool.get_template(instance, instance.template)
        if template_class:
            return template_class().cache

        return None


class TemplateFormMixin:
    def clean(self):
        template_class = template_pool.get_template(self.instance, self.cleaned_data['template'])
        if template_class:
            template_class().clean(self)
