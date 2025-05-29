from calendar import HTMLCalendar
from feedback.models import Feedback

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, next_visit):
		next_visit_per_day = next_visit.filter(next_visit__day=day, next_visit__year=self.year, next_visit__month=self.month)

		d = ''
		for n in next_visit_per_day:
				d += f'{n.get_html_url_next_visit}'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, next_visit):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, next_visit)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		next_visit = Feedback.objects.filter(assignment__is_deleted=0, next_visit__isnull=False)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, next_visit)}\n'
		return cal