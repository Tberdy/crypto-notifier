"""crypto_notifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework_nested import routers
from rest_framework.authtoken import views
from restmanager.views import UserViewSet, AlertViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

alerts_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
alerts_router.register(r'alerts', AlertViewSet, base_name='user-alerts')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(alerts_router.urls)),
    url(r'^api/login', views.obtain_auth_token),
]
