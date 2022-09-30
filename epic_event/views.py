from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import User, Client, Contract, Event
from . import serializer
from .permissions import IsSalesRepresentative, IsClientOwner
from .permissions import IsContractOwner
from .permissions import IsEventOwner


class ClientViewset(ModelViewSet):

    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    create_permission_classes = [IsAuthenticated(), IsSalesRepresentative()]
    update_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsClientOwner(),
    ]

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()


class ContractViewset(ModelViewSet):

    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]
    create_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsClientOwner(),
    ]
    update_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsContractOwner(),
    ]

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()


class EventViewset(ModelViewSet):
    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    create_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsContractOwner(),
    ]
    update_permission_classes = [IsAuthenticated(), IsEventOwner()]

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()
