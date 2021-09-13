import os
import json
import argparse
from modules.user import User
from modules.username_generator import UsernameGenerator
from modules.email_generator import EmailGenerator
<<<<<<< HEAD

NB_PRINT_USERNAME = 100
NB_PRINT_EMAIL = 50
=======
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c

def printBanner():
    for line in open("assets/banner.txt","r"):
        print(line.replace('\n',''))

def main(args):
    printBanner()

    if (args.firstname+args.middlename+args.lastname+args.username) == "":
        print("\nPlease provide indications to generate potentials emails (leave empty for \"None\")")
        firstname  = input("\nFirstname ?\n> ")
        middlename = input("\nMiddlename ?\n> ")
        lastname   = input("\nLastname ?\n> ")
        username   = input("\nUsername ?\n> ")
        number     = input("\nNumber ?\n> ")
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

    username_generator = UsernameGenerator(level=args.level)
    email_generator    = EmailGenerator()
    
    print("\n================================ USER ================================")
    user.print()
        
    usernames = username_generator.generate(user)
    print("\n============================= LOCAL-PART =============================")
    print(f"Number    : {len(usernames)} generated")
    print(f"Generating level : {username_generator.level}")
    print(f"Using separators : {username_generator.separators}")
    # print("Usernames",end=" ")
    # print(
    #     f'(only the first {NB_PRINT_USERNAME}) ' if len(usernames)>NB_PRINT_USERNAME else '',
    #     end=": "
    # )
    # printable_usernames = usernames[:NB_PRINT_USERNAME]
    # print(*printable_usernames,sep=", ",end=" [...]\n" if len(usernames)>NB_PRINT_USERNAME else '\n')

<<<<<<< HEAD
    emails = email_generator.generate(usernames)
    print("\n================================ EMAILS ==============================")
    print(f"Emails       : {sum(len(domain) for domain in emails)} generated (with {len(email_generator.providers)} different domains)")
    print(f"Domains used :")
    for provider in email_generator.providers:
        print(f" {provider} \t: {len(emails[provider])}")
    # print(
    #     f"Emails (only the first {NB_PRINT_EMAIL})" if len(usernames)>NB_PRINT_EMAIL else "Emails",
    #     end=" : "
    # )
    # printable_emails = [email for email in emails[provider] for provider in emails][:NB_PRINT_EMAIL]
    # print(*printable_emails,sep=", ",end=" [...]\n" if len(emails)>NB_PRINT_EMAIL else '\n')

    print("\n\t#~~~~~~~~~~~~~~~~~~~~ VALIDATION ~~~~~~~~~~~~~~~~~~~~#")
    for provider in email_generator.providers:
        if args.validate_all: answer = "y"
        else:
            answer = input(f"\n\t Would you like to verify {provider} ({len(emails[provider])}) [N/y] ")
        
        if answer in ["y","Y","yes","Yes","yEs","yeS","YEs","YeS","yES","YES"]:
            emails[provider] = email_generator.validate(emails[provider],provider=provider)

    print("\n\t#~~~~~~~~~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~~~~~~~~~~#")
    print(*emails,sep=", ")

    output = {
        "firstname"   : user.firstname,
        "middlename"  : user.middlename,
        "lastname"    : user.lastname,
        "username"    : user.username,
        "number"      : user.number,
        "local-parts" : usernames,
        "emails"      : emails,
    }
    output_name = (user.firstname+user.middlename+user.lastname).replace(" ","")
    if not os.path.isdir(f"{output_location}") and output_location != "./output/":
        print(f"\nNo such directory \'{output_location}\'. Saving in \'./output/\'")
        output_location = "./output/"
    if output_location == "./output/" and not os.path.isdir("./output/"):
        os.mkdir("./output/")
    with open((f"{output_location}/{output_name}.json"),"w") as f:
        json.dump(output,f,indent=2)
=======
    print("\n================ USER ================")
    user.print()
        
    usernames = username_generator.generate(user)
    print("\n============== USERNAMES =============")
    print(f"Number    : {len(usernames)} usernames")
    print(f"Usernames {'(only the first 100) ' if len(usernames)>100 else ''}:",end="\n\t")
    printable_usernames = usernames[:100]
    print(*printable_usernames,sep=", ",end=" [...]\n" if len(usernames)>100 else '\n')

    emails = email_generator.generate(usernames)
    print("\n================ EMAILS ==============")
    print(f"Number       : {len(emails)} emails with {len(email_generator.providers)} different domains")
    print(f"Domains used : {', '.join(email_generator.providers)}")
    #print(*emails,sep="\n")

    # output = {
    #     "firstname"  : user.firstname,
    #     "middlename" : user.middlename,
    #     "lastname"   : user.lastname,
    #     "username"   : user.username,
    #     "number"     : user.number,
    #     "usernames"  : usernames,
    # }
    # output_name = (user.firstname+user.middlename+user.lastname).replace(" ","")
    # if not os.path.isdir(f"{output_location}") and output_location != "./output/":
    #     print(f"\nNo such directory \'{output_location}\'. Saving in \'./output/\'")
    #     output_location = "./output/"
    # if output_location == "./output/" and not os.path.isdir("./output/"):
    #     os.mkdir("./output/")
    # with open((f"{output_location}/{output_name}.json"),"w") as f:
    #     json.dump(output,f,indent=2)
>>>>>>> 6bc37d2a6d34678c1e3fe0a0417ceba63461da3c

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="python script to guess the potentials email adress of someone",
    )
    parser.add_argument(
        "-f",
        dest="firstname",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="set target\'s firstname",
    )
    parser.add_argument(
        "-m",
        dest="middlename",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="set target\'s middlename",
    )
    parser.add_argument(
        "-l",
        dest="lastname",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="set target\'s lastname",
    )
    parser.add_argument(
        "-u",
        dest="username",
        type=str,
        nargs="?",
        default="",
        required=False,
        help="set target\'s username",
    )
    parser.add_argument(
        "-n",
        dest="number",
        type=str,
        nargs="?",
        default=None,
        required=False,
        help="set a number to use (year of birth, locality...)",
    )
    parser.add_argument(
        "-o",
        dest="output_location",
        nargs="?",
        type=str,
        default="./output/",
        required=False,
        help="choose output location (default is \"./output/\")",
    )
    parser.add_argument(
        "--level",
        dest="level",
        choices=["min","low","high","max"],
        default="min",
        required=False,
        help="choose level of generation (default \'min\')",
    )
    parser.add_argument(
        "--all",
        dest="validate_all",
        action="store_true",
        default=False,
        required=False,
        help="validate directly without asking the emails generated",
    )

    main(parser.parse_args())