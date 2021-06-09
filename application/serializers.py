from django.contrib.auth import get_user_model
from django.db.models.fields import EmailField
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import password_validation as validators
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
         read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password','first_name' ,'last_name','location')
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, data):

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateUserSerializer, self).validate(data)
     
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data['email'],
            location=validated_data['location'],
            password=make_password(validated_data['password'], salt=None, hasher='default')
        )
        return user
       