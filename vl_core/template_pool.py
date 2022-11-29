from django.utils.translation import gettext_lazy as _


class Template:
    template = None
    title = None
    cache = None  # in seconds

    def get_template(self, instance, context=None, *args, **kwargs):
        return self.template

    def get_context(self, *args, **kwargs):
        return {}

    def clean(self, form):
        pass


class TemplatePool:
    """
        templates in TemplatePool objects contains plugins grouped by name. Name maybe pool (str) or model

        Ex: templates = {
            'sb_link': {
                'orange_btn': OrangeBtn,
                ...
            },
            ...
        }
    """
    def __init__(self):
        self.templates = {}

    def register(self, pool=None, model=None):
        def decorator(template):
            if pool is None and model is None or (pool and model):
                raise Exception(f'You need use pool or model parameter for {template.__name__}')

            if model:
                _pool = model.__name__
            else:
                _pool = pool

            template_name = template.__name__
            if _pool in self.templates and template_name in self.templates[_pool]:
                raise TemplateAlreadyRegistered(
                    f'Cannot register {template}, a command with this name ({template_name}) is already registered.')

            template.name = template_name
            self.templates.setdefault(_pool, {})[template_name] = template

            return template

        return decorator

    def unregister(self, pool, template):
        template_name = template.__name__
        if pool not in self.templates or pool in self.templates and template_name not in self.templates[pool]:
            raise TemplateNotRegistered(f'Command {template_name} is not registered')
        del self.templates[pool][template_name]

    def get_pools(self):
        return self.templates.keys()

    def get_template(self, instance, name):
        if name == '':
            return ''

        pool = instance.pool if hasattr(instance, 'pool') else instance.__class__.__name__
        try:
            return self.templates[pool][name]
        except KeyError:
            return None

    def obj_template_str(self, obj, title='', use_brackets=False):
        template = self.get_template(obj, obj.template)

        if template == '':
            return ''

        if template is None:
            res_title = _(f'Template class "{obj.template}" is not found')
        else:
            res_title = f'{_("T")}: {template.title}'

        if title or use_brackets:
            res_title = f' ({res_title})'

        return str(res_title)


class TemplateAlreadyRegistered(Exception):
    pass


class TemplateNotRegistered(Exception):
    pass


template_pool = TemplatePool()
