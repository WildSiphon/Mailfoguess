# **OSINT TOOL UNDER DEVELOPMENT, COME BACK LATER**

# [Mailfoguess](https://github.com/WildSiphon/Mailfoguess)

**OSINT tool** to **guess** and **verify** the **email address of a person** from  information such as firstname, middlename, lastname, username...    

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4a1.png" alt="bulb" style="zoom:33%;" /> The script

### Operation

An email address is made up from **local-part**, the symbol **@**, and a **domain**. This script does :

- **Create *a lot* of possible local-part** from informations given and following generation level 
- **Add @domain to all local-part** respecting the conditions of creation of mail of these domains
- **Verify these mails** (only for ["gmail","google","laposte","protonmail","yahoo"])

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f6e0.png" alt="hammer_and_wrench" style="zoom:33%;" /> Installation

### Download files and dependencies

```bash
git clone https://github.com/WildSiphon/Mailfoguess
cd Mailfoguess
pip3 install -r requirements.txt
```

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4c8.png" alt="chart_with_upwards_trend" style="zoom:33%;" />Use

### Usual use

```bash
usage: mailfoguess.py [-h] [-f [FIRSTNAME]] [-m [MIDDLENAME]] [-l [LASTNAME]] [-u [USERNAME]] [-n [NUMBER]] [-o [OUTPUT_LOCATION]] [-Y] [--level {min,low,high,max}]

python script to guess the potentials email adress of someone

optional arguments:
  -h, --help            show this help message and exit
  -f [FIRSTNAME]        set target's firstname
  -m [MIDDLENAME]       set target's middlename
  -l [LASTNAME]         set target's lastname
  -u [USERNAME]         set target's username
  -n [NUMBER]           set a number to use (year of birth, locality...)
  -o [OUTPUT_LOCATION]  choose output location (default is "./output/")
  -Y, --yes             assumes "yes" as the answer to all questions of validation
  --level {min,low,high,max}
                        choose level of generation (default 'min')
```

**Examples**

+ Classic use in command line in "no interactions" mod :

```bash
~$ python3 mailfoguess.py -f P* -l C* --yes
```
​	Print in console :

```
[banner]

================================ USER ================================
Firstname  : p*
Lastname   : c*

============================= LOCAL-PART =============================
Number    : 14 generated
Generating level : Minimal
Using separators : ['', '-', '.', '_']

================================ EMAILS ==============================
Emails       : 57 generated (with 5 different domains)
Domains used :
 gmail.com	: 7
 yahoo.com	: 11
 yahoo.fr	: 11
 laposte.net	: 14
 protonmail.com	: 14

#~~~~~~~~~~~~~~~~~~~~ VALIDATION ~~~~~~~~~~~~~~~~~~~~#
> Processing gmail.com (7)...	 |################################| 100.0% - 0s	Done
> Processing yahoo.com (11)...	 |################################| 100.0% - 0s	Done
> Processing yahoo.fr (11)...	 |################################| 100.0% - 0s	Done
> Processing laposte.net (14)...	 |################################| 100.0% - 0s	Done
> Processing protonmail.com (14)...	 |################################| 100.0% - 0s	Done

#~~~~~~~~~~~~~~~~~~~~~ RESULTS ~~~~~~~~~~~~~~~~~~~~~~#
14 verified adress in total on 57
0 are unverified and 43 doesn't exist
By provider :
 gmail.com	: 6 verified adress found!
 protonmail.com	: 8 verified adress found!
```

+ Use in interactions mod (no indications provided to generate potentials emails) :

```bash
$ python3 mailfoguess.py
$ python3 mailfoguess.py --level high
$ python3 mailfoguess.py --yes
```

​	If so, you will be ask about that :

```
[banner]

Please provide indications to generate potentials emails (leave empty for "None")

Firstname ?
> P*

Middlename ?
> 

Lastname ?
> C*

Username ?
> 

Number ?
> 
```

+ To generate and verify the maximum about one person without any interactions. 

```bash
~$ python3 mailfoguess.py -f Bill -m "The Gater" -l Gates -u billythekid -n 1955 --level max --yes
```

​	We strongly recommend that you **do not** do this as the script could last a long time. I tried this one for fun and it took me almost 6 hours to verify 10 000 email address generated from 2300 local-part. 

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4da.png" alt="books" style="zoom:33%;" />Output

Results are displayed in console, but all the informations are recorded and stored by default in `./output/` in a `json` file. This is much more than just what is printed on the terminal.

### Example

`p*c*.json`

