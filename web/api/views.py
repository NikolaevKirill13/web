import jwt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.views import APIView
from rest_framework import status

from . import serializers
from core.models import Faq, Block, User, Poll
from api.serializers import UserWrite, BlockWrite, PollWrite, FaqSerializer




@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'faq': 'api/faq - просмотр всех тем справки, добавление справки',
        'faq detail': 'api/faq/title - просмотр и редактирование справки',
        'member list': 'api/user - просмотр всех юзеров, добавление и редактирование юзеров'
                       'обязательные поля: username и user_id_tg',
        'member detail': 'api/user/user_id - просмотр и редактирование юзера',
        'block list': 'api/block - просмотр списка заблокированных юзеров',
        'block detail': 'api/block/user_id - блокирование юзеров, обязательное поле: user',
        'poll': 'api/poll - просмотр и сохранение голосовалок, для добавления методом post отправить "keyboard_id:<int>, "user_id: <int>',
        'poll detail': 'api/poll/<keyboard_id> - просмотр конкретной голосовалки'
    }
    return Response(api_urls)


#class FaqList(generics.ListCreateAPIView):
#    permission_classes = (IsAuthenticated,)
#    queryset = Faq.objects.all()
#    serializer_class = serializers.FaqSerializer


class FaqDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faq.objects.all()
    serializer_class = serializers.FaqSerializer
    lookup_field = 'title'


class FaqList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Faq.objects.all()
        serializer_class = FaqSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FaqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockWriteList(APIView):
    def get(self, request):
        queryset = Block.objects.all()
        block_list = BlockWrite(queryset, many=True)
        return Response(block_list.data)

    def post(self, request):
        serializer = BlockWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockWriteDetail(APIView):
    def get(self, request, user):
        queryset = Block.objects.get(user=user)
        block = BlockWrite(queryset)
        return Response(block.data, status=status.HTTP_200_OK)


class UserWriteList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer_for_queryset = UserWrite(queryset, many=True)
        return Response(serializer_for_queryset.data)

    def post(self, request):
        serializer = UserWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserWriteDetail(APIView):
    def get(self, request, user_id_tg):
        queryset = User.objects.get(user_id_tg=user_id_tg)
        user = UserWrite(queryset)
        return Response(user.data, status=status.HTTP_200_OK)


class PollWriteList(APIView):
    def get(self, request):
        queryset = Poll.objects.all()
        serializer_for_queryset = PollWrite(queryset, many=True)
        return Response(serializer_for_queryset.data)

    def post(self, request):
        serializer = PollWrite(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollDetailList(APIView):
    def get(self, request, keyboard_id):
        queryset = Poll.objects.filter(keyboard_id=keyboard_id)
        serializer_class = serializers.PollWrite(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_bot(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=username)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {'username': user.username, 'token': token}
                #user_logged_in.send(sender=user.__class__,
                #                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
    except KeyError:
        res = {'error': 'HTTP_511_NETWORK_AUTHENTICATION_REQUIRED'}
        return Response(res, status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

