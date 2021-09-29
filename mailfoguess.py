import argparse
from modules.user import User
from modules.guesser import Guesser

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
            exit("\nNot enough indications provided. Try [-h] to show options available.")
    else:
        firstname  = args.firstname
        middlename = args.middlename
        lastname   = args.lastname
        username   = args.username
        number     = args.number

    user = User(
        firstname  = firstname,
        middlename = middlename,
        lastname   = lastname,
        username   = username,
        number     = number,
    )
    guesser = Guesser(
        user  = user,
        level = args.level,
    )
    
    print("\n================================ USER ================================")
    user.print()
        
    print("\n============================= LOCAL-PART =============================")
    print(f"Generating level: {guesser.level}")
    print(f"Using separators: {guesser.separators}")
    print(f"Number generated: {len(guesser.localparts)} generated")
    if print_more:
        print("Local-parts",end=f" (printing only {nb_print_localparts}):\n - " if len(guesser.localparts)>nb_print_localparts else ":\n - ")
        if len(guesser.localparts)>nb_print_localparts:
            printable_localparts = guesser.localparts[:int(nb_print_localparts/2)] + ["..."] + guesser.localparts[len(guesser.localparts)-int(nb_print_localparts/2):]
        else: printable_localparts = guesser.localparts
        print(*printable_localparts,sep="\n - ")

    print("\n================================ EMAILS ==============================")
    nb_emails = sum(len(guesser.emails[provider]) for provider in guesser.emails)
    print(f"Emails      : {nb_emails} generated (with {len(guesser.providers)} different domains)")
    print(f"Domains used:")
    for provider in guesser.providers:
        print(f" + {provider} ({len(guesser.emails[provider])})",end=":\n\t- " if print_more else "\n")
        if print_more:
            emails_from_provider = [email for email in guesser.emails[provider]]
            if len(emails_from_provider)>nb_print_emails:
                printable_emails = emails_from_provider[:int(nb_print_emails/2)] + ["..."] + emails_from_provider[len(emails_from_provider)-int(nb_print_emails/2):]
            else: printable_emails = emails_from_provider
            print(*printable_emails,sep="\n\t- ")

    print("\n#~~~~~~~~~~~~~~~~~~~~ VALIDATION ~~~~~~~~~~~~~~~~~~~~#")
    try:
        guesser.validate(validate_all=args.validate_all)
    except KeyboardInterrupt as e:
        print("\n[ctrl+c] Script interrupted by user.")
    finally:
        print("\n#~~~~~~~~~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~~~~~~~~~~#")
        verified,unverified,nonexistent,nb_emails = guesser.validated_emails_stats()
        print(f"Address processed  : {nb_emails}")
        print(f" + verified     : {verified}")
        print(f" + unverified   : {unverified}")
        print(f" + non-existent : {nonexistent}")
        if verified:
            print("\nBy provider :")
            for provider in guesser.validated_emails:
                verified_emails = guesser.verified_emails(provider=provider)
                if len(verified_emails):
                    print(f" + {provider}: {len(verified_emails)} verified adress found!",end=":\n\t- " if print_more else "\n")
                    if print_more:
                        if nb_print_verified:
                            printable_verified = verified_emails[:int(nb_print_emails/2)] + ["..."] + verified_emails[len(verified_emails)-int(nb_print_emails/2):]
                        else: printable_verified = verified_emails
                        print(*printable_verified,sep="\n\t- ")
        print()

        guesser.save(output_location=args.output_location)

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
        "--yes","-Y",
        dest="validate_all",
        action="store_true",
        default=False,
        required=False,
        help="assumes \"yes\" as the answer to all questions of validation",
    )
    generation_parameters.add_argument(
        "--level","-L",
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
        "--print","-P",
        dest="print_informations",
        action="store_true",
        default=False,
        required=False,
        help="print generated informations on screen (local-part, emails and verified emails)",
    )
    output_parameters.add_argument(
        "--output","-O",
        dest="output_location",
        nargs="?",
        type=str,
        default="./output",
        required=False,
        help="choose output location (default is \"./output\")",
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

    #~~~~~~~~~~~~~~~~~ OPTIONALS PARAMETERS ~~~~~~~~~~~~~~~~~#

    main(arguments.parse_args())