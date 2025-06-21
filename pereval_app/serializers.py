from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Coords, Pereval, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']
        extra_kwargs = {
            'email': {'validators': []}
        }


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)
    level = serializers.DictField(write_only=True)

    class Meta:
        model = Pereval
        fields = '__all__'
        read_only_fields = ['status']

    def update(self, instance, validated_data):
        # обновляем координаты
        coords_data = validated_data.pop('coords', None)
        if coords_data:
            coords = instance.coords
            for attr, value in coords_data.items():
                setattr(coords, attr, value)
            coords.save()

        # обновляем картинки
        images_data = validated_data.pop('images', None)
        if images_data is not None:
            # Delete existing images
            instance.images.all().delete()
            # Create new images
            for image_data in images_data:
                Image.objects.create(pereval=instance, **image_data)

        # обновляем уровни сложности
        level_data = validated_data.pop('level', {})
        for season in ['winter', 'summer', 'autumn', 'spring']:
            if season in level_data:
                setattr(instance, season, level_data[season] if level_data[season] else None)

        # обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        level_data = validated_data.pop('level', {})
        winter = level_data.get('winter', '')
        summer = level_data.get('summer', '')
        autumn = level_data.get('autumn', '')
        spring = level_data.get('spring', '')

        try:
            user = User.objects.get(email=user_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create(**user_data)

        coords = Coords.objects.create(**coords_data)

        pereval = Pereval.objects.create(
            **validated_data,
            user=user,
            coords=coords,
            status='new',
            winter=winter if winter else None,
            summer=summer if summer else None,
            autumn=autumn if autumn else None,
            spring=spring if spring else None
        )

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval


class PerevalDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True, source='images.all')
    level = serializers.SerializerMethodField()

    class Meta:
        model = Pereval
        fields = [
            'id', 'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'status', 'user', 'coords', 'level', 'images'
        ]

    def get_level(self, obj):
        return {
            'winter': obj.winter if obj.winter else '',
            'summer': obj.summer if obj.summer else '',
            'autumn': obj.autumn if obj.autumn else '',
            'spring': obj.spring if obj.spring else ''
        }
