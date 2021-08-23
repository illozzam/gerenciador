from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('financeiro/', include(('financeiro.urls', 'financeiro'), namespace='financeiro')),
	path('', include(('principal.urls', 'principal'), namespace='principal')),

	path('admin/', admin.site.urls),

	path('summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
