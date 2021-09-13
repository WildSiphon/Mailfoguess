import json
<<<<<<< HEAD
import time
import trio,httpx

from progress.bar import Bar

from holehe.modules.mails.google import google
from holehe.modules.mails.laposte import laposte
from holehe.modules.mails.protonmail import protonmail
from holehe.modules.mails.yahoo import yahoo
from holehe.modules.software.office365 import office365
=======
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c

class EmailGenerator():
    """Create a generator of emails

    :param country: country to set
    :type country: str
    """

    def __init__(self,country="fr"):
        """The constructor."""
<<<<<<< HEAD
        self.__providers  = self._set_providers(country=country)
        self.__validators = ["gmail","laposte","protonmail","yahoo","outlook"]
=======
        self.__providers = self._set_providers(country=country)
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c

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

<<<<<<< HEAD
        mail = username+"@"+domain

=======
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
        # https://support.google.com/mail/answer/9211434?hl=en
        if 'gmail' in domain:
            if (len(username) < 6) or (len(username) > 30):
                return
            if ('-' in username) or ('_' in username):
                return
<<<<<<< HEAD
            # if ('.' in username):
            #     return
=======
            # if ('.' in username): # charactère ignoré par google (un.tel = untel)
            #     return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
            
        # https://login.yahoo.com/account/create
        if 'yahoo' in domain:
            if (len(username) < 4) or (len(username) > 32):
                return
            if ('-' in username): # characters interdits
                return
<<<<<<< HEAD
=======
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
            
        if 'outlook' in domain:
            if (len(username) < 1) or (len(username) > 64):
                return
<<<<<<< HEAD
=======
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
        
        # https://compte.laposte.net/inscription/index.do?srv_gestion=lapostefr
        if 'laposte' in domain:
            if (len(username) < 4) or (len(username) > 49):
                return
<<<<<<< HEAD
=======
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
        
        # https://mail.protonmail.com/create/
        if 'protonmail' in domain:
            if (len(username) < 1) or (len(username) > 40):
                return
            # if ('-' in username) or ('_' in username) or ('.' in username):
<<<<<<< HEAD
            #     return
=======
            #     # charactère ignoré par protonmail (un.tel = un-tel = un_tel = untel)
            #     return
            # if not trio.run(validate_mails,mail):
            #     return ({'mail' : mail, 'exist' : False})
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
            
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

<<<<<<< HEAD
        return mail

    async def _validate_mails(self,email):
        out = []
        client = httpx.AsyncClient()
        
        domain = email.split('@')[1].split('.')[0]
        if domain not in self.__validators:
            return "unverified"
        elif domain == 'gmail':
            await google(email, client, out)
        elif domain == 'laposte':
            await laposte(email, client, out)
        elif domain == 'protonmail':
            await protonmail(email, client, out)
        elif domain == 'yahoo':
            await yahoo(email, client, out)
        elif domain == 'outlook':
            await office365(email, client, out)

        await client.aclose()
        
        return out[0]['exists']

    def validate(self,emails: list,provider=None):
        validated_emails = {}

        bar = Bar(f"\t Processing{' '+provider if provider else ''} ({len(emails)})...",suffix='%(percent).1f%% - %(eta)ds',max=len(emails))
        for email in emails:
            validated_emails[email] = []
            # print(f"   {email}",end=" ")
            while validated_emails[email] == []:
                try:
                    validated_emails[email] = trio.run(self._validate_mails,email)
                except Exception as e:
                    pass
            bar.next()
            # print(f": {validated_emails[email]}")
        print("\tDone")
        return validated_emails
=======
        return username+"@"+domain
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c

    def generate(self,usernames: list):
        """Generate emails from a list of usernames

        :param usernames: list of usernames
        :type people: list

<<<<<<< HEAD
        :return: all the emails generated sorted by provider
        :rtype: dict
        """
        emails = {}
        for domain in self.__providers:
            emails[domain] = []
            for username in usernames:
                email = self._create_email(domain=domain,username=username)
                if email: emails[domain].append(email)
        return emails
    
=======
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

>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c
    @property
    def providers(self):
        return self.__providers
    