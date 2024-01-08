# urls.py
from django.urls import path
from .views import WhitelistRequestListCreateView, WhitelistRequestApproveView

urlpatterns = [
    path('api/whitelist/', WhitelistRequestListCreateView.as_view(), name='whitelist-request-list-create'),
    path('api/whitelist/frontend', WhitelistRequestListCreateView.index, name='whitelist-request-list-create'),
    path('api/whitelist/approve/', WhitelistRequestApproveView.manager_approval, name='whitelist-request-approve'),
     path('api/whitelist/submit/',WhitelistRequestListCreateView.submit, name='whitelist-request-submit'),
]
