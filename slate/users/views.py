from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import StudentAchievement
from rest_framework.generics import ListAPIView
from .serializers import StudentAchievementSerializer, UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import User, StudentAchievement

User = get_user_model()  # Ensure you're using the correct User model


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password").encode('utf-8')  # Convert input password to bytes
        role = request.data.get("role")

        if not email or not password or not role:
            return Response({"error": "Email, password, and role are required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        stored_password = user.password.encode('utf-8')  # Convert stored hash to bytes

        # Check if the password matches the stored hash
        if not bcrypt.checkpw(password, stored_password):  
            return Response({"error": "Invalid credentials"}, status=400)

        if user.role != role:
            return Response({"error": "Role mismatch"}, status=400)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password").encode('utf-8')  # Convert password to bytes
        role = request.data.get("role")

        if not email or not password or not role:
            return Response({"error": "All fields are required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        # Hash the password with bcrypt before storing
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        # Create user with hashed password
        if(role == "parent"):
            linked_student_id = request.data.get("linked_student_id")
            user = User.objects.create(email=email, password=hashed_password, role=role, linked_student_id=linked_student_id)
        else:
            user = User.objects.create(email=email, password=hashed_password, role=role)
        
        return Response({"message": "User created successfully"})


class StudentAchievementView(ListAPIView):
    serializer_class = StudentAchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in  ["parent"]:
            return StudentAchievement.objects.filter(student_id=user.linked_student_id)
        elif user.role == "student":
            return StudentAchievement.objects.filter(student_id=user.id)
        elif user.role == "school":
            return StudentAchievement.objects.all()
        return StudentAchievement.objects.none()

    def post(self, request):
        user = request.user
        if user.role != "school":
            return Response({"error": "Permission denied"}, status=403)

        student_id = request.data.get("student_id")
        if not student_id:
            return Response({"error": "Student ID is required"}, status=400)

        # Ensure student exists
        if not User.objects.filter(id=student_id).exists():
            return Response({"error": "Student not found"}, status=404)

        serializer = StudentAchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Achievement added successfully", "data": serializer.data}, status=201) 

        return Response(serializer.errors, status=400)