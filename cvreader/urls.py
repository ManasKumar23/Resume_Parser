from django.contrib import admin
from django.urls import path,include
from cvreader import views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reader/',csrf_exempt(views.reader),name='reader'),
]

if settings.DEBUG:
    urlpatterns += static(settings.PDF_FILE_URL, document_root=settings.PDF_FILE_ROOT)