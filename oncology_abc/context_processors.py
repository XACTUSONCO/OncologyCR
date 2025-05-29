from user.models import Contact, InvestigatorContact
from datetime import datetime
import calendar

def onco_team(request):
    today = datetime.today()
    onco_A_crc = Contact.objects.filter(onco_A=1).values_list('user_id', flat=True)
    onco_A_investigator = InvestigatorContact.objects.filter(onco_A=1).values_list('user_id', flat=True)
    onco_team = onco_A_crc.union(onco_A_investigator)

    return {'onco_team': onco_team,
            'from_month_date': datetime(today.year, today.month, 1),
            'to_month_date': datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
            }