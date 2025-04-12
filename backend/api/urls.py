from django.urls import path
from .views import diagnostic, auth, teleconsultation

urlpatterns = [
    path('diagnose/', diagnostic.DiagnosticView.as_view(), name='diagnose'),
    path('auth/login/', auth.LoginView.as_view(), name='login'),
    path('teleconsult/start/', teleconsultation.StartSessionView.as_view(), name='start_session'),
]