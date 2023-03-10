from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnlyOrAdmin


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyOrAdmin]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnlyOrAdmin()]
        return []

    def get_queryset(self):
        user = self.request.user.id
        return Advertisement.objects.filter(Q(status__in=('OPEN', 'CLOSED')) | Q(status='DRAFT', creator=user))

    @action(detail=True, methods=['PATCH'], name='add_bookmark', url_path='add-bookmark',
            url_name='add-bookmark')
    def add_bookmark(self, request, pk=None):
        user = request.user
        if user != Advertisement.objects.get(id=pk).creator:
            user.favourites.add(Advertisement.objects.get(id=pk))
            return Response("OK", status=status.HTTP_200_OK)
        else:
            raise ValueError('error')

    @action(detail=False, methods=['GET'], name='bookmarks_list', url_path='bookmarks-list',
            url_name='bookmarks-list')
    def bookmarks_list(self, request):
        if request.user.is_authenticated:
            queryset = Advertisement.objects.filter(favourites=request.user)
        else:
            raise ValueError('error')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)