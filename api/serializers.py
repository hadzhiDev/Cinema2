from rest_framework import serializers
from django.contrib.auth.models import User

from apps.models import Genre, Movie, Director


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def create(self, validated_data):
        return super().create(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = GenreSerializer(many=True)
    author = serializers.CharField(source='author.email')
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user_id = serializers.IntegerField(source='author.id')

    class Meta:
        model = Movie
        fields = '__all__'


class AddUpdateMovieSerializer(serializers.ModelSerializer):

    # image = serializers.ImageField()
 
    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        return super().create(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

