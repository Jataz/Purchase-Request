from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'), 
    path('logout/', views.user_logout_view, name='logout'),
    
    path('dashboard/', views.index ,name='dashboard'),
    
    path('create_purchase_request/', views.create_purchase_request, name='create_purchase_request'),
    path('purchase_request/<int:pk>/', views.purchase_request_detail, name='purchase_request_detail'),
    path('purchase_request/update/<int:pk>/', views.update_purchase_request, name='update_purchase_request'),
    path('purchase_request/delete/<int:pk>/', views.delete_purchase_request, name='delete_purchase_request'),
    path('purchase_requests/', views.user_purchase_requests, name='purchase_requests'),
    
    path('pending_requests/', views.admin_pending_requests, name='pending_requests'),
    path('review_purchase_request/<int:pk>/', views.review_purchase_request, name='review_purchase_request'),
    
    path('purchase_orders/', views.purchase_order_list, name='purchase_orders'),
    path('purchase_order/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase_order/update/<int:pk>/', views.update_purchase_order, name='update_purchase_order'),
    path('purchase_order/delete/<int:pk>/', views.delete_purchase_order, name='delete_purchase_order'),
    


]
