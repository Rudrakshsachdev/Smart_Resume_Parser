"""
URL configuration for Resume_Parser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # for handling media files
from django.conf.urls.static import static # for serving media files during development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parser_app.urls')),
]


# serve media files during development
if settings.DEBUG:
    # This will serve media files from the MEDIA_URL to the MEDIA_ROOT directory
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

