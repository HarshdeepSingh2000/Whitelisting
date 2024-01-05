from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import WhitelistRequest
from .serializers import WhitelistRequestSerializer
from django.shortcuts import render




def index(request):
    whitelist_entries =WhitelistRequest.objects.all()
    return render(request, 'index.html', {'whitelist_entries': whitelist_entries})
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class WhitelistRequestListCreateView(generics.ListCreateAPIView):
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class WhitelistRequestApproveView(generics.UpdateAPIView):
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'approved'
        instance.save()

        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
