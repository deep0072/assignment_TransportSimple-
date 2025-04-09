# qa_app/serializers.py
from rest_framework import serializers
from .models import UserModel






class UserSerializer(serializers.ModelSerializer):
    """ Serializer for displaying basic user information (read-only contexts) """
    class Meta:
        model = UserModel
      
        fields = ['id', 'username', 'email', 'phone_number'] 

class RegisterSerializer(serializers.ModelSerializer):
    """ Serializer for user registration """

    password = serializers.CharField(
        write_only=True, required=True
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = UserModel
     
        fields = ['email', 'username', 'phone_number', 'password', 'password2']
        extra_kwargs = {
           
            'username': {'required': True},
            'phone_number': {'required': True},
        }

    def validate(self, attrs):
        """ Check that the two password entries match """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
       
        return attrs

    def create(self, validated_data):
        """ Create and return a new user using the custom manager """

        validated_data.pop('password2')
       
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
