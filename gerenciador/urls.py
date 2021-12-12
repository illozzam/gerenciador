from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', include(('principal.urls', 'principal'), namespace='principal')),
	path('', include(('https.urls', 'https'), namespace='https')),
	path('financeiro/', include(('financeiro.urls', 'financeiro'), namespace='financeiro')),

	path('admin/', admin.site.urls),
]
