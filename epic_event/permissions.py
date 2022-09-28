from rest_framework.permissions import BasePermission
from .models import Client


class IsCommercial(BasePermission):
    message = "You must be a commercial to access this feature"

    def has_permission(self, request, view):
        return "Sales" == str(request.user.groups.all().first())


class IsClientOwner(BasePermission):
    message = "it's not your client"

    def has_object_permission(self, request, view, obj):
        return obj.sales_contact == request.user


class IsContractOwner(BasePermission):
    message = "it's not your client"

    def has_object_permission(self, request, view, obj):
        return obj.sales_contact == request.user


class IsSupport(BasePermission):
    message = "You must be support to access this feature"

    def has_permission(self, request, view):
        return "Support" == str(request.user.groups.all().first())
