import os
import json
import argparse
from modules.user import User
from modules.localpart_generator import LocalPartGenerator
from modules.email_generator import EmailGenerator

def printBanner():
    for line in open("assets/banner.txt","r"):
        print(line.replace('\n',''))

def main(args):
    printBanner()

    print_more          = args.print_informations
    nb_print_localparts = args.nb_print_localparts
    nb_print_emails     = args.nb_print_emails
    nb_print_verified   = args.nb_print_verified

    if not (args.firstname or args.middlename or args.lastname or args.username):
        print("\nPlease provide indications to generate potentials emails (leave empty for \"None\")")
        firstname  = input("\nFirstname ?\n> ")
        middlename = input("\nMiddlename ?\n> ")
        lastname   = input("\nLastname ?\n> ")
        username   = input("\nUsername ?\n> ")
        number     = input("\nNumber ?\n> ")
        if firstname+middlename+lastname+username == "":
            exit("\nNot enough indications provided. Try [-h] to open the help message.")
    else:
        firstname  = args.firstname
        middlename = args.middlename
        lastname   = args.lastname
        username   = args.username
        number     = args.number
    output_location= args.output_location

    user = User(
        firstname  = firstname,
        middlename = middlename,
        lastname   = lastname,
        username   = username,
        number     = number,
    )

    localpart_generator = LocalPartGenerator(level=args.level)
    email_generator     = EmailGenerator()
    
    print("\n================================ USER ================================")
    user.print()
        
    localparts = localpart_generator.generate(user)
    print("\n============================= LOCAL-PART =============================")
    print(f"Generating level: {localpart_generator.level}")
    print(f"Using separators: {localpart_generator.separators}")
    print(f"Number generated: {len(localparts)} generated")
    if print_more:
        print("Local-parts",end=f" (printing only {nb_print_localparts}):\n - " if len(localparts)>nb_print_localparts else ":\n - ")
        if len(localparts)>nb_print_localparts:
            printable_localparts = localparts[:int(nb_print_localparts/2)] + ["[...]"] + localparts[len(localparts)-int(nb_print_localparts/2):]
        else: printable_localparts = localparts
        print(*printable_localparts,sep="\n - ")

    emails = email_generator.generate(localparts)
    print("\n================================ EMAILS ==============================")
    nb_emails = sum(len(emails[provider]) for provider in emails)
    print(f"Emails      : {nb_emails} generated (with {len(email_generator.providers)} different domains)")
    print(f"Domains used:")
    for provider in email_generator.providers:
        print(f" + {provider} ({len(emails[provider])})",end=":\n\t- " if print_more else "\n")
        if print_more:
            emails_from_provider = [email for email in emails[provider]]
            if len(emails_from_provider)>nb_print_emails:
                printable_emails = emails_from_provider[:int(nb_print_emails/2)] + ["[...]"] + emails_from_provider[len(emails_from_provider)-int(nb_print_emails/2):]
            else: printable_emails = emails_from_provider
            print(*printable_emails,sep="\n\t- ")

    print("\n#~~~~~~~~~~~~~~~~~~~~ VALIDATION ~~~~~~~~~~~~~~~~~~~~#")
    emails = email_generator.validate(emails=emails,validate_all=args.validate_all)

    print("\n#~~~~~~~~~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~~~~~~~~~~#")
    verified, unverified, inexistent, nb_emails = 0,0,0,0
    for provider in emails:
        for email in emails[provider]:
            if emails[provider][email] == None: unverified += 1
            elif emails[provider][email]: verified += 1
            else: inexistent += 1
            nb_emails += 1
    print(f"{verified} verified adress in total on {nb_emails}")
    print(f"{unverified} are unverified and {inexistent} doesn\'t exist")
    if verified:
        print("By provider :")
        for provider in emails:
            verified_emails = [email for email in emails[provider] if emails[provider][email]]
            nb_verified_emails = len(verified_emails)
            if nb_verified_emails:
                print(f" + {provider}: {nb_verified_emails} verified adress found!",end=":\n\t- " if print_more else "\n")
                if print_more:
                    if nb_print_verified:
                        printable_verified = verified_emails[:int(nb_print_emails/2)] + ["[...]"] + verified_emails[nb_verified_emails-int(nb_print_emails/2):]
                    else: printable_verified = verified_emails
                    print(*printable_verified,sep="\n\t- ")

    output = {
        "firstname"   : user.firstname,
        "middlename"  : user.middlename,
        "lastname"    : user.lastname,
        "username"    : user.username,
        "number"      : user.number,
        "local-parts" : localparts,
        "emails"      : emails,
    }
    output_name = f"{user.firstname if user.firstname else ''}" + \
                f"{user.middlename if user.middlename else ''}" + \
                f"{user.lastname if user.lastname else ''}"
    output_name = output_name.replace(" ","")
    if not os.path.isdir(f"{output_location}") and output_location != "./output/":
        print(f"\nNo such directory \'{output_location}\'. Saving in \'./output/\'")
        output_location = "./output/"
    if output_location == "./output/" and not os.path.isdir("./output/"):
        os.mkdir("./output/")
    with open((f"{output_location}/{output_name}.json"),"w") as f:
        json.dump(output,f,indent=2)

