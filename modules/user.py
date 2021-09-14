class User():
    """User class

    :param *name: {first,middle,last or user}name of the user
    :type *name: string

    :param number: number refereing to the user (year of birth, locality...)
    :type number: str
    """

    def __init__(self,firstname,middlename,lastname,username,number):
        """The constructor."""
        self._firstname  = self._define_name(firstname)
        self._middlename = self._define_name(middlename)
        self._lastname   = self._define_name(lastname)
        self._username   = self._define_name(username)
        self._number     = self._define_number(number)

    def _define_number(self,number):
        """Format number"""
        if not number:
            return None
        elif number.isnumeric():
            return [number[-2:],number] if len(number)>2 else [number]
        else:
            return None

    def _define_name(self,name):
        """Format *name"""
        if name == "": return None

        name = name.strip().lower() if name else ""
        accents = {
            "a" : ["à", "ã", "á", "â", "ä", "å"],
            "e" : ["é", "è", "ê", "ë"],
            "i" : ["î", "ï", "ì", "í"],
            "o" : ["ô", "ö", "ò", "ó", "õ", "ø"],
            "u" : ["ù", "ü", "û", "ú"],
            "y" : ["ÿ", "ý"],
            "c" : ["ç"],
            "s" : ["š"],
            "z" : ["ž"],
            "n" : ["ñ"],
            "ae": ["æ"],
            "oe": ["œ"],
        }
        for char in accents:
            for accented_char in accents[char]:
                name = name.replace(accented_char, char)
        return name

    def print(self):
        """Print user's informations"""
        if self._firstname != "":
            print(f"Firstname  : {self._firstname}") 
        if self._middlename != "":
            print(f"Middlename : {self._middlename}") 
        if self._lastname != "":
            print(f"Lastname   : {self._lastname}") 
        if self._username != "":
            print(f"Username   : {self._username}")
        if self._number:
            print(f"Number     : {' and '.join(self._number[::-1])}")

    @property
    def firstname(self):
        return self._firstname

    @property
    def middlename(self):
        return self._middlename

    @property
    def lastname(self):
        return self._lastname

    @property
    def username(self):
        return self._username

    @property
    def number(self):
        return self._number