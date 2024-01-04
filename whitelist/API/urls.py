# urls.py
from django.urls import path
from .views import WhitelistRequestListCreateView, WhitelistRequestApproveView

urlpatterns = [
    path('api/whitelist/', WhitelistRequestListCreateView.as_view(), name='whitelist-request-list-create'),
    path('api/whitelist/approve/<int:pk>/', WhitelistRequestApproveView.as_view(), name='whitelist-request-approve'),
]
