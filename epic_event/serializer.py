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
        client_id = self.context["request"].data["client_id"]
        client = get_object_or_404(Client, id=client_id)
        data["client"] = client
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
            "contract_id",
            "support_contact_id",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "date_created",
            "date_updated",
        ]

    def url_consistency(self):
        # the client exists?
        client_id = self.context["view"].kwargs["client_pk"]
        client = get_object_or_404(Client, id=client_id)
        # the contract exist?
        contract_id = self.context["view"].kwargs["contract_pk"]
        contract = get_object_or_404(Contract, id=contract_id)

        return client, contract

    def create(self, data):
        client, contract = self.url_consistency()
        if contract.client != client:
            raise serializers.ValidationError("It is not a contract of the client")
        data["contract"] = contract
        return super().create(data)

    def update(self, instance, data):
        _, contract = self.url_consistency()
        event_id = self.context["view"].kwargs["pk"]
        event = get_object_or_404(Event, id=event_id)
        if event.contract != contract:
            raise serializers.ValidationError("Contract and event are non consistent")
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
