from rest_framework import serializers

import api.models as models


class DistillerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distillery
        fields = "__all__"
        depth = 1
