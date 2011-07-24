from textwrap import dedent
class Task():
	def __init__(self, title=None, notes=None):
		self.key = None
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

#	def __cmp__(self, other):
#		if (self.key == other.key 
#				and self.title == other.title
#				and self.notes == other.notes):
#			return 0
#		elif self.key > other.key:
#			return 1
#		elif self.key < other.key:
#			return -1
			
	def __lt__(self, other):
		if self.key < other.key:
			return True
		
		return False

	def __le__(self, other):
		if self.key <= other.key:
			return True
		
		return False

	def __eq__(self, other):
		if self.key == other.key and self.title == other.title and self.notes == other.notes:
			return True
		
		return False

	def __ne__(self, other):
		if self.key != other.key and self.title != other.title and self.notes != other.notes:
			return True
		
		return False

	def __gt__(self, other):
		if self.key > other.key:
			return True
		
		return False

	def __ge__(self, other):
		if self.key >= other.key:
			return True
		
		return False

