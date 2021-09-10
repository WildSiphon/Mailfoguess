import json

class EmailGenerator():
    """Create a generator of emails

    :param country: country to set
    :type country: str
    """

    def __init__(self,country="fr"):
        """The constructor."""
        self.__providers = self._set_providers(country=country)

    def _set_providers(self,country):
        """Set the providers used for the generation 
        by choosing from a list and keeping only the good ones."""
        with open(("./ressources/providers.json"),"r") as f:
            providers = json.load(f)
        providers = providers["test"]
        return providers

    def _create_email(self,username,domain):
        """Create an email by concatening param and following rules

        :param username: local-part of email
        :type username: str
        
        :param username: domain of email
        :type username: str

        :return: username@domain if rules are good
        :rtype: str
        """

        # https://support.google.com/mail/answer/9211434?hl=en
        if 'gmail' in domain:
            if (len(username) < 6) or (len(username) > 30):
                return
            if ('-' in username) or ('_' in username):
                return
            # if ('.' in username): # charactère ignoré par google (un.tel = untel)
            #     return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
            
        # https://login.yahoo.com/account/create
        if 'yahoo' in domain:
            if (len(username) < 4) or (len(username) > 32):
                return
            if ('-' in username): # characters interdits
                return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
            
        if 'outlook' in domain:
            if (len(username) < 1) or (len(username) > 64):
                return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
        
        # https://compte.laposte.net/inscription/index.do?srv_gestion=lapostefr
        if 'laposte' in domain:
            if (len(username) < 4) or (len(username) > 49):
                return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
        
        # https://mail.protonmail.com/create/
        if 'protonmail' in domain:
            if (len(username) < 1) or (len(username) > 40):
                return
            # if ('-' in username) or ('_' in username) or ('.' in username):
            #     # charactère ignoré par protonmail (un.tel = un-tel = un_tel = untel)
            #     return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
            
        # https://subscribe.free.fr/accesgratuit/
        if 'free' in domain:
            if (len(username) < 1) or (len(username) > 20):
                return
            if ('-' in username) or ('_' in username):
                return
        
        # https://login.orange.fr/signup
        if 'orange' in domain:
            if (len(username) < 1) or (len(username) > 64):
                return

        return username+"@"+domain

    def generate(self,usernames: list):
        """Generate emails from a list of usernames

        :param usernames: list of usernames
        :type people: list

        :return: all the emails generated
        :rtype: list
        """
        emails = []
        for domain in self.__providers:
            for username in usernames:
                email = self._create_email(domain=domain,username=username)
                if email:
                    emails.append(email)
        return emails

    @property
    def providers(self):
        return self.__providers
    