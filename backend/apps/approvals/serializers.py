from rest_framework import serializers
from apps.approvals.models import ApprovalConfig


class ApprovalConfigSerializer(serializers.ModelSerializer):
    user_name  = serializers.CharField(source='user.login_id', read_only=True)
    stage_name = serializers.CharField(source='stage.name', read_only=True)

    class Meta:
        model = ApprovalConfig
        fields = ['id', 'stage', 'stage_name', 'user', 'user_name', 'category']