if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        description="python script to guess the potentials email adress of someone",
    )

    #~~~~~~~~~~~~~~~~~ TARGET'S PARAMETERS ~~~~~~~~~~~~~~~~~#
    target_informations = arguments.add_argument_group(
        "Target",
        description="Set known parameters concerning the target",
    )
    target_informations.add_argument(
        "-f",
        dest="firstname",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set target\'s firstname",
    )
    target_informations.add_argument(
        "-m",
        dest="middlename",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set target\'s middlename",
    )
    target_informations.add_argument(
        "-l",
        dest="lastname",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set target\'s lastname",
    )
    target_informations.add_argument(
        "-u",
        dest="username",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set target\'s username",
    )
    target_informations.add_argument(
        "-n",
        dest="number",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set a number to use (year of birth, locality...)",
    )

    #~~~~~~~~~~~~~~~~~ GENERATION PARAMETERS ~~~~~~~~~~~~~~~~~#
    generation_parameters = arguments.add_argument_group(
        "Generation",
        description="Set parameters concerning the generation",
    )
    generation_parameters.add_argument(
        "--level",
        dest="level",
        choices=["min","low","high","max"],
        default="min",
        required=False,
        help="choose level of generation (default \'min\')",
    )

    #~~~~~~~~~~~~~~~~~ OUTPUT PARAMETERS ~~~~~~~~~~~~~~~~~#
    output_parameters = arguments.add_argument_group(
        "Output",
        description="Select how the data will be displayed and/or saved",
    )
    output_parameters.add_argument(
        "--print",
        dest="print_informations",
        action="store_true",
        default=False,
        required=False,
        help="print generated informations on screen (local-part, emails and verified emails)",
    )
    output_parameters.add_argument(
        "--nb-localparts",
        dest="nb_print_localparts",
        type=int,
        nargs="?",
        default=20,
        required=False,
        help="set the maximum of local-part printed when informations are displayed"
             " (default is 20)",
    )
    output_parameters.add_argument(
        "--nb-emails",
        dest="nb_print_emails",
        type=int,
        nargs="?",
        default=4,
        required=False,
        help="set the maximum of emails printed per domain when informations are displayed"
             " (default is 4)",
    )
    output_parameters.add_argument(
        "--nb-verified",
        dest="nb_print_verified",
        type=int,
        nargs="?",
        default=None,
        required=False,
        help="set the maximum of verified emails printed per domain when informations are displayed"
             " (default is all)",
    )
    output_parameters.add_argument(
        "--output",
        dest="output_location",
        nargs="?",
        type=str,
        default="./output/",
        required=False,
        help="choose output location (default is \"./output/\")",
    )

    #~~~~~~~~~~~~~~~~~ OPTIONALS PARAMETERS ~~~~~~~~~~~~~~~~~#
    arguments.add_argument(
        "-Y","--yes",
        dest="validate_all",
        action="store_true",
        default=False,
        required=False,
        help="assumes \"yes\" as the answer to all questions of validation",
    )

    main(arguments.parse_args())