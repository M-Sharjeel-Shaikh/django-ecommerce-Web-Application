from django.db.models import fields
from rest_framework import serializers
from customer.models import *
 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_email(self, attr):
        if '@' not in attr.lower():
            raise serializers.ValidationError("Email Is Not Valid or Not Contain @ ")
        return attr
    