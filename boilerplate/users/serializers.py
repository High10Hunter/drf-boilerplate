import re
from rest_framework import serializers

from boilerplate.roles.serializers import RoleSerializer
from boilerplate.users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "role", "password")

    def validate(self, args):
        email = args.get("email", None)
        if User.objects.filter(email__icontains=email).exists():
            raise serializers.ValidationError({"email": "email already taken"})

        password = args.get("password", None)
        if password is not None:
            pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
            result = re.match(pattern, password)

            if result is None:
                raise serializers.ValidationError(
                    {
                        "password": "Password must be at least 8 characters long, include at least one number, one letter, and one special character."
                    }
                )

        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "role",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"password": {"write_only": True}}