```json
{
  "firstname": "p*",
  "middlename": null,
  "lastname": "c*",
  "username": null,
  "number": null,
  "local-parts": [
    "c*",
    "p-c*",
    "p.c*",
    "p_c*",
    "pc*",
    "p*",
    "p*-c",
    "p*-c*",
    "p*.c",
    "p*.c*",
    "p*_c",
    "p*_c*",
    "p*c",
    "p*c*"
  ],
  "emails": {
    "gmail.com": {
      "p.c*@gmail.com": true,
      "pc*@gmail.com": true,
      "p*@gmail.com": false,
      "p*.c@gmail.com": true,
      "p*.c*@gmail.com": true,
      "p*c@gmail.com": true,
      "p*c*@gmail.com": true
    },
    "yahoo.com": {
      "c*@yahoo.com": false,
      "p.c*@yahoo.com": false,
      "p_c*@yahoo.com": false,
      "pc*@yahoo.com": false,
      "p*@yahoo.com": false,
      "p*.c@yahoo.com": false,
      "p*.c*@yahoo.com": false,
      "p*_c@yahoo.com": false,
      "p*_c*@yahoo.com": false,
      "p*c@yahoo.com": false,
      "p*c*@yahoo.com": false
    },
    "yahoo.fr": {
      "c*@yahoo.fr": false,
      "p.c*@yahoo.fr": false,
      "p_c*@yahoo.fr": false,
      "pc*@yahoo.fr": false,
      "p*@yahoo.fr": false,
      "p*.c@yahoo.fr": false,
      "p*.c*@yahoo.fr": false,
      "p*_c@yahoo.fr": false,
      "p*_c*@yahoo.fr": false,
      "p*c@yahoo.fr": false,
      "p*c*@yahoo.fr": false
    },
    "laposte.net": {
      "c*@laposte.net": false,
      "p-c*@laposte.net": false,
      "p.c*@laposte.net": false,
      "p_c*@laposte.net": false,
      "pc*@laposte.net": false,
      "p*@laposte.net": false,
      "p*-c@laposte.net": false,
      "p*-c*@laposte.net": false,
      "p*.c@laposte.net": false,
      "p*.c*@laposte.net": false,
      "p*_c@laposte.net": false,
      "p*_c*@laposte.net": false,
      "p*c@laposte.net": false,
      "p*c*@laposte.net": false
    },
    "protonmail.com": {
      "c*@protonmail.com": false,
      "p-c*@protonmail.com": true,
      "p.c*@protonmail.com": true,
      "p_c*@protonmail.com": true,
      "pc*@protonmail.com": false,
      "p*@protonmail.com": false,
      "p*-c@protonmail.com": true,
      "p*-c*@protonmail.com": true,
      "p*.c@protonmail.com": true,
      "p*.c*@protonmail.com": false,
      "p*_c@protonmail.com": true,
      "p*_c*@protonmail.com": false,
      "p*c@protonmail.com": false,
      "p*c*@protonmail.com": true
    }
  }
}
```

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f39a.png" alt="level_slider" style="zoom:33%;" />Generation level

### Processing each part

Creating lists of names to use based on given names :

| Level       | Consequences                                                 |
| ----------- | ------------------------------------------------------------ |
| **Minimal** | Add an empty name<br><br>If {first,middle,last,user}**name is composed** (ex : Jean-Michel) :<br>   - add each part of the name separatly (ex : ["jean","michel"])<br>   - add the all name separated by each separator (ex : ["jeanmichel","jean-michel"…])<br>   + skipping particles (2 letters word) in all the names except in usernames<br><br>If **name is not composed** :<br>   - add name |
| **Low**     | Add the vowelless lastname where all consonants are unique   |
| **High**    | Add the vowelless lastname where all double consonants are kept |
| **Maximal** |                                                              |

### Generating local-part

+ **{first,middle,last,user}** represents **{firstname,middlename,lastname,username}**
+ **{f,m,l}ini** represents the initials of **f**irstname, **m**iddlename or **l**astname
  + If the name is composed, the initials are the concatenation of all initials' part
+ **°** represent a **separator**

| Level       | Consequences                                                 |
| ----------- | ------------------------------------------------------------ |
| **Minimal** | user<br><br>first<br>first ° last<br>first ° lini<br>first ° middle ° last<br>first ° middle ° lini<br>fini  ° last<br>fini  ° middle ° last<br><br>last |
| **Low**     | first  ° middle<br>first  ° mini <br>fini   ° middle<br><br>middle<br>middle ° last<br>middle ° lini<br><br>last ° first<br>last ° fini<br>last ° middle<br>last ° first ° middle<br>last ° fini  ° middle<br>lini  ° first ° middle<br>lini  ° first<br>lini  ° middle |
| **High**    | first ° last ° middle<br>first ° last ° mini <br>first ° lini  ° middle<br><br>middle ° first<br>middle ° fini<br>mini     ° first<br>mini     ° last<br><br>last   ° mini<br>last   ° middle ° first<br>last   ° mini     ° first<br>lini    ° middle ° first |
| **Maximal** | first  ° mini ° last<br><br>middle ° first ° last<br>middle ° last  ° first<br>middle ° first ° lini<br>middle ° lini   ° first<br>mini     ° first ° last<br>mini     ° last  ° first<br><br>last ° first ° mini |

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4dd.png" alt="memo" style="zoom:33%;" /> Stuff to add

+ Colors in the printed output (feel free to help me with that)
+ ~~Creation of email~~
+ ~~Verification on email~~
+ Add options in command line to change separators and choose providers to use
+ Option to choose a country to define the list of domains

## References

+ This tool which help me to verify email address : https://github.com/megadose/holehe

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
