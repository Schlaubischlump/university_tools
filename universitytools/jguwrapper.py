import sys
import datetime

import requests
from bs4 import BeautifulSoup

from universitytools import print_table

# --------------------------------------------------------
# --------------------- Exceptions -----------------------
# --------------------------------------------------------

class LoginFailedException(Exception):
    pass


# --------------------------------------------------------
# ----------------- Helper classes -----------------------
# --------------------------------------------------------

class Term(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Modul(object):
    def __init__(self):
        self.name = ""
        self.lectures = []


class Lecture(object):
    def __init__(self):
        self.name = ""
        self.modul = None
        self.exam = None
        self.semester = None


class Exam(object):
    def __init__(self):
        self.name = ""
        self.number = None
        self.kind = None
        self.weight = None
        self.grade = None
        self.term = None
        self.status = None
        self.date = None

# --------------------------------------------------------
# ---------------------- Config --------------------------
# --------------------------------------------------------

parser = "html.parser" #"lxml"

# --------------------------------------------------------
# ------------------------ URLs --------------------------
# --------------------------------------------------------
all_terms_code = "999"

base_url = "https://jogustine.uni-mainz.de"
script_url = base_url + "/scripts/mgrqispi.dll"
url_scheme = script_url + "?APPNAME=CampusNet&PRGNAME=EXAMRESULTS&ARGUMENTS=-N{0},-N000350,-N{1}"


# --------------------------------------------------------
# --------------------- Parsing --------------------------
# --------------------------------------------------------

def login(user, password):
    req_headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "keep-alive",
                   "Upgrade-Insecure-Requests": "1",
                   "Host": "jogustine.uni-mainz.de",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Referer": script_url + "?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000265,-Awelcome",
                    "DNT": "1"
    }
    form_data = {"usrname": user,
        "pass": password,
        "APPNAME": "CampusNet",
        "PRGNAME": "LOGINCHECK",
        "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
        "clino": "000000000000001",
        "menuno": "000265",
        "menu_type": "classic",
        "browser": "",
        "platform": ""
    }

    session = requests.Session()
    try:
        r_post = session.post(script_url, headers=req_headers, data=form_data, allow_redirects=True)
        if r_post.status_code is not 200:
            raise requests.exceptions.RequestException("login failed! ")
        session_no = r_post.headers["REFRESH"][86:101]
    except KeyError as keyError:
        raise LoginFailedException("[ERROR] - Key error occured {0}".format(keyError))
    except TypeError as typeError:
        raise LoginFailedException("[ERROR] - Type error occured {0}".format(typeError))
    except requests.exceptions.RequestException as exception:
        raise LoginFailedException("[ERROR] - Exception occured {0}".format(exception))
    return session, session_no


def get_terms(session, session_no):
    """
    :param session: current session
    :param session_no: current session number
    :return: list with all terms
    """
    url = url_scheme.format(session_no, all_terms_code)
    res = session.get(url)
    res.encoding = "utf-8"
    html = BeautifulSoup(res.text.replace("<br />", "\n"), parser)
    term_tags = html.find("select", id="semester").find_all("option")

    # load all terms
    terms = []
    for s in term_tags:
        if s["value"] != all_terms_code:
            term = Term(name=s.string, code=s["value"])
            terms.append(term)
    return terms


def get_exam_results(session, session_no, terms):
    """
    :param: session
    :return: list with exam objects for each exam result
    """
    results = []

    for term in terms:
        url = url_scheme.format(session_no, term.code)
        res = session.get(url)
        res.encoding = "utf-8"
        html = BeautifulSoup(res.text.replace("<br />", "\n"), parser)
        selection = html.find("tbody").find_all("tr")

        # get results
        for row in selection:
            # parse information string
            entry = row.find_all("td")
            exam_info = [l.strip() for l in entry[0].text.splitlines()][1:-6]
            date = entry[1].get_text(strip=True)

            # create exam object
            ex = Exam()
            ex.name = exam_info[1]
            ex.number = exam_info[0]
            ex.kind, ex.weight = [info for info in exam_info[2].rsplit(None, 1)]
            ex.date = "" if date == "" else datetime.datetime.strptime(date, "%d.%m.%Y").date()
            ex.grade = entry[2].get_text(strip=True)
            ex.term = term
            ex.status = entry[3].get_text(strip=True)

            results.append(ex)

    return results

def print_terms(data):
    print_table([(t.code, t.name) for t in data], ["Nr.", "Name"], title="Semester:")

def print_exam_results(data, title="Ergebnisse:"):
    print_table(data=[(e.name, str(e.date), e.grade, e.status) for e in data],
                header=["Name", "Datum", "Note", "Status"],
                title=title)
