from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from apps.users.permissions import IsAdminOnly  # type: ignore
from .models import ECOStage
from apps.approvals.models import ApprovalConfig  # type: ignore
from .serializers import ECOStageSerializer, ApprovalConfigSerializer


class ECOStageListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOnly()]

    def get(self, request):
        stages = ECOStage.objects.all().order_by('sequence')
        return Response(ECOStageSerializer(stages, many=True).data)

    def post(self, request):
        serializer = ECOStageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ECOStageDetailView(APIView):
    permission_classes = [IsAdminOnly]

    def get_object(self, pk):
        try:
            return ECOStage.objects.get(pk=pk)
        except ECOStage.DoesNotExist:
            return None

    def put(self, request, pk):
        stage = self.get_object(pk)
        if not stage:
            return Response({'error': 'Stage not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ECOStageSerializer(stage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stage = self.get_object(pk)
        if not stage:
            return Response({'error': 'Stage not found'}, status=status.HTTP_404_NOT_FOUND)
        if stage.is_default_new or stage.is_default_done:
            return Response(
                {'error': 'Cannot delete default New or Done stages.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        stage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApprovalConfigListCreateView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        configs = ApprovalConfig.objects.select_related('stage', 'user').all()
        return Response(ApprovalConfigSerializer(configs, many=True).data)

    def post(self, request):
        serializer = ApprovalConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApprovalConfigDetailView(APIView):
    permission_classes = [IsAdminOnly]

    def get_object(self, pk):
        try:
            return ApprovalConfig.objects.get(pk=pk)
        except ApprovalConfig.DoesNotExist:
            return None

    def put(self, request, pk):
        config = self.get_object(pk)
        if not config:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApprovalConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        config = self.get_object(pk)
        if not config:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
