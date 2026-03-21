from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdminOnly
from apps.approvals.models import ApprovalConfig, ApprovalRecord
from .serializers import ApprovalConfigSerializer


class ApprovalConfigListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        configs = ApprovalConfig.objects.select_related('stage', 'user').all()
        return Response(ApprovalConfigSerializer(configs, many=True).data)


class ApprovalConfigCreateView(APIView):
    permission_classes = [IsAdminOnly]

    def post(self, request):
        serializer = ApprovalConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
