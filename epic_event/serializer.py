from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "company_name",
            "sales_contact",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        data["sales_contact"] = self.context["request"].user
        return super().create(data)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "client_id",
            "sales_contact",
            "status",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        id_client = self.context["view"].kwargs["client_pk"]
        data["client"] = get_object_or_404(Client, id=id_client)
        data["sales_contact"] = self.context["request"].user
        return super().create(data)

    def update(self, instance, data):
        print("ouf")
        return super().update(instance, data)

    def validate_client(self, value):
        print("validate")
        if value.sales_contact != self.context["request"].user:
            raise serializers.ValidationError(
                "You can not create/update a contract for a client who is not yours"
            )
        return value


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "contract",
            "support_contact",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        # The field support_contact cannot be create here
        if "support_contact" in data:
            data.pop("support_contact")
        return super().create(data)

    def update(self, instance, data):
        # fields contract and support_contact cannot be changed
        data["contract"] = instance.contract
        data["support_contact"] = instance.support_contact
        return super().update(instance, data)

    def validate_contract(self, value):
        if value.sales_contact != self.context["request"].user:
            raise serializers.ValidationError(
                "You can not create an event for a client who is not yours"
            )
        if not value.status:
            raise serializers.ValidationError(
                "You can not create an event if the contract is not signed"
            )
        return value
