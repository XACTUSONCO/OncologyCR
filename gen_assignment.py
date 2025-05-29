import datetime
import os
import random

import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oncology_abc.settings")
django.setup()

from django.contrib.auth.models import User
from research.models import Research
from feedback.models import Assignment, Feedback, SEX_CHOICES, DX_CHOICES, STATUS_CHOICES, \
    RESPONSE_CHOICES

faker = Faker()
research_list = Research.objects.all()

_start_date = datetime.date(2020, 1, 1)
_end_date = datetime.date.today()


def generate_feedback(assignment, n):
    time_between_dates = _end_date - _start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    photo_date = _start_date + datetime.timedelta(days=random_number_of_days)

    print(f'\tCreating {n} feedback(s)...')
    for _ in range(n):
        delta = random.randrange(1, 31)
        photo_date = photo_date + datetime.timedelta(days=delta)
        response = random.choice(RESPONSE_CHOICES)[0]
        response_text = faker.word()
        toxicity = faker.sentence(nb_words=4)
        comment = faker.sentence(nb_words=4)
        cycle = faker.word()
        dosing_date = photo_date + datetime.timedelta(days=random.randrange(delta))
        tx_dose = faker.word()
        new_feedback = Feedback(
            photo_date=photo_date,
            response=response,
            response_text=response_text,
            toxicity=toxicity,
            comment=comment,
            cycle=cycle,
            dosing_date=dosing_date,
            tx_dose=tx_dose,
            assignment=assignment
        )
        new_feedback.save()
        print('\t' + str(new_feedback))


def generate_assignment():
    no = faker.ean(length=8)
    register_number = int(faker.ean(length=13))
    name = faker.name()
    sex = random.choice(SEX_CHOICES)[0]
    age = random.randint(50, 90)
    crc = User.objects.get(id=1)
    status = random.choice(STATUS_CHOICES)[0]
    dx = random.choice(DX_CHOICES)[0]
    previous_tx = faker.paragraph()
    research = random.choice(research_list)

    new_assignment = Assignment(
        no=no,
        register_number=register_number,
        name=name,
        sex=sex,
        age=age,
        crc=crc,
        status=status,
        dx=dx,
        previous_tx=previous_tx,
        research=research
    )
    new_assignment.save()
    print(new_assignment)

    n_of_feedback = random.randint(0, 20)
    generate_feedback(new_assignment, n_of_feedback)


if __name__ == '__main__':
    for _ in range(133):
        generate_assignment()
