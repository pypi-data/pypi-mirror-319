from epyk.core.html.Html import Component


class Btn(Component):
  css_classes = None
  name = "Evergreen Button"

  str_repr = '''<Button marginRight=16>{text}</Button>'''

  def write_values(self):
    return {"text": self._vals}

