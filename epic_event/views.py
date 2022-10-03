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

    permission_classes = [IsAuthenticated]
    create_permission_classes = [IsAuthenticated(), IsSalesRepresentative()]
    update_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsClientOwner(),
    ]

    def get_queryset(self):
        if len(self.request.query_params) > 0:
            if (
                len(self.request.query_params) == 1
                and "client" in self.request.query_params
            ):  # list of the clients or of the prospects
                value = self.request.query_params["client"]
                signed_contract = Contract.objects.filter(status=True)
                signed_client = {contract.client for contract in signed_contract}
                if value == "True":
                    return Client.objects.filter(
                        id__in={client.id for client in signed_client}
                    )
                else:
                    return Client.objects.exclude(
                        id__in={client.id for client in signed_client}
                    )

            else:
                kwargs = {}
                for field, value in self.request.query_params.items():
                    if field in ["last_name", "email"]:
                        kwargs[field] = value
                return Client.objects.filter(**kwargs)
        return Client.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()


class ContractViewset(ModelViewSet):

    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.ContractSerializer
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

    def get_queryset(self):
        print("query")
        if len(self.request.query_params) > 0:
            kwargs = {}
            for field, value in self.request.query_params.items():
                if field in ["last_name", "email"]:
                    kwargs["client__" + field] = value
                elif field in ["amount", "date_created"]:
                    kwargs[field + "__gt"] = value
            return Contract.objects.filter(**kwargs)

        return Contract.objects.all()

    def get_permissions(self):
        if self.action == "create":
            print("permission")
            print(self.request)
            print(self.kwargs)
            print(dir(self))
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()


class EventViewset(ModelViewSet):
    http_method_names = ["post", "get", "put"]
    serializer_class = serializer.EventSerializer
    permission_classes = [IsAuthenticated]
    create_permission_classes = [
        IsAuthenticated(),
        IsSalesRepresentative(),
        IsContractOwner(),
    ]
    update_permission_classes = [IsAuthenticated(), IsEventOwner()]

    def get_queryset(self):
        if len(self.request.query_params) > 0:
            kwargs = {}
            for field, value in self.request.query_params.items():
                if field in ["last_name", "email"]:
                    kwargs["contract__client__" + field] = value
                elif field in ["date_created"]:
                    kwargs[field + "__gt"] = value
            return Event.objects.filter(**kwargs)

        return Event.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()
