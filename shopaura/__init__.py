# Backward compatibility alias for legacy libraries using removed ugettext/ugettext_lazy
try:
    import django.utils.translation as _translation
    if not hasattr(_translation, 'ugettext_lazy'):
        _translation.ugettext_lazy = _translation.gettext_lazy
    if not hasattr(_translation, 'ugettext'):
        _translation.ugettext = _translation.gettext
except (ImportError, AttributeError):
    pass

