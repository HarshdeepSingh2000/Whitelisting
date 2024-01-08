from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import WhitelistRequest
from .serializers import WhitelistRequestSerializer
from django.shortcuts import render,redirect,HttpResponse


class WhitelistRequestListCreateView(generics.ListCreateAPIView):
    queryset = WhitelistRequest.objects.all()
    serializer_class = WhitelistRequestSerializer

    def index(request):
        whitelist_entries =WhitelistRequest.objects.all()
        return render(request, 'index.html', {'whitelist_entries': whitelist_entries})
    
    def submit(request):
        if request.method == 'POST':
            user = request.POST.get('user')
            domain = request.POST.get('domain')
            addresses = request.POST.get('addresses')
            user = request.user

            # Create and save a WhitelistRequest instance
            whitelist_request = WhitelistRequest(user=user, domain=domain,addresses=addresses)
            whitelist_request.save()

            return redirect('http://127.0.0.1:8000/api/whitelist/')  # Redirect to the index page or wherever you want after saving

        return HttpResponse("Your request has been submitted")



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
    

    def manager_approval(request):
        if request.method == 'POST':
            action = request.POST.get('action')
            user = request.POST.get('user')
            domain = request.POST.get('domain')
            addresses = request.POST.get('addresses')

            if action == 'approve':
                user = request.user
                # Perform additional actions for manager approval here
                # For simplicity, we'll just add the entry to the WhitelistEntry model
                WhitelistRequest.objects.create( user=user,domain=domain, addresses=addresses,status="Approved")
                return redirect('index')

            elif action == 'reject':
                # Handle rejection logic (e.g., show a rejection message)
                return render(request, 'error.html', {'error_message': 'Whitelist entry rejected'})

        # If the request is not a POST request or action is not specified, render the manager approval template
        return render(request, 'manager_approval.html')


