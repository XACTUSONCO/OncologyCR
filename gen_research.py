import os
import random
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oncology_abc.settings")
django.setup()

from research.models import Research, Cancer, Lesion, Phase, \
    Alternation, Line, Chemotherapy, IO_Naive, PDL1, Brain_METS, Biopsy
from django.contrib.auth.models import User

faker = Faker()

m2m_field_class_list = [Cancer, Phase, Chemotherapy, Alternation, Line]
o2m_field_class_list = [Lesion, PDL1, IO_Naive, Brain_METS, Biopsy]


def random_select_many2many():
    choice_values = []
    for c in m2m_field_class_list:
        choices = c.__dict__['CHOICES']
        values = []
        while not values:
            values = [choices[i][0] for i in range(len(choices))
                      if bool(random.getrandbits(1))][:3]
        if 'na' in values or -1 in values:
            values = [values[0]]
        choice_values.append(values)

    return choice_values


def random_select_one2many():
    choice_values = []
    for c in o2m_field_class_list:
        count = c.objects.all().count()
        idx = random.randint(1, count)
        value = c.objects.get(pk=idx)
        choice_values.append(value)

    return choice_values


def generate_research():
    liver_func = None
    lung_func = None
    heart_func = None
    kidney_func = None
    remark = None
    if bool(random.getrandbits(1)):
        liver_func = faker.paragraph(nb_sentences=10)
    if bool(random.getrandbits(1)):
        lung_func = faker.paragraph(nb_sentences=10)
    if bool(random.getrandbits(1)):
        heart_func = faker.paragraph(nb_sentences=10)
    if bool(random.getrandbits(1)):
        kidney_func = faker.paragraph(nb_sentences=10)
    if bool(random.getrandbits(1)):
        remark = faker.paragraph(nb_sentences=10)

    (cancer, phase, chemotherapy, alternation, line) = random_select_many2many()
    (lesion, pdl1, io_naive, brain_mets, biopsy) = random_select_one2many()

    uploader = User.objects.get(id=1)
    turn_aronud_time = random.randint(1, 54)
    crc = faker.name()
    contact = faker.phone_number()

    new_research = Research(
        is_recruiting=bool(random.getrandbits(1)),
        research_name=faker.company(),
        medicine_name=faker.catch_phrase(),
        PI=faker.name(),
        crc=crc,
        contact=contact,
        uploader=uploader,
        lesion=lesion,
        pdl1=pdl1,
        io_naive=io_naive,
        brain_mets=brain_mets,
        biopsy=biopsy,
        turn_around_time=turn_aronud_time,
        liver_function=liver_func,
        lung_function=lung_func,
        heart_function=heart_func,
        kidney_function=kidney_func,
        remark=remark
    )
    new_research.save()

    new_research.cancer.set(Cancer.objects.filter(value__in=cancer))
    new_research.phase.set(Phase.objects.filter(value__in=phase))
    new_research.chemotherapy.set(Chemotherapy.objects.filter(value__in=chemotherapy))
    new_research.alternation.set(Alternation.objects.filter(value__in=alternation))
    new_research.line.set(Line.objects.filter(value__in=line))

    print(new_research)
    return


for _ in range(33):
    generate_research()
