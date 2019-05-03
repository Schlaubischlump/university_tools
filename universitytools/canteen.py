import sys
from enum import Enum
from collections import defaultdict, namedtuple
from xml.etree.ElementTree import fromstring as xml_from_string, ParseError

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class EnumBase(Enum):
    def __str__(self):
        return self.display_name

    def __repr__(self):
        return self.display_name

    def __len__(self):
        return len(self.display_name)

    @property
    def display_name(self):
        return self.name.replace("_", " ").strip()

    @classmethod
    def find_by_value(cls, value):
        if isinstance(value, int):
            for e in cls:
                val = e.value
                # find the correct enum value which is the number
                if isinstance(val, int):
                    if val == value:
                        break
                # find the correct enum value which contains the number
                elif isinstance(val, (list, tuple)):
                    if value in val:
                        break
            else:
                # we did not find a matching value => fallback to default
                val = value
        else:
            # default behavior
            val = value
        return cls(val)


class Mensa(EnumBase):
    Zentralmensa = 310
    Mensaria = 312


class Theke(EnumBase):
    Theke_1 = [110, 112, 113]
    Theke_2 = 120
    Theke_3 = 130
    Theke_4 = [140, 142]
    Wok = [303]
    Tagesessen = [302]
    Snacken = [104]


class Beilagen(EnumBase):
    Tagessuppe = 100
    Eintopf = 102
    Salat = 18
    Beilagen = [200, 202]


URL = "https://www.studierendenwerk-mainz.de/speiseplan/Speiseplan.xml"


def xml_to_dict(ele):
    """
    Convert an xml object to a dictionary structure.
    See: http://stackoverflow.com/a/10077069
    :param ele: xml string
    :return: dictionary from xml
    """
    d = {ele.tag: {} if ele.attrib else None}
    children = list(ele)
    if children:
        dd = defaultdict(list)
        for dc in map(xml_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {ele.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if ele.attrib:
        d[ele.tag].update(('@' + k, v) for k, v in ele.attrib.items())
    if ele.text:
        text = ele.text.strip()
        if children or ele.attrib:
            if text:
                d[ele.tag]['#text'] = text
        else:
            d[ele.tag] = text
    return d


def load_mensa_data(filter_expr=None):
    """
    :param filter_expr: lambda expression to filter the data
    :return generator with date, location, counter, food, price, kind
    """
    try:
        file = urlopen(URL)
        data = file.read()
        xml = xml_from_string(data)
        xml = xml_to_dict(xml)
        rows = xml["DATAPACKET"]["ROWDATA"]["ROW"]

        Entry = namedtuple("Entry", "date location counter food price kind")

        for row in rows:
            date = row["@DATUM"]
            try:
                location = Mensa.find_by_value(int(row["@VERBRAUCHSORT"]))
                counter = Theke.find_by_value(int(row["@TYP"]))
                food = row["@AUSGABETEXT"].strip()
                price = row["@STUDIERENDE"].strip() + "€"
                kind = row["@MENUEKENNZTEXT"].strip()
                res = Entry(date, location, counter, food, price, kind)

                # filter the data based on the given argument
                if filter_expr is None:
                    yield res
                elif filter_expr(res):
                    yield res

            except ValueError:
                # just skip unknown values
                continue
    except ParseError:
        print("Could not read mensa data", file=sys.stderr)
    except Exception as e:
        print("Unknown error: {0}".format(e), file=sys.stderr)


def print_mensa_data(data, header=("Datum", "Ort", "Theke", "Essen", "Preis", "Art")):
    """
    Print the mensa data in a simple table structure.
    :param data: mensa data
    :param header: first header row of the table 
    """
    data = list(data)
    if len(data) == 0:
        return

    cols = len(data[0])

    assert len(header) == cols

    # print the data
    from texttable import Texttable

    table = Texttable()
    table.set_cols_align(["c"]*cols)
    table.set_cols_valign(["m"]*cols)
    table.add_rows([header] + list(data))
    table_str = table.draw()

    table_width = len(table_str.split()[0])
    title = "Speiseplan:".center(table_width)

    print()
    print(title)
    print()
    print(table_str)
    print()
