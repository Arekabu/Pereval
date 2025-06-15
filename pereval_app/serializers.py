from rest_framework import serializers
from .models import User, Coords, Level, Pereval, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')
        level_data = {
            'winter': validated_data.pop('winter', None),
            'summer': validated_data.pop('summer', None),
            'autumn': validated_data.pop('autumn', None),
            'spring': validated_data.pop('spring', None),
        }

        user = User.objects.create(**user_data)

        coords = Coords.objects.create(**coords_data)

        pereval = Pereval.objects.create(
            **validated_data,
            user=user,
            coords=coords,
            status='new',  # Устанавливаем статус 'new'
            winter=Level.objects.get(name=level_data['winter']) if level_data['winter'] else None,
            summer=Level.objects.get(name=level_data['summer']) if level_data['summer'] else None,
            autumn=Level.objects.get(name=level_data['autumn']) if level_data['autumn'] else None,
            spring=Level.objects.get(name=level_data['spring']) if level_data['spring'] else None,
        )

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval