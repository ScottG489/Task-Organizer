from textwrap import dedent
class Task():
	def __init__(self, title='', notes = '', priority = int(), tags = []):
#		self.id
		self.title = title
		self.notes = notes
#		self.priority = priority
#		self.tags = tags

	def __str__(self):
		return dedent('''\
			Title: %(title)s
			Notes: %(notes)s''') % {
				'title': self.title,
				'notes': self.notes
		}
