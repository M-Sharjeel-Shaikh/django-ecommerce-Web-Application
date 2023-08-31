
from django.db.models import fields
from rest_framework import serializers
from contact.models import Contact
 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


    def validate_email(self, value):
        a = value
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

    