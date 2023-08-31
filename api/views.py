from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ContactSerializer
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def contact(request):
    contact = ContactSerializer(data=request.data)

    if contact.is_valid():
        contact.save()
        content = {'message': 'contact is created'}
        return Response(content, status=status.HTTP_201_CREATED)
    else:
        return Response(status=400)
        

