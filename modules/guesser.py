import os
import trio
import json

from progress.bar import Bar

from modules.user import User
from modules.email_generator import EmailGenerator
from modules.localpart_generator import LocalPartGenerator

class Guesser():
    """Class guessing the emails address
    
    :param user: informations known concerning the target
    :type user: User

    :param level: level of generation wanted (default "min")
    :type level: str
    """

    def __init__(self,user: User,level="min"):
        """The constructor"""

        # Useful generators
        self._localpart_generator = LocalPartGenerator(level=level)
        self._email_generator     = EmailGenerator()
        
        # Param
        self._user       = user
        self._localparts = self._localpart_generator.generate(self._user)
        self._emails     = self._email_generator.generate(self._localparts)
        self._validated_emails = {}

    def validate(self,validate_all=False):
        """Validate the existence of emails by domain

        :param validate_all: flag to validate evrything wihtout asking th user
        :type validate_all: bool
        """
        for provider in self._emails:
            self._validated_emails[provider] = {}

            if provider.split(".")[0] not in self._email_generator.validators:
                print(f"Can't verify {provider.split('.')[0]}\'s mails validity")
                for email in self._emails[provider]:
                    self._validated_emails[provider][email] = None

            else:
                if validate_all: answer = "y"
                else:
                    answer = input(f"Would you like to verify {provider} ({len(self._emails[provider])})\t[N/y] ")
                
                if answer in ["y","Y","yes","Yes","yEs","yeS","YEs","YeS","yES","YES"]:
                    bar = Bar(
                        f"> Processing {provider} ({len(self._emails[provider])})...\t",
                        suffix='%(percent).1f%% - %(eta)ds',
                        max=len(self._emails[provider])
                    )

                    for email in self._emails[provider]:
                        self._validated_emails[provider][email] = -1
                        while self._validated_emails[provider][email] == -1:
                            try:
                                self._validated_emails[provider][email] = trio.run(self._email_generator.validate_email,email)
                            except Exception as e:
                                print(e)
                                pass
                        bar.next()
                    print("\tDone")
                    
                else:
                    for email in self._emails[provider]:
                        self._validated_emails[provider][email] = None

    def save(self,output_location="./output"):
        """Save data

        :param output_location: define output location
        :type output_location: str
        """

        output = {
            "firstname"        : self._user.firstname,
            "middlename"       : self._user.middlename,
            "lastname"         : self._user.lastname,
            "username"         : self._user.username,
            "number"           : self._user.number,
            "localparts"       : self._localparts,
            "emails"           : self._emails,
            "validated_emails" : self._validated_emails,
        }

        # Set the name of the output file
        output_name = f"{self._user.firstname if self._user.firstname else ''}" + \
                      f"{self._user.middlename if self._user.middlename else ''}" + \
                      f"{self._user.lastname if self._user.lastname else ''}"
        output_name = output_name.replace(" ","")

        # Incorrect path
        if not os.path.isdir(output_location) and output_location != "./output":
            print(f"\nNo such directory \'{output_location}\'. Saving in \'./output\'")
            output_location = "./output"

        # Path is "./output" but dir doesn't exist
        if output_location == "./output" and not os.path.isdir("./output"):
            print("Creating directory ./output...",end=" ")
            os.mkdir("./output")

        # Save json to file
        with open((f"{output_location}/{output_name}.json"),"w") as f:
            json.dump(output,f,indent=2)
        print(f"Data successfully saved in \'{output_location}/{output_name}.json\'!")

    def validated_emails_stats(self):
        """To get statistics about emails verified

        :return: number of verified emails, unverified emails, non-existent emails and total of emails
        :rtype: tuple of 4 variables (verified,unverified,nonexistent,nb_emails)
        """
        verified,unverified,nonexistent,nb_emails = 0,0,0,0
        for provider in self._validated_emails:
            for email in self._validated_emails[provider]:
                if self._validated_emails[provider][email] == None: unverified += 1
                elif self._validated_emails[provider][email]: verified += 1
                else: nonexistent += 1
                nb_emails += 1
        return (verified,unverified,nonexistent,nb_emails)

    def verified_emails(self,provider):
        """To get a list of verified emails by provider

        :param provider: select the provider to iter
        :type provider: str

        :return: all verified emails for this provider
        :rtype: list
        """
        return [email for email in self._validated_emails[provider] 
                if self._validated_emails[provider][email]]

    @property
    def localparts(self):
        return self._localparts

    @property
    def emails(self):
        return self._emails

    @property
    def validated_emails(self):
        return self._validated_emails

    @property
    def all_verified_emails(self):
        value = []
        for provider in self._validated_emails:
            value += self.verified_emails(provider)
        return value

    @property
    def level(self):
        return self._localpart_generator.level

    @property
    def separators(self):
        return self._localpart_generator.separators

    @property
    def providers(self):
        return self._email_generator.providers