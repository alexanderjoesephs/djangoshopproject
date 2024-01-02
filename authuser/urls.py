from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout',views.logoutview, name='logout'),
    path('createaccount', views.createaccount, name='createaccount'),
    path('<int:id>', views.productview, name="productview"),
    path('checkout', views.checkout, name="checkout"),
    path('league=<str:league>', views.leaguerange, name="range"),
    path('timerange', views.timerange, name="timerange"),
    path('your_orders',views.your_orders, name="your_orders"),
    path('review', views.review, name='review')
]