from django.views.generic.base import View

class InertiaResponseMixin:
  """A mixin that can be used to render an Inertia response"""

  component_name = None

  def render_to_response():
    pass
