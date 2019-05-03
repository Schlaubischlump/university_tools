# Tools:

This repository contains personal scripts used to make my life at the University of Mainz (JGU) easier. These scripts require `python3.6` and up.

## Mensa
```
usage: mensa [-h] [-k {vegan,veggi,vital,all}] [-d {past,today,upcoming,all}]
             [-c {Theke 1,Theke 2,Theke 3,Theke 4,Wok,Tagesessen,Snacken,all}]
             [-l {Zentralmensa,Mensaria,all}] [-p PRICE] [-f FOOD]

Mensa Speiseplan

optional arguments:
  -h, --help            show this help message and exit
  -k {vegan,veggi,vital,all}, --kind {vegan,veggi,vital,all}
                        Only list food of a special kind.
  -d {past,today,upcoming,all}, --date {past,today,upcoming,all}
                        List only foods for today or upcoming days.
  -c {Theke 1,Theke 2,Theke 3,Theke 4,Wok,Tagesessen,Snacken,all}, --counter {Theke 1,Theke 2,Theke 3,Theke 4,Wok,Tagesessen,Snacken,all}
                        Only list a specific counter.
  -l {Zentralmensa,Mensaria,all}, --location {Zentralmensa,Mensaria,all}
                        List only food for a special location.
  -p PRICE, --price PRICE
                        Set a upper price limit as float.
  -f FOOD, --food FOOD  Regex to only match certain foods.
```

## Fahrplan

```
usage: fahrplan [-h] [-e ESTIMATE] [-s STATION]

Fahrplanauskunft

optional arguments:
  -h, --help            show this help message and exit
  -e ESTIMATE, --estimate ESTIMATE
                        only show connections in the next ESTIMATE minutes

required named arguments:
  -s STATION, --station STATION
                        show all connections for this station
```

## Noten
```
usage: noten [-h] [-t TERM] [-l] [-s] [-u USER]

Grades from Jogustine

optional arguments:
  -h, --help            show this help message and exit
  -t TERM, --term TERM  Only show grades for a specific term (The default is
                        'latest' for the current term).
  -l, --list            Show all terms.
  -s, --save-password   Save and store the current credentials in a keychain.

required named arguments:
  -u USER, --user USER  Use a specific user for the login.
```

# Installation:
```
pip3 install git+https://github.com/Schlaubischlump/university_tools
```

# Credits:
Special thanks goes to [gusser93](https://github.com/Gusser93?tab=repositories) !