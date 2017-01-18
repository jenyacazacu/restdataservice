from dataservice.models import DataFile
from rest_framework import serializers

class DataFileSerializer(serializers.ModelSerializer):

    file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=True)
    filename = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = DataFile
        fields = ('id', 'filename', 'description', 'upload_datetime', 'file')
