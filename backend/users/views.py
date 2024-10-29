from api.paginators import CustomHomePagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import MyUser, SubscriptionUser
from .serializers import (UserGetSubscribeSerializer,
                          UserPostDelSubscribeSerializer, UserSerializer)


class MyUserViewSet(UserViewSet):
    """Вьюсет для модели User."""

    serializer_class = UserSerializer
    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_context_data(self):
        context = super().get_context_data()
        context['request'] = self.request
        return context

    @action(
        detail=False,
        methods=('get'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('get', 'put', 'delete',),
        permission_classes=(IsAuthenticated,),
    )
    def avatar(self, request, id=None):
        return Response(UserSerializer(request.user).data['avatar'])

    @action(
            detail=False,
            permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = MyUser.objects.filter(following__username=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserGetSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(MyUser, pk=id)

        if request.method == 'POST':
            serializer = UserGetSubscribeSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            SubscriptionUser.objects.create(username=user, author=author)
            return Response(serializer.data)

        if request.method == 'DELETE':
            get_object_or_404(
                SubscriptionUser, username=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
