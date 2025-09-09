from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User



class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "username", "gender",
            "nation", "state", "city", "district", "mandal", "village", "pincode","profile_picture"]
        

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[validate_password]) 
    re_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username", "email", "mobile",
            "password", "re_password",
            "gender",
            "nation", "state", "city", "district", "mandal", "village", "pincode","profile_picture"]
    def validate(self,attrs):
        if attrs.get("password")!=attrs.get("re_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    def create(self,validate_data):
        validate_data.pop("re_password")
        return User.objects.create_user(**validate_data)
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)