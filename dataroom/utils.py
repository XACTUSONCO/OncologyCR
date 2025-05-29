import os
from uuid import uuid4

def rename_imagefile_to_uuid(instance, filename):
    upload_to = 'reference/'
    uuid = uuid4().hex

    if instance.id:
        filename = '{}.{}'.format(instance.clinical_trial_id, 'png')
    else:
        filename = '{}.{}'.format(uuid, 'png')

    return os.path.join(upload_to, filename)
