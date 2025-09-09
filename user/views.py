from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, PublicUserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .models import User
from .serializers import PublicUserSerializer


#Registration View
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        data=PublicUserSerializer(user).data
        return Response({"message": "Registered", "user": data},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"]
    )

    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": PublicUserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])  
def profile(request):
    user = request.user
    serializer = PublicUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    user = request.user
    qs = User.objects.exclude(id=user.id)  # exclude self

    # Extract filters from query params
    params = request.query_params
    gender   = params.get("gender")
    nation   = params.get("nation")
    state    = params.get("state")
    city     = params.get("city")
    district = params.get("district")
    mandal   = params.get("mandal")
    village  = params.get("village")
    pincode  = params.get("pincode")

    # Apply filters (priority: gender > nation > state > city > district > mandal > village > pincode)
    if gender:
        qs = qs.filter(gender=gender)
    if nation:
        qs = qs.filter(nation=nation)
    if state:
        qs = qs.filter(state=state)
    if city:
        qs = qs.filter(city=city)
    if district:
        qs = qs.filter(district=district)
    if mandal:
        qs = qs.filter(mandal=mandal)
    if village:
        qs = qs.filter(village=village)
    if pincode:
        qs = qs.filter(pincode=pincode)

    serializer = PublicUserSerializer(qs, many=True)
    return Response(serializer.data)