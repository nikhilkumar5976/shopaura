from .models import Category

# ==============================================================================
# Category Context Processors
# ==============================================================================

def menu_links(request):
    """
    Context processor that injects category links into every template context.
    Configured in settings.TEMPLATES['OPTIONS']['context_processors'].
    Enables components like the top navbar and catalog sidebar to render categories
    without having to pass them explicitly from every view function.
    """
    links = Category.objects.all()
    return dict(links=links)