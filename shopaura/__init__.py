# Backward compatibility shims for legacy packages (e.g. django-admin-honeypot) on modern Django
try:
    import django.utils.translation as _translation
    if not hasattr(_translation, 'ugettext_lazy'):
        _translation.ugettext_lazy = _translation.gettext_lazy
    if not hasattr(_translation, 'ugettext'):
        _translation.ugettext = _translation.gettext
except (ImportError, AttributeError):
    pass

try:
    import django.urls
    import django.conf.urls
    if not hasattr(django.conf.urls, 'url'):
        django.conf.urls.url = django.urls.re_path
except (ImportError, AttributeError):
    pass

try:
    import django.dispatch
    _orig_signal_init = django.dispatch.Signal.__init__
    def _compat_signal_init(self, *args, **kwargs):
        kwargs.pop('providing_args', None)
        return _orig_signal_init(self, *args, **kwargs)
    django.dispatch.Signal.__init__ = _compat_signal_init
except (ImportError, AttributeError):
    pass

try:
    import django.utils.html
    _orig_format_html = django.utils.html.format_html
    def _compat_format_html(format_string, *args, **kwargs):
        if not args and not kwargs:
            return django.utils.html.mark_safe(format_string)
        return _orig_format_html(format_string, *args, **kwargs)
    django.utils.html.format_html = _compat_format_html
except (ImportError, AttributeError):
    pass
