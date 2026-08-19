from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Buyurtma, Item
from .serializers import (
    BuyurtmaSerializer,
    ItemSerializer,
    LoginSerializer,
    RegisterSerializer,
    UstaSerializer,
)


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            profile = getattr(user, "profile", None)

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Tizimga muvaffaqiyatli kirdingiz",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "rol": profile.rol if profile else "mijoz",
                        "avatar": profile.rasm.url if profile and profile.rasm else None,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UstaListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UstaSerializer

    def get_queryset(self):
        return User.objects.filter(profile__rol="usta").select_related("profile")


class UstaDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UstaSerializer
    queryset = (
        User.objects.filter(profile__rol="usta")
        .select_related("profile")
        .prefetch_related("profile__portfolio")
    )


# --- BUYURTMALAR QISMI ---

class MijozBuyurtmaView(generics.ListCreateAPIView):
    serializer_class = BuyurtmaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MijozBuyurtmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuyurtmaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(user=self.request.user)


class UstaBuyurtmaListView(generics.ListAPIView):
    serializer_class = BuyurtmaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(usta=self.request.user)


class UstaBuyurtmaDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BuyurtmaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(usta=self.request.user)

from rest_framework import viewsets, permissions
from .models import Buyurtma
from .serializers import BuyurtmaSerializer

class BuyurtmaViewSet(viewsets.ModelViewSet):
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Agar foydalanuvchi usta bo'lsa, unga kelgan buyurtmalar, mijoz bo'lsa o'zi bergan buyurtmalar chiqadi
        if hasattr(user, 'profile') and user.profile.rol == 'usta':
            return Buyurtma.objects.filter(usta=user).order_by('-yaratilgan_vaqt')
        return Buyurtma.objects.filter(user=user).order_by('-yaratilgan_vaqt')

    def perform_create(self, serializer):
        # Buyurtma yaratishda avtomatik ravishda hozirgi kirgan foydalanuvchi user qilib belgilanadi
        serializer.save(user=self.request.user)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Agar Buyurtma modulingiz bo'lsa import qiling (masalan: Order yoki Buyurtma)
# from .models import Buyurtma 

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def statistika_view(request):
    mijozlar_soni = User.objects.filter(profile__rol='mijoz').count()
    ustalar_soni = User.objects.filter(profile__rol='usta').count()
    tugatilgan_ishlar = Buyurtma.objects.filter(status='bajarildi').count() if hasattr(Buyurtma, 'status') else Buyurtma.objects.count()

    return Response({
        "mijozlar": mijozlar_soni,
        "ustalar": ustalar_soni,
        "tugatilgan_ishlar": tugatilgan_ishlar,
        "mamnunlik": "98%"
    })

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def stats_view(request):
    mijozlar_soni = User.objects.filter(rol='mijoz').count()
    ustalar_soni = User.objects.filter(rol='usta').count()
    
    return Response({
        'mijozlar_soni': mijozlar_soni,
        'ustalar_soni': ustalar_soni,
    })