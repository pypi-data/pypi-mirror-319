from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'user/', views.UserViewSet.as_view({"get": "list", "post": "create"}), name="User List"),
    re_path(r'^user/(?P<pk>\d+)/$', views.UserViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name="User List __1"),
]
