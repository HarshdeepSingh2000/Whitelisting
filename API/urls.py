# urls.py
from django.urls import path
from .views import WhitelistRequestListCreateView, WhitelistRequestApproveView,index

urlpatterns = [
    path('api/whitelist/', WhitelistRequestListCreateView.as_view(), name='whitelist-request-list-create'),
    path('api/whitelist/approve/<int:pk>/', WhitelistRequestApproveView.as_view(), name='whitelist-request-approve'),
     path('', index, name='index')
]
