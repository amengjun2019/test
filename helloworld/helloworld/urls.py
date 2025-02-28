"""
URL configuration for helloworld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views
# from .views import my_json_view, MyJsonView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path("", views.hello, name="hello"),
    path('json-example/', views.my_json_view, name='json_example'),
    path('json-post/', views.json_post, name='jsonpost'),
    path('json-class-example/', views.MyJsonView.as_view(), name='json_class_example'),
    path('captcha/',views.get_code),
    path('query-llm/',views.query),
    path('query-csrf/',views.get_csrf_token),
    path("llm-stream/", views.llm_stream_view, name="llm_stream"),
    path('query-stream-llm/',views.query_stream),
]
