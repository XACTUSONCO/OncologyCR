import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oncology_abc.settings")
django.setup()

_dir = 'base_db'

from research.models import ECOG, Cancer, Histology, Lesion, \
    Alternation, Line, Chemotherapy, IO_Naive, MSI, Kinds, CRO, Vendor

#####################
# Generate Field Data
class_list = [ECOG, Cancer, Histology, Lesion,
              Alternation, Line, Chemotherapy, IO_Naive, MSI, Kinds, CRO, Vendor]

for c in class_list:
    c_name = c.__name__
    c_upper_name = c.__name__.upper()
    c_lower_name = c.__name__.lower()
    choices = c.__dict__['CHOICES']

    _json = []
    for pk, choice in enumerate(choices):
        if c_lower_name == 'vendor':
            _json.append({
                "model": 'research.' + c_name,
                "pk": pk + 1,
                "fields": {
                    "value": choice[0],
                    "information": "",
                    "link": "",
                    "vendor_id": "",
                    "vendor_pw": ""
                }
            })
        else:
            _json.append({
                "model": 'research.' + c_name,
                "pk": pk + 1,
                "fields": {
                    c_lower_name + '_type': choice[0]
                }
            })

    with open(os.path.join(_dir, c_lower_name + '.json'), 'w') as f:
        f.write(json.dumps(_json, indent=4))

####################
# Generate Group Data

group_list = ['doctor', 'nurse', 'etc']
for g in group_list:
    _json = []
    for pk, group in enumerate(group_list):
        _json.append({
            'model': 'auth.Group',
            'pk': pk + 1,
            'fields': {
                'name': group
            }
        })
    with open(os.path.join(_dir, 'group.json'), 'w') as f:
        f.write(json.dumps(_json, indent=4))
