from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import User, Client, Contract
from . import serializer
from . import permissions


class ClientViewset(ModelViewSet):

    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.ClientSerializer
    permission_classes = [
        IsAuthenticated,
        permissions.IsCommercial,
        permissions.IsClientOwner,
    ]

    def get_queryset(self):
        if self.action == "update":
            client_id = self.kwargs["pk"]
            return Client.objects.fileter(id=client_id)
        return Client.objects.all()


class ContractViewset(ModelViewSet):

    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.ContractSerializer
    permission_classes = [
        IsAuthenticated,
        permissions.IsCommercial,
        permissions.IsContractOwner,
    ]

    def get_queryset(self):

        if self.action == "update":
            client_id = self.request.data["client"]
            if not (Client.objects.filter(id=client_id)):
                raise ValidationError("This client does not exist")
            contract_id = self.kwargs["pk"]
            return Contract.objects.filter(id=contract_id)
        return Contract.objects.all()
