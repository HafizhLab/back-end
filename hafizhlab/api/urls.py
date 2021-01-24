from django.urls import include, path

urlpatterns = [
    path('v1/', include('hafizhlab.api.v1.urls')),
]
