from textwrap import dedent
class Task():
	def __init__(self, title='', notes = ''):
		self.key = int()
		self.title = title
		self.notes = notes
#		self.priority = priority
#		self.tags = tags

	def __str__(self):
		return dedent('''\
			ID: %(key)s
			Title: %(title)s
			Notes: %(notes)s''') % {
				'key': self.key,
				'title': self.title,
				'notes': self.notes
		}
