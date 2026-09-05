

class GenerateurSQL:

  @classmethod
  def name(self):
    return self.__name__.lower()  

  @classmethod
  def creer_table(self):
    print(f"CREATE TABLE {self.name()}")