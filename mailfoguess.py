import os
import json
import argparse
from modules.user import User
from modules.username_generator import UsernameGenerator
from modules.email_generator import EmailGenerator

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
    
    print("\n============= PARAMETERS =============")
    print(f"Generating level : {username_generator.level}")
    print(f"Using separators : {username_generator.separators}")

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
        help="set target\'s firstname",
    )
    parser.add_argument(
        "-m",
        dest="middlename",
        type=str,
        nargs="?",
        default="",
        help="set target\'s middlename",
    )
    parser.add_argument(
        "-l",
        dest="lastname",
        type=str,
        nargs="?",
        default="",
        help="set target\'s lastname",
    )
    parser.add_argument(
        "-u",
        dest="username",
        type=str,
        nargs="?",
        default="",
        help="set target\'s username",
    )
    parser.add_argument(
        "-n",
        dest="number",
        type=str,
        nargs="?",
        default=None,
        help="set a number to use (year of birth, locality...)",
    )
    parser.add_argument(
        "-o",
        dest="output_location",
        type=str,
        nargs="?",
        default="./output/",
        help="choose output location (default is \"./output/\")",
    )
    parser.add_argument(
        "--level",
        dest="level",
        choices=["min","low","high","max"],
        default="min",
        help="choose level of generation (default \'min\')",
    )

    main(parser.parse_args())