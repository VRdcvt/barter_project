from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('<int:pk>/update/', views.ad_update, name='ad_update'),
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('proposal/<int:pk>/<str:status>/', views.update_proposal_status, name='update_proposal_status'),
    path('proposals/', views.exchange_proposals, name='exchange_proposals'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('delete_by_id/', views.ad_delete_by_id, name='ad_delete_by_id'),
    path('edit_by_id/', views.ad_edit_by_id, name='ad_edit_by_id'),
]