from rest_framework import serializers
from .models import User
from .models import StudentAchievement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role", "linked_student_id"]


class StudentAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAchievement
        fields = "__all__"
