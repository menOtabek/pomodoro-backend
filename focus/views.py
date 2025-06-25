from datetime import timedelta

from django.db.models import Sum
from django.utils.timezone import now
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PomodoroSession
from .serializers import PomodoroCreateSessionSerializer, PomodoroSessionUpdateSerializer, PomodoroSessionSerializer


@extend_schema(tags=["Sessions"])
class PomodoroSessionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PomodoroSession.objects.filter(user=self.request.user).order_by('-start_time')

    @extend_schema(tags=["Sessions"])
    class PomodoroSessionViewSet(viewsets.ViewSet):
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            return PomodoroSession.objects.filter(user=self.request.user).order_by('-start_time')

        # @extend_schema(
        #     summary="List Pomodoro sessions with optional filters",
        #     description="Returns a filtered list of Pomodoro sessions for the authenticated user.\n\n"
        #                 "Supports optional `range` parameter: `today`, `week`, `month`, `year`.",
        #     responses=PomodoroSessionSerializer
        # )
        # def list(self, request):
        #     queryset = self.get_queryset()
        #
        #     serializer = PomodoroSessionSerializer(queryset, many=True)
        #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve a Pomodoro session",
        description="Returns detail of a specific Pomodoro session.",
        responses=PomodoroSessionSerializer
    )
    def retrieve(self, request, pk=None):
        try:
            session = self.get_queryset().get(pk=pk)
        except PomodoroSession.DoesNotExist:
            return Response(data="Not found.", status=status.HTTP_404_NOT_FOUND)

        serializer = PomodoroSessionSerializer(session)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a new Pomodoro session",
        description="Creates a new Pomodoro session. Do not provide duration — it is calculated later.",
        request=PomodoroCreateSessionSerializer,
        responses=PomodoroCreateSessionSerializer
    )
    def create(self, request):
        serializer = PomodoroCreateSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update Pomodoro session duration",
        description="Updates the duration of a Pomodoro session by providing the end_time (as UNIX timestamp).",
        request=PomodoroSessionUpdateSerializer,
        responses=PomodoroSessionUpdateSerializer
    )
    def partial_update(self, request, pk=None):
        session = self.get_queryset().filter(pk=pk).first()
        if not session:
            return Response(data="Pomodoro session not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = PomodoroSessionUpdateSerializer(instance=session, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get Pomodoro statistics",
        description="Get statistics for today/week/month/year.\nReturns chart data, total worked time, break time, and session count.",
        parameters=[
            OpenApiParameter(name="range", type=OpenApiTypes.STR, description="today, week, month, year",
                             required=False)
        ]
    )
    def list(self, request):
        user = request.user
        range_param = request.query_params.get('range', 'today')
        today = now()

        def format_minutes(seconds):
            hours = seconds // 3600
            mins = seconds % 3600 // 60
            return {'hours': hours, 'minutes': mins}

        queryset = PomodoroSession.objects.filter(user=user)

        if range_param == "today":
            queryset = queryset.filter(start_time__date=today.date())
        elif range_param == "week":
            queryset = queryset.filter(start_time__gte=today - timedelta(days=7))
        elif range_param == "month":
            queryset = queryset.filter(start_time__gte=today - timedelta(days=30))
        elif range_param == "year":
            queryset = queryset.filter(start_time__gte=today - timedelta(days=365))

        work_sessions = queryset.filter(category__type='work')
        break_sessions = queryset.filter(category__type='break')

        # total_work_duration = work_sessions.aggregate(total=Sum('duration'))['total'] or 0
        # total_break_duration = break_sessions.aggregate(total=Sum('duration'))['total'] or 0
        session_count = queryset.count()

        chart_data = []
        if range_param == "week":
            for i in range(1, 8):
                date = today - timedelta(days=today.weekday() - i)
                work_count = work_sessions.filter(start_time__date=date.date()).count()
                break_count = break_sessions.filter(start_time__date=date.date()).count()
                work_duration = work_sessions.filter(start_time__date=date.date()).aggregate(total=Sum('duration'))['total'] or 0
                break_duration = break_sessions.filter(start_time__date=date.date()).aggregate(total=Sum('duration'))['total'] or 0
                chart_data.append({
                    "label": i,
                    "work_count": work_count,
                    "break_count": break_count,
                    "work_duration": format_minutes(work_duration),
                    "break_duration": format_minutes(break_duration),
                })

        elif range_param == "month":
            for i in range(1, today.day + 2):
                work_count = work_sessions.filter(start_time__day=i).count()
                break_count = break_sessions.filter(start_time__day=i).count()
                work_duration = work_sessions.filter(start_time__day=i).aggregate(total=Sum('duration'))[
                                    'total'] or 0
                break_duration = break_sessions.filter(start_time__day=i).aggregate(total=Sum('duration'))[
                                     'total'] or 0
                chart_data.append({
                    "label": str(i),
                    "work_count": work_count,
                    "break_count": break_count,
                    "work_duration": format_minutes(work_duration),
                    "break_duration": format_minutes(break_duration),
                })

        elif range_param == "year":
            for i in range(1, 13):
                work_count = work_sessions.filter(start_time__month=i).count()
                break_count = break_sessions.filter(start_time__month=i).count()
                work_duration = work_sessions.filter(start_time__month=i).aggregate(total=Sum('duration'))[
                                    'total'] or 0
                break_duration = break_sessions.filter(start_time__month=i).aggregate(total=Sum('duration'))[
                                     'total'] or 0
                chart_data.append({
                    "label": i,
                    "work_count": work_count,
                    "break_count": break_count,
                    "work_duration": format_minutes(work_duration),
                    "break_duration": format_minutes(break_duration),
                })


        return Response({
            # "worked_duration": format_minutes(total_work_duration),
            # "break_duration": format_minutes(total_break_duration),
            "session_count": session_count,
            "chart_data": chart_data
        }, status=status.HTTP_200_OK)

