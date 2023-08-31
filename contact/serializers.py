# from django.db.models import fields
from rest_framework import serializers
from contact.models import Contact
 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


    def validate_email(self, attr):
        if '@' not in attr.lower():
            raise serializers.ValidationError("Email Is Not Valid or Not Contain @ ")
        return attr
    