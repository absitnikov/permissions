from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )
    favourites = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'favourites')
        read_only_fields = ['favourites', ]

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if data.get('status') not in ('CLOSED', 'DRAFT') and Advertisement.objects.filter(
                creator=self.context['request'].user.id,
                status='OPEN').count() > 10:
            raise ValueError('У вас больше 10 открытых объявлений')
        return data
