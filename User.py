import re

class User:
    def __init__(self, name, email, password, c_password, tp_no, query):
        self.query = query
        if not name or not email or not password or not c_password or not tp_no:
            raise ValueError
        try:
            self.name = name
            self.email = email
        except:
            raise ValueError

        if password == c_password:
            self.password = password
            self.c_password = c_password
        else:
            raise ValueError
        tp = tp_no.replace("-","").strip()
        if tp.isnumeric() and (len(tp) == 10 or len(tp) == 11):
            self.tp_no = tp_no
        else:
            raise ValueError
        

    def __str__(self):
        return None
    
    @property
    def name(self):
        return self._name

    @name.setter    
    def name(self, name):
        if len(self.query) != 0:
            raise ValueError
        else:
            self._name = name
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            self._email = email
        else:
            raise ValueError
    
    

        

