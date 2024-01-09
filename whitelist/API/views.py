from rest_framework import generics, permissions, status
from .models import WhitelistRequest
from rest_framework.permissions import IsAuthenticated
from .serializers import WhitelistRequestSerializer
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.views import View
from django.shortcuts import render

class WhitelistRequestListCreateView(generics.ListCreateAPIView):
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer

    def index(request):
        whitelist_entries =WhitelistRequest.objects.all()
        return render(request, 'index.html', {'whitelist_entries': whitelist_entries})
    
    def submit(request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name')
            domain = request.POST.get('domain')
            addresses = request.POST.get('addresses')


            whitelist_request = WhitelistRequest(user_name=user_name, domain=domain,addresses=addresses)
            whitelist_request.save()

            return redirect('http://127.0.0.1:8000/api/whitelist/submit/')  # Redirect to the index page or wherever you want after saving

        return HttpResponse("Your request has been submitted")



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class WhitelistRequestApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def manager_approval(request):
            model_data = WhitelistRequest.objects.all()
            if request.method == 'POST':
                
                action = request.POST.get('action')
                domain = request.POST.get('domain')
                ip_address = request.POST.get('ip_address')


                if action == 'approve':

                    whitelist_request = get_object_or_404(WhitelistRequest, domain=domain, addresses=ip_address)

                    whitelist_request.status = "Approved"
                    whitelist_request.save()

                    return HttpResponse("<h4>Your request has been Approved</h4>")

                elif action == 'reject':
                    whitelist_request = get_object_or_404(WhitelistRequest, domain=domain, addresses=ip_address)

                    whitelist_request.status = "Rejected"
                    whitelist_request.save()
                    return render(request, 'error.html', {'error_message': 'Whitelist entry rejected'})

            
            return render(request, 'manager_approval.html',{'model_data': model_data})
        