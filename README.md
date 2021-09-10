# **OSINT TOOL UNDER DEVELOPMENT**

# **COME BACK LATER**

# [Mailfoguess](https://github.com/WildSiphon/Mailfoguess)

**OSINT tool** to **guess** and **verify** the **email address of a person** from  information such as firstname, middlename, lastname, username...    

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4a1.png" alt="bulb" style="zoom:33%;" /> The script

### Operation

An email address is made up from **local-part**, the symbol **@**, and a **domain**. This script does :

- **Create *a lot* of possible local-part** from informations given and following generation level 
- **Add @domain to all local-part** respecting the conditions of creation of mail of these domains
- **Verify these mails** (still working on it but know how to do it)

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f6e0.png" alt="hammer_and_wrench" style="zoom:33%;" /> Installation

### Download files and dependencies

```bash
git clone https://github.com/WildSiphon/Mailfoguess
cd Mailfoguess
pip3 install -r requirements.txt
```

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4c8.png" alt="chart_with_upwards_trend" style="zoom:33%;" />Use

### Usual use

```
usage: mailfoguess.py [-h] [-f [FIRSTNAME]] [-m [MIDDLENAME]] [-l [LASTNAME]] [-u [USERNAME]] [-n [NUMBER]] [-o [OUTPUT_LOCATION]] [--level {min,low,high,max}]

python script to guess the potentials email adress of someone

optional arguments:
  -h, --help            show this help message and exit
  -f [FIRSTNAME]        set target's firstname
  -m [MIDDLENAME]       set target's middlename
  -l [LASTNAME]         set target's lastname
  -u [USERNAME]         set target's username
  -n [NUMBER]           set a number to use (year of birth, locality...)
  -o [OUTPUT_LOCATION]  choose output location (default is "./output/")
  --level {min,low,high,max}
                        choose level of generation (default 'min')
```

**Example**

```bash
~$ python3 mailfoguess.py -f Bill -m "The Gater" -l Gates -u billythekid -n 1955 --level max
```

// EXAMPLE.gif

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4da.png" alt="books" style="zoom:33%;" />Output

Results are displayed in console, but all the informations are recorded and stored by default in `./output/` in a `json` file. This is much more than just what is printed on the terminal.

### Example

`output.json`

```json
{
  "firstname": "bill",
  "middlename": "the gater",
  "lastname": "gates",
  "username": "billythekid",
  "number": [
    "55",
    "1955"
  ],
  "usernames": [
    "b-gater",
    "b-gater-1955",
    "b-gater-55",
    "b-gater-gates",
    "b-gater-gates-1955",
    "b-gater-gates-55",
    "b-gater-gts",
    "b-gater-gts-1955",
    "b-gater-gts-55",
    "b-gates",
    "b-gates-1955",
    "b-gates-55",
    "b-gates-gater",
    "b-gates-gater-1955",
    "b-gates-gater-55",
    "b-gates-the",
    "b-gates-the-1955",
    "b-gates-the-55",
    "b-gates-the-gater",
    "b-gates-the-gater-1955",
    "b-gates-the-gater-55",
    "b-gts",
    "b-gts-1955",
    "b-gts-55",
    "b-gts-gater",
    "b-gts-gater-1955",
    "b-gts-gater-55",
    "b-gts-the",
    "b-gts-the-1955",
    "b-gts-the-55",
    [...]
    "thegates",
    "thegates1955",
    "thegates55",
    "thegatesb",
    "thegatesb1955",
    "thegatesb55",
    "thegatesbill",
    "thegatesbill1955",
    "thegatesbill55",
    "thegbill",
    "thegbill1955",
    "thegbill55",
    "thegts",
    "thegts1955",
    "thegts55",
    "thegtsb",
    "thegtsb1955",
    "thegtsb55",
    "thegtsbill",
    "thegtsbill1955",
    "thegtsbill55"
  ]
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

| Level       | Consequences                                                 |
| ----------- | ------------------------------------------------------------ |
| **Minimal** | user<br><br>first<br>first ° last<br>first ° lini<br>first ° middle ° last<br>first ° middle ° lini<br>fini  ° last<br>fini  ° middle ° last<br><br>last |
| **Low**     | first  ° middle<br>first  ° mini <br>fini   ° middle<br><br>middle<br>middle ° last<br>middle ° lini<br><br>last ° first<br>last ° fini<br>last ° middle<br>last ° first ° middle<br>last ° fini  ° middle<br>lini  ° first ° middle<br>lini  ° first<br>lini  ° middle |
| **High**    | first ° last ° middle<br>first ° last ° mini <br>first ° lini  ° middle<br><br>middle ° first<br>middle ° fini<br>mini     ° first<br>mini     ° last<br><br>last   ° mini<br>last   ° middle ° first<br>last   ° mini     ° first<br>lini    ° middle ° first |
| **Maximal** | first  ° mini ° last<br><br>middle ° first ° last<br>middle ° last  ° first<br>middle ° first ° lini<br>middle ° lini   ° first<br>mini     ° first ° last<br>mini     ° last  ° first<br><br>last ° first ° mini |

+ **{first,middle,last,user}** represents **{firstname,middlename,lastname,username}**
+ **{f,m,l}ini** represents the initials of **f**irstname, **m**iddlename or **l**astname
  + If the name is composed, the initials are the concatenation of all initials' part
+ **°** represent a **separator**

## <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4dd.png" alt="memo" style="zoom:33%;" /> Stuff to add

+ Colors in the printed output (feel free to help me with that)
+ Creation of email (already working on it)
+ Verification on email (already working on it)
+ Option to choose a country to define the list of domains to use 

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
