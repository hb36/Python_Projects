# encoding:utf-8
import django, os
from django.contrib import admin
from django.urls import include, path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
]
