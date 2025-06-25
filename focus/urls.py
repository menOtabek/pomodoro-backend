from django.urls import path
from .views import PomodoroSessionViewSet

pomodoro_list = PomodoroSessionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

pomodoro_detail = PomodoroSessionViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = [
    path('', pomodoro_list, name='pomodoro-session-list'),
    path('<int:pk>/', pomodoro_detail, name='pomodoro-session-detail'),
]
