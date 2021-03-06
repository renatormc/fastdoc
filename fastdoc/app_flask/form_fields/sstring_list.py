from wtforms import Field
from wtforms.widgets import TextInput


class SStringList(Field):
    widget = TextInput()

    def __init__(self, *args, separator=",", **kargs):
        super().__init__(*args, **kargs)
        self.sep = separator

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return self.sep.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        
        try:
            self.data = [item.strip() for item in valuelist[0].split(self.sep)]
        except Exception as e:
            self.data = []
            raise ValueError(str(e))