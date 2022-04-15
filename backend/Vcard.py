

class vcard:
  def __init__(self, name, lastname, tel):
      self.n = name
      self.fn = lastname
      self.tel = tel


  def get_json(self):
    return {'name': str(self.n), 'lastname':str(self.fn),'tel':str(self.tel)}