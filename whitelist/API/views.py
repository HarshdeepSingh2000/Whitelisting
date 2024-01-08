from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import WhitelistRequest
from rest_framework.permissions import IsAuthenticated
from .serializers import WhitelistRequestSerializer
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator

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

            # Create and save a WhitelistRequest instance
            whitelist_request = WhitelistRequest(user_name=user_name, domain=domain,addresses=addresses)
            whitelist_request.save()

            return redirect('http://127.0.0.1:8000/api/whitelist/submit/')  # Redirect to the index page or wherever you want after saving

        return HttpResponse("Your request has been submitted")



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


def is_manager(user):
    # Replace this with your logic to check if the user is a manager
    return user.is_authenticated and user.is_manager

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_manager), name='dispatch')
class WhitelistRequestApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer
    permission_classes = [IsAdminOrReadOnly]
    def manager_approval(request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                action = request.POST.get('action')
                domain = request.POST.get('domain')
                ip_address = request.POST.get('ip_address')
                approver_token = Token.objects.get()
                print(approver_token)


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

            
            return render(request, 'manager_approval.html')
        else:
            return HttpResponse("User is not autheticated")