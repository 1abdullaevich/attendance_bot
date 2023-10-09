from django.urls import path
from .views import *

urlpatterns = [
    path('groups/', GroupListView.as_view()),
    path('students/<int:group_id>/', StudentListView.as_view()),
    # path('attendance/', AttendanceListView.as_view()),
    # path('attendance/<int:group_id>/', GroupAttendanceListView.as_view()),
    path('attendance/<int:group_id>/', GroupAttendance.as_view()),
    path('attendance/student/<int:attendance_id>/', StudentAttendanceView.as_view()),
]
