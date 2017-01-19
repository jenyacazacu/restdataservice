from django.core.exceptions import ObjectDoesNotExist
from dataservice.models import DataFile, StoredData
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from dataservice.serializers import DataFileSerializer
from common.data_processing import load_json_file, raw_aggregate, keymap_aggregate
import ast

class DataFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows datafiles to be viewed.
    """
    queryset = DataFile.objects.all().order_by('-upload_datetime')
    serializer_class = DataFileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def create(self, request):
        file_obj = request.data['file']
        if not file_obj or file_obj.content_type != 'application/json':
            return Response({'details':"Upload must include a JSON readable file."}, status.HTTP_400_BAD_REQUEST)
        # ...
        # upload file to a service if we need to and only store the url in the  models
        # for this purpose we will keep it simple and save the file with the model
        # ...
        uploaded_file = DataFile(filename=request.data['filename'] or file_obj.name,
                                 description=request.data['description'],
                                 file=file_obj)
        uploaded_file.save()
        data = DataFileSerializer(uploaded_file).data
        data['file'] = request.build_absolute_uri(uploaded_file.file.url)
        return Response(data, status.HTTP_201_CREATED)


class AggregateView(APIView):
    """
    API endpoint to request an aggregate of one field in a file.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kw):
        file_id = kw.get('file_id', None)
        aggregate_field_name = kw.get('aggregate_field', None)
        response_status = None
        details = ''
        data = {'result':None, 'details':None}
        try:
            file = DataFile.objects.all().get(pk=file_id)
        except ObjectDoesNotExist:
            file = None
        if not file:
            data['details'] = "File id {0} does not exist".format(file_id)
            response_status = status.HTTP_404_NOT_FOUND
            response = Response(data, status=response_status)
            return response
        else:
            aggregate = None
            try:
                stored_data = StoredData.objects.filter(file__id=file.id,
                                                        field_name=aggregate_field_name
                                                        ).values_list('calculated_value', flat=True)
            except ObjectDoesNotExist:
                stored_data = None
            if not stored_data:
                try:
                    json_df = load_json_file(file.file.url)
                except ValueError:
                    data['details'] = "Error in reading uploaded file, please make sure it is valid JSON"
                    response_status = status.HTTP_400_BAD_REQUEST
                    response = Response(data, status=response_status)
                    return response
                # if the file's keymap got generated use the faster aggregate function
                if file.key_map:
                    key_map = ast.literal_eval(file.key_map)
                    aggregate, details,  response_status = keymap_aggregate(json_df, aggregate_field_name, key_map)
                else:
                    aggregate, details,  response_status = raw_aggregate(json_df, aggregate_field_name)
                data['details'] = details
            else:
                aggregate = stored_data[0]
                response_status = status.HTTP_200_OK
                data['details'] = "success"
                data['result'] = str(aggregate)
            if aggregate and not stored_data:
                # store calculated_value for later use
                new_stored_data = StoredData(file=file, field_name=aggregate_field_name, calculated_value=aggregate)
                new_stored_data.save()
                data['result'] = str(aggregate)
        response = Response(data, status=response_status)
        return response
