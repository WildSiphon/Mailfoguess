import os
import json
import argparse

from modules.user import User
from modules.guesser import Guesser

def main(args):

    print_more          = args.print_informations
    nb_print_localparts = args.nb_print_localparts
    nb_print_emails     = args.nb_print_emails
    nb_print_verified   = args.nb_print_verified

    resume = None
    if args.resume_path:
        if os.path.isfile(args.resume_path) and args.resume_path.split(".")[-1]=="json":
            with open(args.resume_path,"r") as f:
                resume = json.load(f)
            nb_emails = sum(len(resume["emails"][provider]) for provider in resume["emails"])
            nb_validated_emails = sum(len(resume["validated_emails"][provider]) for provider in resume["validated_emails"])
            print(f"Resuming file {args.resume_path}:")
            print(f" + {len(resume['localparts'])} localparts already generated")
            print(f" + {nb_emails} emails already generated")
            print(f" + {nb_validated_emails} emails already processed during validation step")
        else:
            exit(f"File {args.resume_path} is not a valid file or doesn\'t exist. Verify file, spelling or extension (must be \'json\').\n")

    if resume:
        firstname  = resume["firstname"]  if resume["firstname"]  else ""
        middlename = resume["middlename"] if resume["middlename"] else ""
        lastname   = resume["lastname"]   if resume["lastname"]   else ""
        username   = resume["username"]   if resume["username"]   else ""
        number     = resume["number"]     if resume["number"]     else ""
    elif not (args.firstname or args.middlename or args.lastname or args.username):
        print("Please provide indications to generate potentials emails (leave empty for \"None\")")
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
        user       = user,
        level      = args.level,
        separators = "-._"+args.separators,
    )

    if resume: guesser.resume(data=resume)

    print("\n================================ USER ================================")
    user.print()
        
    print("\n============================= LOCAL-PART =============================")
    print(f"Generating level: {guesser.level}")
    print(f"Using separators: {guesser.separators}")
    print(f"Number generated: {len(guesser.localparts)} generated in total")
    if print_more and nb_print_localparts!=0:
        print("Local-parts",end=f" (printing only {nb_print_localparts}):\n - " if len(guesser.localparts)>nb_print_localparts else ":\n - ")
        if len(guesser.localparts)>nb_print_localparts:
            printable_localparts = guesser.localparts[:int(nb_print_localparts/2)] + ["..."] + guesser.localparts[len(guesser.localparts)-int(nb_print_localparts/2):]
        else: printable_localparts = guesser.localparts
        print(*printable_localparts,sep="\n - ")

    print("\n================================ EMAILS ==============================")
    nb_emails = sum(len(guesser.emails[provider]) for provider in guesser.emails)
    print(f"Emails      : {nb_emails} generated in total with {len(guesser.providers)} different domains")
    print(f"Domains used:")
    for provider in guesser.providers:
        print(f" + {provider} ({len(guesser.emails[provider])})",end=":\n\t- " if print_more and nb_print_emails!=0 else "\n")
        if print_more and nb_print_emails!=0:
            emails_from_provider = [email for email in guesser.emails[provider]]
            if len(emails_from_provider) > nb_print_emails:
                printable_emails = emails_from_provider[:int(nb_print_emails/2)] + ["..."] + emails_from_provider[len(emails_from_provider)-int(nb_print_emails/2):]
            elif nb_print_emails: printable_emails = emails_from_provider
            print(*printable_emails,sep="\n\t- ")

    print("\n#~~~~~~~~~~~~~~~~~~~~ VALIDATION ~~~~~~~~~~~~~~~~~~~~#")
    try:
        guesser.validate(validate_all=args.validate_all)
    except KeyboardInterrupt as e:
        print("\n[ctrl+c] Script interrupted by user.")
    finally:
        print("\n#~~~~~~~~~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~~~~~~~~~~#")
        stats = guesser.validated_emails_stats()
        print(f"Address processed : {stats[0]}")
        print(f" + verified     : {stats[1]}")
        print(f" + unverified   : {stats[2]}")
        print(f" + non-existent : {stats[3]}")
        if stats[4]:
            print(f" + unprocessed  : {stats[4]}")
        if stats[1]:
            print("By provider :")
            for provider in guesser.validated_emails:
                verified_emails = guesser.verified_emails(provider=provider)
                if verified_emails:
                    print(f" + {provider}: {len(verified_emails)} verified adress found!",end=":\n\t- " if print_more and nb_print_verified!=0 else "\n")
                    if nb_print_verified!=0:
                        print("\t- ",end="")
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
    generation_parameters.add_argument(
        "--resume","-r",
        dest="resume_path",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="select a json file to resume or enrich wich new options",
    )
    generation_parameters.add_argument(
        "--separators","-s",
        dest="separators",
        nargs="?",
        type=str,
        default="",
        required=False,
        help="set separators used for the generation of local-parts (default are \'-._\')",
    )

    #~~~~~~~~~~~~~~~~~ OUTPUT PARAMETERS ~~~~~~~~~~~~~~~~~#
    output_parameters = arguments.add_argument_group(
        "Output",
        description="Select how the data will be displayed and/or saved",
    )
    output_parameters.add_argument(
        "--no-banner",
        dest="nobanner",
        required=False,
        default=False,
        action="store_true",
        help="doesn't display banner",
    )
    output_parameters.add_argument(
        "--print-more","-P",
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


    args = arguments.parse_args()

    if not args.nobanner:
        print(open("assets/banner.txt", "r").read())

    main(args)
