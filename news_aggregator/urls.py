# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('news.urls')),  # Include URLs from the news app
#     path('users/', include('users.urls')),  # Include URLs from the users app
# ]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls', namespace='news')),  # Include with namespace
    path('accounts/', include('accounts.urls', namespace='accounts')),  # Add accounts URLs with namespace
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
