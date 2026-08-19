from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import Buyurtma, Item, Portfolio, Profile

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = Item
        fields = "__all__"


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["id", "rasm"]


class ProfileSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    avatar = serializers.ImageField(required=False, allow_null=True, write_only=True)
    telefon = serializers.CharField(write_only=True, required=False, allow_blank=True)
    rol = serializers.CharField(write_only=True, required=False, allow_blank=True, default="mijoz")
    viloyat = serializers.CharField(write_only=True, required=False, allow_blank=True)
    shahar = serializers.CharField(write_only=True, required=False, allow_blank=True)
    haqida = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tajriba = serializers.IntegerField(write_only=True, required=False, default=0)
    kategoriya = serializers.CharField(write_only=True, required=False, allow_blank=True)
    konikma = serializers.CharField(write_only=True, required=False, allow_blank=True)
    vaqt = serializers.CharField(write_only=True, required=False, allow_blank=True)
    narx = serializers.IntegerField(write_only=True, required=False, default=0)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "telefon",
            "rol",
            "viloyat",
            "shahar",
            "haqida",
            "tajriba",
            "kategoriya",
            "konikma",
            "vaqt",
            "narx",
        ]

    def create(self, validated_data):
        avatar = validated_data.pop("avatar", None)
        telefon = validated_data.pop("telefon", "")
        rol = validated_data.pop("rol", "mijoz")
        viloyat = validated_data.pop("viloyat", "")
        shahar = validated_data.pop("shahar", "")
        haqida = validated_data.pop("haqida", "")
        tajriba = validated_data.pop("tajriba", 0)
        kategoriya = validated_data.pop("kategoriya", "")
        konikma = validated_data.pop("konikma", "")
        vaqt = validated_data.pop("vaqt", "")
        narx = validated_data.pop("narx", 0)

        # Foydalanuvchi yaratish
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        # Profil yaratish yoki mavjud bo'lsa yangilash
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "rasm": avatar,
                "telefon": telefon,
                "rol": rol,
                "viloyat": viloyat,
                "shahar": shahar,
                "haqida": haqida,
                "tajriba": tajriba,
                "kategoriya": kategoriya,
                "konikma": konikma,
                "vaqt": vaqt,
                "narx": narx,
            },
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        if username_or_email and password:
            username = username_or_email

            if "@" in username_or_email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        "Ushbu email bilan ro'yxatdan o'tgan foydalanuvchi topilmadi."
                    )

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Kiritilgan ma'lumotlar yoki parol noto'g'ri.")
        else:
            raise serializers.ValidationError("Email/Username va parol kiritilishi shart.")

        attrs["user"] = user
        return attrs


class UstaSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    ism = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "profile", "ism"]

    def get_ism(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name if full_name else obj.username


class UstaDetailSerializer(serializers.ModelSerializer):
    ism = serializers.SerializerMethodField()
    rasm = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "ism", "first_name", "last_name", "rasm"]

    def get_ism(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        if full_name:
            return full_name
        return getattr(obj, "ism", None) or obj.username

    def get_rasm(self, obj):
        if hasattr(obj, "profile") and getattr(obj.profile, "rasm", None):
            return obj.profile.rasm.url if hasattr(obj.profile.rasm, "url") else str(obj.profile.rasm)
        return None


class BuyurtmaUserSerializer(serializers.ModelSerializer):
    rasm = serializers.ImageField(source="profile.rasm", read_only=True)
    viloyat = serializers.CharField(source="profile.viloyat", read_only=True)
    shahar = serializers.CharField(source="profile.shahar", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "rasm", "viloyat", "shahar"]


class BuyurtmaSerializer(serializers.ModelSerializer):
    user = BuyurtmaUserSerializer(read_only=True)
    usta_details = BuyurtmaUserSerializer(source="usta", read_only=True)

    class Meta:
        model = Buyurtma
        fields = [
            "id",
            "user",
            "usta",
            "usta_details",
            "xizmat_turi",
            "sana",
            "vaqt",
            "manzil",
            "izoh",
            "status",
            "yaratilgan_vaqt",
        ]
        read_only_fields = ["id", "user", "yaratilgan_vaqt"]