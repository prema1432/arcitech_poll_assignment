from django.urls import path

from poll import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_poll/', views.create_poll, name='create_poll'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),

]