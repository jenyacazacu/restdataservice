from django.core.exceptions import ObjectDoesNotExist
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore
from common.data_processing import load_json_file, build_key_map

logger = get_task_logger(__name__)


@task(name="generate_json_file_key_map")
def generate_json_file_key_map(file_id):
    """
    Generate a key_map for a freshly uploaded json file.
    """
    try:
        from dataservice.models import DataFile
        file_obj = DataFile.objects.all().get(pk=file_id)
    except ObjectDoesNotExist as e:
        logger.info("File id {0} not found exiting".format(file_id))
        raise Ignore()
    logger.info("Gennerating key_map for file id:{0}".format(file_id))
    json_df = load_json_file(file_obj.file.url)
    file_obj.key_map = build_key_map(json_df)
    file_obj.save()
