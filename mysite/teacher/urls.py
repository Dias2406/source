from django.urls import path

from teacher.views import (
    behavioural_view,
    cognitive_view,
    affective_view
)

app_name = 'teacher'

urlpatterns = [
    path('<slug>/behavioural/', behavioural_view, name = "behavioural"),
    path('<slug>/cognitive/', cognitive_view, name = "cognitive"),
    path('<slug>/affective/', affective_view, name = "affective"),
]