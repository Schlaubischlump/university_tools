from texttable import Texttable

def print_table(data, header, title):
    """
        :param data: table data
        :param header: table header names
        :param title: table title
        """
    data = list(data)
    if len(data) == 0:
        return

    cols = len(data[0])

    assert len(header) == cols

    table = Texttable()
    table.set_cols_align(["c"]*cols)
    table.set_cols_valign(["m"]*cols)
    table.add_rows([header] + list(data))
    table_str = table.draw()

    table_width = len(table_str.split()[0])
    title_str = f"{title}:".center(table_width)

    print()
    print(title_str)
    print()
    print(table_str)
    print()

__all__ = ["print_table"]
