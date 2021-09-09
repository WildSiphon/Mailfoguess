from user import User

class UsernameGenerator():
    """Create a generator of usernames

    :param level: level of generation, defaults to minimal
    :type level: string

    :param separators: separators used for the generation
    :type separators: string
    """

    LEVEL = {"min" : 0, "low" : 1, "high" : 2, "max" : 3}

    def __init__(self,level="min",separators="-._"):
        """The constructor."""
        self.__level = self.LEVEL[level]
        self.__separators = self._set_separators(separators=separators)
        
        # Replace "" by " " in separators list to creat limiters list
        self.__limiters = [x for x in self.__separators if x != ""]
        self.__limiters.append(" ")

    def _set_separators(self,separators: str):
        """Set the separators used for the generation 
        by converting a string to a list and suppressing doubles."""
        separators = list(dict.fromkeys(list(separators)))
        separators.append("")
        separators.sort()
        return separators

    def _gen_initials(self,name,separator):
        """Generate a list of different initials used in generation.

        :param name: {first,middle,last or user}name given
        :type name: string

        :param separator: separator to use
        :type separator: single char string
        """

        initials = []

        # Name is composed (separated by one of our limiters)    
        if [charac for charac in self.__limiters if(charac in name)]:
            names = []
            for charac in self.__limiters: name = name.replace(charac," ")
            initial = []
            for n in name.split(" "): initial.append(n[0])    
            initials.append("".join(initial))
            initials.append(separator.join(initial))
        # Name is in one word    
        else:
            if name != "": initials.append(name[0])
        return initials

    def _gen_from_name(self,name,separator,last=False,user=False):
        """Generate a list of different names used in generation.

        :param name: {first,middle,last or user}name given
        :type name: string

        :param separator: separator used
        :type separator: single char string

        :param last: if the name is a lastname, default False
        :type last: bool

        :param user: if the name is an username, default False
        :type user: bool
        """

        # Define vowels list
        vowels = ("a","e","i","o","u","y")

        # Replace "" by " " in separators list
        sep = [x for x in self.__separators if x != ""]
        sep.append(" ")
        
        names = []

        # Add one empty name to the list
        if name != "": names.append("")

        # Name is composed (separated by one of our limiters)    
        if [charac for charac in sep if(charac in name)]:
            for charac in sep: name = name.replace(charac," ")
            for n in name.split(" "):
                if not user and len(n) > 2: names.append(n)
            names.append(name.replace(" ",separator))

        # Name is in one word
        else: names.append(name)

        # Name is a lastname
        if last and self.__level >= 1: # Level 1 of generation
            for n in names:
                withoutVowels = n
                for v in vowels:
                    if v in withoutVowels:
                        withoutVowels = withoutVowels.replace(v,"")
                if self.__level >= 2:  # Level 2 of generation
                    if withoutVowels not in names:
                        names.append(withoutVowels)
                # Suppressing doubled consonants
                withoutVowels = "".join(list(dict.fromkeys(withoutVowels)))
                if withoutVowels not in names:
                    names.append(withoutVowels)

        return names

    # Fonction de génération des noms d"utilisateurs en fonction des informations d"une personne
    def generate_usernames(self,people: User):
        """Generate usernames from informations of a User

        :param people: all informations of a user
        :type people: User

        :return: all the usernames generated
        :rtype: list
        """

        user_list = []

        for charac in self.__separators:

            for u in self._gen_from_name(people.username,charac,user=True):
                if u != "" and u not in user_list:
                    user_list.append(u)

            for l in self._gen_from_name(people.lastname,charac,last=True):
                for m in self._gen_from_name(people.middlename,charac):
                    for f in self._gen_from_name(people.firstname,charac):
                        
                        if f != "":
                            if m != "":
                                if l != "":

                                    user_list.append(f + charac + m + charac + l)
                                    if self.__level >= 1: # Level 1 of generation
                                        user_list.append(l + charac + f + charac + m)
                                    if self.__level >= 2: # Level 2 of generation
                                        user_list.append(f + charac + l + charac + m)
                                        user_list.append(l + charac + m + charac + f)
                                    if self.__level >= 3: # Level 3 of generation
                                        user_list.append(m + charac + f + charac + l)
                                        user_list.append(m + charac + l + charac + f)

                                    for fini in self._gen_initials(f,charac):
                                        user_list.append(fini + charac + m + charac + l)
                                        if self.__level >= 1: # Level 1 of generation
                                            user_list.append(l + charac + fini + charac + m)
                                        if self.__level >= 2: # Level 2 of generation
                                            user_list.append(fini + charac + l + charac + m)
                                            user_list.append(l + charac + m + charac + fini)
                                        if self.__level >= 3: # Level 3 of generation
                                            user_list.append(m + charac + fini + charac + l)
                                            user_list.append(m + charac + l + charac + fini)

                                    if self.__level >= 2:  # Level 2 of generation
                                        for mini in self._gen_initials(m,charac):
                                            user_list.append(f + charac + l + charac + mini)
                                            user_list.append(l + charac + mini + charac + f)
                                            if self.__level >= 3:  # Level 3 of generation
                                                user_list.append(f + charac + mini + charac + l)
                                                user_list.append(l + charac + f + charac + mini)
                                                user_list.append(mini + charac + f + charac + l)
                                                user_list.append(mini + charac + l + charac + f)

                                    for lini in self._gen_initials(l,charac):
                                        user_list.append(f + charac + m + charac + lini)
                                        if self.__level >= 1:  # Level 1 of generation
                                            user_list.append(lini + charac + f + charac + m)
                                        if self.__level >= 2:  # Level 2 of generation
                                            user_list.append(f + charac + lini + charac + m)
                                            user_list.append(lini + charac + m + charac + f)
                                        if self.__level >= 3:  # Level 3 of generation
                                            user_list.append(m + charac + f + charac + lini)
                                            user_list.append(m + charac + lini + charac + f)
                                else:
                                    if self.__level >= 1:  # Level 1 of generation
                                        user_list.append(f + charac + m)
                                        if self.__level >= 2:  # Level 2 of generation
                                            user_list.append(m + charac + f)

                                        for fini in self._gen_initials(f,charac):
                                            user_list.append(fini + charac + m)
                                            if self.__level >= 2:  # Level 2 of generation
                                                user_list.append(m + charac + fini)

                                        for mini in self._gen_initials(m,charac):
                                            user_list.append(f + charac + mini)
                                            if self.__level >= 2:  # Level 2 of generation
                                                user_list.append(mini + charac + f)
                            elif l != "":
                                user_list.append(f + charac + l)
                                if self.__level >= 1:  # Level 1 of generation
                                    user_list.append(l + charac + f)
                                
                                for fini in self._gen_initials(f,charac):
                                    user_list.append(fini + charac + l)
                                    if self.__level >= 1:  # Level 1 of generation
                                        user_list.append(l + charac + fini)
                                
                                for lini in self._gen_initials(l,charac):
                                    user_list.append(f + charac + lini)
                                    if self.__level >= 1:  # Level 1 of generation
                                        user_list.append(lini + charac + f)
                            else:
                                if f not in user_list:
                                    user_list.append(f)

                        elif m != "":
                            if self.__level >= 1:  # Level 1 of generation
                                if l != "":

                                    user_list.append(m + charac + l)
                                    user_list.append(l + charac + m)

                                    for lini in self._gen_initials(l,charac):
                                        user_list.append(m + charac + lini)
                                        user_list.append(lini + charac + m)

                                    if self.__level >= 2:  # Level 2 of generation
                                        for mini in self._gen_initials(m,charac):
                                            user_list.append(mini + charac + l)
                                            user_list.append(l + charac + mini)
                                else:
                                    if self.__level >= 1:  # Level 1 of generation
                                        if m not in user_list:
                                            user_list.append(m)

                        elif l != "":
                            if l not in user_list:
                                user_list.append(l)
            
        if people.number != None:
            usernames_with_number = []
            for ul in user_list:
                toAdd = []
                for charac in self.__limiters:
                    if charac in ul:
                        for y in people.number:
                            toAdd.append(ul + charac + y)
                if toAdd == []:
                    for y in people.number:
                        toAdd.append(ul + y)
                usernames_with_number.extend(toAdd)
            user_list.extend(usernames_with_number)

        # Suppressing doubles and sorting
        user_list = list(dict.fromkeys(user_list))
        user_list.sort()
        return user_list

    @property
    def separators(self):
        return self.__separators

    @property
    def level(self):
        l = ["Minimal","Low","High","Maximal"]
        return l[self.__level]