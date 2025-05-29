from calendar import HTMLCalendar
from .models import Patient, Leave
from django.db.models import Q, F
from django.db.models.functions import ExtractMonth
from feedback.models import Feedback
from django.urls import reverse
from datetime import date

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events, next_visit, cycle_visit):
		events_per_day = events.filter(user=self.user).annotate(end_date_month=ExtractMonth('end_date'))\
			.filter(Q(from_date__day=day, end_date__isnull=True) |
					Q(from_date__day__lte=day, end_date__day__gte=day) |
					(Q(from_date__day__lte=day, from_date__year=self.year, from_date__month=self.month) &
					 ~Q(from_date__month=F('end_date_month'))) |
					(Q(end_date__day__gte=day, end_date__year=self.year, end_date__month=self.month) &
					 ~Q(from_date__month=F('end_date_month'))))

		next_visit_per_day = next_visit.filter(next_visit__day=day, next_visit__year=self.year, next_visit__month=self.month)\
									   .filter(Q(assignment__curr_crc__user_id=self.user.id) | Q(assignment__PI=self.user.first_name))
		cycle_per_day = cycle_visit.filter(dosing_date__day=day, dosing_date__year=self.year, dosing_date__month=self.month)\
								   .filter(Q(assignment__curr_crc__user_id=self.user.id) | Q(assignment__PI=self.user.first_name))

		d = ''
		for event in events_per_day:
			d += f'{event.get_html_url}'

		for n in next_visit_per_day:
			if cycle_per_day.filter(Q(assignment_id=n.assignment)):
				d += ''
			else:
				d += f'{n.get_html_url_next_visit}'

		for cycle_viist in cycle_per_day:
			d += f'{cycle_viist.get_html_url_cycle}'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events, next_visit, cycle_visit):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events, next_visit, cycle_visit)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, left, withyear=True):
		events = Patient.objects.filter(is_deleted=False)\
						      .filter(Q(from_date__year=left.year, from_date__month=left.month) |
									  Q(end_date__year=left.year, end_date__month=left.month))

		next_visit = Feedback.objects.filter(assignment__is_deleted=0, next_visit__isnull=False)
		cycle_visit = Feedback.objects.filter(assignment__is_deleted=0, cycle__isnull=False, dosing_date__isnull=False)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(left.year, left.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(left.year, left.month):
			cal += f'{self.formatweek(week, events, next_visit, cycle_visit)}\n'
		return cal


	def leave_formatday(self, day, events):
                events_per_day = events.filter(Q(from_date__day=day))

		d = ''
		for event in events_per_day:
			today = date.today()
			url = reverse('leave:leave_edit', args=(event.id,))
			if event.kind == 'Annual' and event.user_id == self.user.id and event.from_date >= today: # 연차 / 휴가 전
				d += f'<div class="Annual-title"><a href="{url}" style="color:black;"> {event.name} </a></div>'

			elif (event.kind == 'morning_Half' and event.user_id == self.user.id and event.from_date >= today)\
					or (event.kind == 'afternoon_Half' and event.user_id == self.user.id and event.from_date >= today): # 오전,오후반차 / 휴가 전
				d += f'<div class="Half-title"><a href="{url}" style="color:black;"> {event.name} </a></div>'

			elif (event.kind == 'carry_over' and event.user_id == self.user.id and event.from_date >= today)\
					or (event.kind == 'carry_over_Half' and event.user_id == self.user.id and event.from_date >= today): # 이월 (1일, 0.5일) / 휴가 전
				d += f'<div class="carry-over-title"><a href="{url}" style="color:black;"> {event.name} </a></div>'

			elif event.kind == 'Monthly' and event.user_id == self.user.id and event.from_date >= today: # 월차 / 휴가 전
				d += f'<div class="Monthly-title"><a href="{url}" style="color:black;"> {event.name} </a></div>'

			elif event.kind == 'official' and event.user_id == self.user.id and event.from_date >= today: # 공가 / 휴가 전
				d += f'<div class="official-title"><a href="{url}" style="color:black;"> {event.name} </a></div>'

			elif (event.kind == 'Annual' and event.user_id != self.user.id) or (event.kind == 'Annual' and event.from_date < today and event.user_id == self.user.id): # 사용자의 지난 휴가 혹은 다른 사용자의 휴가 (연차)
				d += f'<div class="Annual-title detail-leave" leave-id="{event.id}"> {event.name} </div>'

			elif (event.kind == 'morning_Half' and event.user_id != self.user.id) or (event.kind == 'afternoon_Half' and event.user_id != self.user.id)\
					or (event.kind == 'morning_Half' and event.from_date < today and event.user_id == self.user.id)\
					or (event.kind == 'afternoon_Half' and event.from_date < today and event.user_id == self.user.id): # 사용자의 지난 휴가 혹은 다른 사용자의 휴가 (반차)
				d += f'<div class="Half-title detail-leave" leave-id="{event.id}"> {event.name} </div>'

			elif (event.kind == 'carry_over' and event.user_id != self.user.id) or (event.kind == 'carry_over_Half' and event.user_id != self.user.id)\
					or (event.kind == 'carry_over' and event.from_date < today and event.user_id == self.user.id)\
					or (event.kind == 'carry_over_Half' and event.from_date < today and event.user_id == self.user.id): # 사용자의 지난 휴가 혹은 다른 사용자의 휴가 (이월 1일/0.5일)
				d += f'<div class="carry-over-title detail-leave" leave-id="{event.id}"> {event.name} </div>'

			elif (event.kind == 'Monthly' and event.user_id != self.user.id) or (event.kind == 'Monthly' and event.from_date < today and event.user_id == self.user.id): # 사용자의 지난 휴가 혹은 다른 사용자의 휴가 (월차)
				d += f'<div class="Monthly-title detail-leave" leave-id="{event.id}"> {event.name} </div>'

			elif (event.kind == 'official' and event.user_id != self.user.id) or (event.kind == 'official' and event.from_date < today and event.user_id == self.user.id): # 사용자의 지난 휴가 혹은 다른 사용자의 휴가 (공가)
				d += f'<div class="official-title detail-leave" leave-id="{event.id}"> {event.name} </div>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def leave_formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.leave_formatday(d, events)
		return f'<tr> {week} </tr>'

	def leave_formatmonth(self, right, withyear=True):
		events = Leave.objects.filter(is_deleted=False) \
							.filter(Q(from_date__year=right.year, from_date__month=right.month))

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar" style="width: calc(50% - 10px); float:left; margin: 5px;">\n'
		cal += f'{self.formatmonthname(right.year, right.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(right.year, right.month):
			cal += f'{self.leave_formatweek(week, events)}\n'
		return cal
