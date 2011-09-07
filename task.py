from textwrap import dedent

class Task():
    def __init__(self, **kwargs):
        try:
            self.key = kwargs['key']
        except:
            self.key = None

        try:
            self.title = kwargs['title']
        except:
            self.title = None

        try:
            self.notes = kwargs['notes']
        except:
            self.notes = None

#        self.priority = priority
#        self.tags = tags


    def __str__(self):
        return dedent('''\
            ID: %(key)s
            Title: %(title)s
            Notes: %(notes)s''') % {
                'key': self.key,
                'title': self.title,
                'notes': self.notes
        }

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        if self.key == other.key\
                and self.title == other.title\
                and self.notes == other.notes:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Task):
            return True
        if self.key != other.key\
                or self.title != other.title\
                or self.notes != other.notes:
            return True

        return False
