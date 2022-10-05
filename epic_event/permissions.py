from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Client, Contract


class IsSalesRepresentative(BasePermission):
    message = "You must be a sales representative to access this feature"

    def has_permission(self, request, view):
        return "Sales" == str(request.user.groups.all().first())


class IsClientOwner(BasePermission):
    message = "it's not your client"

    def has_permission(self, request, view):
        if "pk" in view.kwargs:  # call from ContractViewSet
            client_id = view.kwargs["pk"]
        else:  # call from ClientViewSet

            client_id = request.data["client_id"]

        client = get_object_or_404(Client, id=client_id)
        return client.sales_contact == request.user


class IsContractOwner(BasePermission):
    message = "it's not your client"

    def has_permission(self, request, view):
        if "pk" in view.kwargs:
            contract_id = view.kwargs["pk"]
        else:
            contract_id = request.data["contract_id"]
        contract = get_object_or_404(Contract, id=contract_id)
        return contract.sales_contact == request.user


class IsEventOwner(BasePermission):
    message = "You must be the sales representative or the support of this event"

    def has_object_permission(self, request, view, obj):
        sales_representative = Contract.objects.get(id=obj.contract_id).sales_contact
        support = obj.support_contact
        return request.user in [support, sales_representative]
