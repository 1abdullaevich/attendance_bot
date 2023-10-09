from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    student_full_name = serializers.SerializerMethodField()

    def get_student_full_name(self, obj):
        return obj.student.full_name

    class Meta:
        model = AttendanceModel
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = '__all__'
