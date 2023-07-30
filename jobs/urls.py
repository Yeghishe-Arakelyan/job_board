from django.urls import path
from . import views
app_name = 'jobs'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('<slug:slug>', views.job_detail, name='job_detail'),
    path('search/', views.search, name='search'),
	path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),

]