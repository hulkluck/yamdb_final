import datetime as dt
# import uuid

from django.core import validators
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import (CHOICES, Category, Comment, Genre, Review, Title,
                            User)


class ErrorResponse:
    NOT_ALLOWED = 'Отзыв уже есть.'
    FORBIDDEN_NAME = 'Это имя невозможно использовать!'
    INCORRECT_RELEASE_YEAR = 'Нельзя использовать год больше текущего'
    INCORRECT_GENRE = 'В списке нет такого жанра'
    INCORRECT_CATEGORY = 'Данной категории нет в списке'
    MISSING_EMAIL = 'Необходимо ввести электронную почту'
    MISSING_USERNAME = 'Введите имя пользователя'
    MISSING_CODE = 'Введите код подтверждения'
    USERNAME_EXISTS = 'Такой пользователь уже существует'
    EMAIL_EXISTS = 'Такой адрес электронной почты уже зарегестрирован'


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User

    # def create(self, validated_data):
    #     email = validated_data['email']
    #     confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
    #     user = User.objects.create(
    #         **validated_data,
    #         confirmation_code=confirmation_code
    #     )
    #     return user

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(ErrorResponse.FORBIDDEN_NAME)
        elif not name:
            raise serializers.ValidationError(ErrorResponse.MISSING_USERNAME)
        return name

    def validate_email(self, email):
        try:
            validators.validate_email(email)
        except serializers.ValidationError:
            raise serializers.ValidationError(ErrorResponse.MISSING_EMAIL)
        else:
            return email


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(ErrorResponse.FORBIDDEN_NAME)
        return name

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
                User.objects.filter(username=username).exists()
                and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(ErrorResponse.USERNAME_EXISTS)
        if (
                User.objects.filter(email=email).exists()
                and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(ErrorResponse.EMAIL_EXISTS)
        return data


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_USERNAME)
        if confirmation_code is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_CODE)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = GenreField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_RELEASE_YEAR
            )
        return value

    def validate_genre(self, value):
        for item in value:
            if not Genre.objects.filter(name=item.name).exists():
                raise serializers.ValidationError(
                    ErrorResponse.INCORRECT_GENRE
                )
        return value

    def validate_category(self, value):
        if not Category.objects.filter(name=value.name).exists():
            raise serializers.ValidationError(ErrorResponse.INCORRECT_CATEGORY)
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        required=False
    )
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                    author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError(ErrorResponse.NOT_ALLOWED)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=['author', 'text']
            )
        ]
