from rest_framework import serializers  # type: ignore
from .models import ECOStage
from apps.approvals.models import ApprovalConfig  # type: ignore
from apps.users.serializers import UserSerializer  # type: ignore


class ECOStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECOStage
        fields = ['id', 'name', 'sequence', 'is_default_new', 'is_default_done']
        read_only_fields = ['id']


class ApprovalConfigSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.login_id', read_only=True)
    stage_name = serializers.CharField(source='stage.name', read_only=True)

    class Meta:
        model = ApprovalConfig
        fields = ['id', 'stage', 'stage_name', 'user', 'user_name', 'category']
