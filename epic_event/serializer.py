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
            "mobile",
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
            "sales_contact_id",
            "signed",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        client_id = self.context["request"].data["client_id"]
        client = get_object_or_404(Client, id=client_id)
        data["client"] = client
        data["sales_contact"] = self.context["request"].user
        return super().create(data)

    def update(self, instance, data):
        return super().update(instance, data)


class EventSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "client_id",
            "contract_id",
            "support_contact_id",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "date_created",
            "date_updated",
        ]

    def get_client_id(self, obj):
        client_id = obj.contract.client_id
        return client_id

    def create(self, data):

        contract_id = self.context["request"].data["contract_id"]
        contract = get_object_or_404(Contract, id=contract_id)
        if not contract.status:
            raise serializers.ValidationError(
                "You can not create an event if the contract is not signed"
            )

        data["contract"] = contract
        return super().create(data)

    def update(self, instance, data):
        return super().update(instance, data)
