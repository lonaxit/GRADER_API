from django.urls import path,include

from core.api.views import *

urlpatterns =[
    
    path("term/", TermListCreateAPIView.as_view(), name="term"),
    path("term-detail/<int:pk>/", TermDetailAPIView.as_view(), name="term-detail"),
    
    path("session/", SessionListCreateAPIView.as_view(), name="session"),
    path("session-detail/<int:pk>/", SessionDetailAPIView.as_view(), name="session-detail"),
    
    path("school_class/", SchoolClassCreateAPIView.as_view(), name="schoolclass"),
    path("schoolclass-detail/<int:pk>/", SchoolClassDetailAPIView.as_view(), name="schoolclass-detail"),
    
    path("subject/", SubjectCreateAPIView.as_view(), name="subject"),
    path("subject-detail/<int:pk>/", SubjectDetailAPIView.as_view(), name="subject-detail"),
    
    path("subject-perclass/", SubjectPerClassCreateAPIView.as_view(), name="subject-perclass"),
    path("subjectperclass-detail/<int:pk>/", SubjectPerClassDetailAPIView.as_view(), name="subjectperclass-detail"),
    
    path("attendance-setting/", AttendanceSettingsCreateAPIView.as_view(), name="attendance-setting"),
    path("attendancesetting-detail/<int:pk>/", AttendanceSettingsClassDetailAPIView.as_view(), name="attendancesetting-detail"),
    
    
    path("resumption-setting/", ResumptionSettingsCreateAPIView.as_view(), name="resumption-setting"),
    path("resumptionsetting-detail/<int:pk>/", ResumptionSettingsClassDetailAPIView.as_view(), name="resumptionsetting-detail"),
    
    
    path("student-profile/", StudentProfileCreateAPIView.as_view(), name="student-profile"),
    path("studentprofile-detail/<int:pk>/", StudentProfileClassDetailAPIView.as_view(), name="studentprofile-detail"),
    
    
    path("teacher-profile/", TeacherProfileCreateAPIView.as_view(), name="teacher-profile"),
    path("teacherprofile-detail/<int:pk>/", TeacherProfileClassDetailAPIView.as_view(), name="teacherprofile-detail"),
    
    
    path("list-subjectteacher/", SubjectTeacherListAPIView.as_view(), name="list-subjectteacher"),
    
    path("create-subject-teacher/<int:pk>/", SubjectTeacherCreateAPIView.as_view(), name="create-subject-teacher"),
    
    path("subjectteacher-detail/<int:pk>/", SubjectTeacherClassDetailAPIView.as_view(), name="subjectteacher-detail"),
    
    path("toggle-subjectteacher/<int:pk>/", ToggleSubjectTeacherAPIView.as_view(), name="toggle-subjectteacher"),

]