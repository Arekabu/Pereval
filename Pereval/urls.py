from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pereval_app.urls')),
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
 ]
