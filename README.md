# vl_core_light

vl_core_light is vl_core (https://github.com/vivazzi/vl_core) without django-cms support.


## Installation

There is no vl_core_light in PyPI, so you can install this package from repository only.

```shell
$ pip install git+https://github.com/vivazzi/vl_core_light.git
```

Also, you need install django-vite from repo: `https://github.com/vivazzi/django-vite/tree/multi-config` - this is fork
with extended functionality:

```shell
$ pip install git+https://github.com/vivazzi/django-vite.git@multi-config
```

## Configuration

Add "vl_core" to INSTALLED_APPS

```python
INSTALLED_APPS = (
    ...
    'django_vite',
    'vl_core',
    ...
)
```

Run `python manage.py test vl_core`


# CONTRIBUTING

To reporting bugs or suggest improvements, please use the [issue tracker](https://github.com/vivazzi/vl_core_light/issues).

Thank you very much, that you would like to contribute to vl_core_light. Thanks to the [present, past and future contributors](https://github.com/vivazzi/vl_core_light/contributors).

If you think you have discovered a security issue in our code, please do not create issue or raise it in any public forum until we have had a chance to deal with it.
**For security issues use security@vuspace.pro**


# LINKS

- Project's home: https://github.com/vivazzi/vl_core_light
- Report bugs and suggest improvements: https://github.com/vivazzi/vl_core_light/issues
- Author's site, Artem Maltsev: https://vivazzi.pro

# LICENCE

Copyright © 2022 Artem Maltsev and contributors.

MIT licensed.
