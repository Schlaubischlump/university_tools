import time
from contextlib import closing
from urllib.request import urlopen

# Take a look at:
# https://github.com/derf/Travel-Status-DE-URA/blob/master/lib/Travel/Status/DE/URA.pm
base_url = "http://ura.itcs.mvg-mainz.de/interfaces/ura/instant_V2"


class MalformedListString(Exception):
    pass


def _split_line(line):
    """
    Split a string or bytes object in the format "["a", "b", "c"]" to a list of it's components.
    :param line: list as string or bytes object
    :return: list of elements
    """
    # convert bytes to a string b
    if isinstance(line, bytes):
        line = line.decode("utf-8")

    # strip leading and trailing whitespaces
    line = line.strip()

    # create a list from the string
    if line[0] == "[" and line[-1] == "]":
        # remove brackets and "" around each element
        return [e[1:-1] if (e[0] == '"' and e[-1] == '"') else e for e in line[1:-1].split(",")]

    # could not parse the line
    raise MalformedListString("Can not parse list string: {0}".format(line))


def get_stations():
    """
    Dictionary with all stations and their corresponding ids.
    :return dict {stationname: stopid}
    """
    station_id_dict = {}
    url = base_url + "?ReturnList=stopid%2Cstoppointname"
    with closing(urlopen(url)) as file:
        # skip first API version line
        next(file)
        # parse each line
        for line in file:
            # DO NOT USE EVAL FOR THIS!! We are reading data straight from a website
            try:
                _, station, sid = _split_line(line)
                station_id_dict[station] = int(sid)
            except Exception as e:
                # ignore invalid lines
                continue
    return station_id_dict


def get_current_connections(station_id):
    """
    :param station_id: station for which all connections should be listed
    :return: [(line number, destination, departure time in minutes), ...]
    """
    connections = []
    url = base_url + f"?ReturnList=lineid%2Cdestinationname%2Cestimatedtime%2Cexpiretime&stopid={station_id}"
    with closing(urlopen(url)) as file:
        # skip first API version line
        next(file)
        # parse each line
        for line in file:
            try:
                _, num, dest, estimate, _ = _split_line(line)
                current_milli_time = int(round(time.time()*1000))
                estimate = round((int(estimate) - current_milli_time) / 60000.0)
                connections.append((int(num), dest, int(estimate)))
            except Exception as e:
                # ignore invalid lines
                continue
    return connections


def print_connections(station, header=["Nr.", "Linie", "Abfahrt in min"]):
    """
    Print the current connections for this station in a tabular.
    :param station: name of the station
    """
    from texttable import Texttable

    stations = get_stations()
    my_station = stations[station]
    connections = get_current_connections(my_station)

    assert len(header) == len(connections[0])

    table = Texttable()
    table.set_cols_align(["c"]*len(header))
    table.set_cols_valign(["m"]*len(header))
    table.add_rows([header] + connections)
    table_str = table.draw()

    table_width = len(table_str.split()[0])
    title = f"{station}:".center(table_width)

    print()
    print(title)
    print()
    print(table_str)
    print()
