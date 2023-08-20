from django.urls import path

from student.views import (
    behavioural_view,
    affective_view,
    cognitive_view
)

app_name = 'student'

urlpatterns = [
    path('<slug>/behavioural/', behavioural_view, name = "behavioural"),
    path('<slug>/affective/', affective_view, name = "affective"),
    path('<slug>/cognitive/', cognitive_view, name = "cognitive")
]