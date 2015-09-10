__author__ = 'vitaly'

from rest_framework import generics

from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import PersonSerializer, AccountSerializer, AccountCreateSerializer
from .models import Person, PersonAccount


class PersonView(generics.CreateAPIView):

    serializer_class = PersonSerializer


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PersonSerializer

    queryset = Person.objects.all()



@api_view(['POST'])
def set_image(request, pk, account_pk):

    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response({"status": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        account = person.accounts.get(pk=account_pk)
    except PersonAccount.DoesNotExist:
        return Response({"status": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    account.set_use_image()
    account.save()

    return Response({"status": True})

class AccountDetailView(generics.DestroyAPIView):

    serializer_class = AccountSerializer

    lookup_url_kwarg = 'account_pk'

    def get_queryset(self):

        person_pk = self.kwargs.get('pk')

        return Person.objects.get(pk=person_pk).accounts.all()

    def perform_destroy(self, instance):

        account = self.get_object()

        from .core_functions import remove_user_posts
        remove_user_posts(account.type, account.person.pk, account.social_id)

        instance.delete()


class AccountListView(generics.CreateAPIView):

    serializer_class = AccountCreateSerializer

    def create(self, request, *args, **kwargs):


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        link = serializer.validated_data.get('link')

        from .core_functions import fetch_link
        account = fetch_link(link)

        if not account:
            return Response({"detail": "Unable to process link"}, status=status.HTTP_400_BAD_REQUEST)

        account['person'] = self.kwargs.get('pk')

        serializer2 = AccountSerializer(data=account)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer2.data, status=status.HTTP_201_CREATED, headers=headers)