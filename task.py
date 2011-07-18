from textwrap import dedent
class Task():
	def __init__(self, title='', notes = '', priority = int(), tags = []):
		self.id = int()
		self.title = title
		self.notes = notes
#		self.priority = priority
#		self.tags = tags

	def __str__(self):
		return dedent('''\
			ID: %(id)s
			Title: %(title)s
			Notes: %(notes)s''') % {
				'id': self.id,
				'title': self.title,
				'notes': self.notes
		}
