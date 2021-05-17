import datetime
class date:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        return datetime.date()

    def to_url(self, value):
        return '%04d' % value