from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
import datetime


class GroupListView(APIView):
    def get(self, request):
        groups = GroupModel.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class StudentListView(APIView):
    def get(self, request, group_id):
        students = StudentModel.objects.filter(group_id=group_id)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class GroupAttendance(APIView):
    def get(self, request, group_id):
        students = StudentModel.objects.filter(group_id=group_id)
        print("Students:", students)

        for student in students:
            attendance, created = AttendanceModel.objects.get_or_create(student=student, day=datetime.date.today())
            print("Attendance:", attendance)

        attendance = AttendanceModel.objects.filter(student__group_id=group_id, day=datetime.date.today())
        print("Filtered Attendance:", attendance)

        serializer = AttendanceSerializer(attendance, many=True)
        print("Serialized Data:", serializer.data)

        response = Response(serializer.data)
        print("API Response:", response)

        return response


class StudentAttendanceView(APIView):
    def get(self, request, attendance_id):
        attendance = AttendanceModel.objects.get(id=attendance_id)
        if attendance.is_come == True:
            attendance.is_come = False
        else:
            attendance.is_come = True
        attendance.save()
        attendance = AttendanceModel.objects.filter(student__group_id=attendance.student.group.id, day=datetime.date.today())
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
