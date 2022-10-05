from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Client, Contract, Event
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
                signed_contract = Contract.objects.filter(signed=True)
                signed_client = {contract.client for contract in signed_contract}
                if value == "True":
                    return Client.objects.filter(
                        id__in={client.id for client in signed_client}
                    ).order_by("id")
                else:
                    return Client.objects.exclude(
                        id__in={client.id for client in signed_client}
                    ).order_by("id")

            else:
                kwargs = {}
                for field, value in self.request.query_params.items():
                    if field in ["company_name", "email"]:
                        kwargs[field] = value
                return Client.objects.filter(**kwargs).order_by("id")
        return Client.objects.all().order_by("id")

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
        if len(self.request.query_params) > 0:
            kwargs = {}
            for field, value in self.request.query_params.items():
                if field in ["company_name", "email"]:
                    kwargs["client__" + field] = value
                elif field in ["amount", "date_created"]:
                    kwargs[field + "__gt"] = value
            return Contract.objects.filter(**kwargs).order_by("id")

        return Contract.objects.all().order_by("id")

    def get_permissions(self):
        if self.action == "create":
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
                if field in ["company_name", "email"]:
                    kwargs["contract__client__" + field] = value
                elif field in ["event_date"]:
                    kwargs[field + "__gt"] = value
            return Event.objects.filter(**kwargs).order_by("id")

        return Event.objects.all().order_by("id")

    def get_permissions(self):
        if self.action == "create":
            return self.create_permission_classes
        if self.action == "update":
            return self.update_permission_classes
        return super().get_permissions()
