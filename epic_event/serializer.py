from rest_framework import serializers
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
            "client",
            "status",
            "amount",
            "payment_due",
            "date_created",
            "date_updated",
        ]

    def create(self, data):
        data["sales_contact"] = self.context["request"].user
        data["status"] = True
        return super().create(data)

    def update(self, instance, data):
        print("ouf")
        return super().update(instance, data)

    def validate_client(self, value):

        if value.sales_contact != self.context["request"].user:
            raise serializers.ValidationError(
                "You can not create a contract for a client who is not yours"
            )
        return value
