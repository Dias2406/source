"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from personal.views import (
    home_screen_view,

)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('home/', home_screen_view, name="home"),
    path('', home_screen_view, name="home"),
    path('account/', account_view, name="account"),
    path('student/', include('student.urls', 'student'), name = "student"),
    path('tracking/', include('teacher.urls', 'tracking'), name="teacher"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

