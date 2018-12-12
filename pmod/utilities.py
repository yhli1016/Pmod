import sys
import os
import re
from operator import itemgetter


def print_stdout(command):
    """
    Print commands to stdout, which are then interpreted by shell.

    :param command: string, command to be interpreted by shell
    :return: None
    """
    sys.stdout.write("%s\n" % command)
    sys.stdout.flush()


def print_stderr(message):
    """
    Print message to stderr, which WILL NOT be interpreted by shell.
    This function is also used to print banners and tables.

    :param message: string, error message
    :return: None
    """
    sys.stderr.write("%s\n" % message)
    sys.stderr.flush()


def split_list(raw_list, num_group, algorithm="remainder"):
    """
    Split given list into different groups.

    Two algorithms are implemented: by the remainder of the index of each
    element divided by the number of group, or the range of index. For example,
    if we are to split the list of [0, 1, 2, 3] into two groups, by remainder
    we will get [[0, 2], [1, 3]] while by range we will get [[0, 1], [2, 3]].

    :param raw_list: list to split
    :param num_group: integer, number of groups
    :param algorithm: string, should be either "remainder" or "range"
    :return: a list containing the split list
    """
    assert num_group in range(1, len(raw_list)+1)
    assert algorithm in ("remainder", "range")
    num_element = len(raw_list)
    if algorithm == "remainder":
        list_split = [[raw_list[i] for i in range(num_element)
                      if i % num_group == k] for k in range(num_group)]
    else:
        # Get the numbers of items for each group
        num_item = [num_element // num_group for i in range(num_group)]
        for i in range(num_element % num_group):
            num_item[i] += 1
        # Divide the list according to num_item
        list_split = []
        for i in range(num_group):
            j0 = sum(num_item[:i])
            j1 = j0 + num_item[i]
            list_split.append([raw_list[j] for j in range(j0, j1)])
    return list_split


def get_terminal_size():
    """
    Get the current size of the terminal in characters. We cannot use
    os.get_terminal_size() as it is supported only in Python 3.

    :return: (integer, integer), size of the terminal
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def print_banner(banner, columns):
    """
    Print a banner like --------------- FOO ------------------ to stderr.

    The number '2' in this piece of code counts for the two spaces wrapping the
    central text.

    :param banner: the central text in the banner
    :param columns: total width of the banner
    :return: None
    """
    if len(banner) + 2 > columns:
        print_stderr(banner)
    else:
        num_marks_total = columns - len(banner) - 2
        num_marks_left = num_marks_total // 2 
        num_marks_right = num_marks_total - num_marks_left
        banner_with_marks = ""
        mark = "-"
        for i in range(num_marks_left):
            banner_with_marks += mark
        banner_with_marks += " %s " % banner
        for i in range(num_marks_right):
            banner_with_marks += mark
        print_stderr(banner_with_marks)


def print_table(table_head, table_body, number_items=True):
    """
    Print a table to stderr.

    :param table_head: string, head of the table
    :param table_body: list of strings
    :param number_items: boolean, whether to number the items in table_body
    :return: None
    """
    rows, columns = get_terminal_size()

    # Print table head
    print_stderr("")
    print_banner(table_head, columns)

    # Print table body
    if len(table_body) == 0:
        print_stderr("None")
    else:
        # Get the maximum length of string with reserved spaces.
        # DO NOT CHANGE THE NUMBER of RESERVED SPACES.
        max_length = max([len(string) for string in table_body])
        if not number_items:
            max_length += 2
        else:
            max_length += 6

        # Determine the number of columns and rows of the table
        num_table_column = columns // max_length
        num_table_row = len(table_body) // num_table_column
        if len(table_body) % num_table_column > 0:
            num_table_row += 1

        # Break table_body into rows and print
        table_rows = split_list(table_body, num_table_row)
        if not number_items:
            for row in table_rows:
                for string in row:
                    fmt =  "%-" + str(max_length) + "s"
                    sys.stderr.write(fmt % string)
                sys.stderr.write("\n")
            sys.stderr.write("\n")
            sys.stderr.flush()
        else:
            # Determine the dimension of the transposed table, for numbering
            # the items
            table_dim_trans = []
            for i in range(num_table_column):
                if i < len(table_rows[-1]):
                    table_dim_trans.append(num_table_row)
                else:
                    table_dim_trans.append(num_table_row - 1)

            # Print the table with numbered items
            for i, row in enumerate(table_rows):
                for j, string in enumerate(row):
                    fmt = "%4d) %-" + str(max_length-6) + "s"
                    item_number = sum(table_dim_trans[:j]) + i + 1
                    sys.stderr.write(fmt % (item_number, string))
                sys.stderr.write("\n")
            sys.stderr.write("\n")
            sys.stderr.flush()


def print_list(list_head, list_body, number_items=True):
    """
    Prints a list to stderr.

    :param list_head: string, head of the list
    :param list_body: list of strings
    :param number_items: boolean, whether to number the items
    :return:
    """
    sys.stderr.write("%s: " % list_head)
    if len(list_body) == 0:
        sys.stderr.write("None")
    else:
        if number_items:
            for i, item in enumerate(list_body):
                sys.stderr.write("%4d) %s" % (i+1, item))
        else:
            for i, item in enumerate(list_body):
                sys.stderr.write(" %s" % item)
    sys.stderr.write("\n")
    sys.stderr.flush()


def get_latest_version(versions):
    """
    Get the latest version for given software.
    :param versions: list of string, different versions of the software, each
                     version should be in the form of
                     [a-zA-Z0-9]+[-/]+[0-9\.]+.?
    :return: string, the latest version of this software
    """
    # Extract and normalize version numbers from software names
    ver_str = [re.search(r"[0-9\.]+", ver).group().split(".")
               for ver in versions]
    ver_num = [[int(i) for i in ver if i != ""] for ver in ver_str]
    num_digit = max([len(ver) for ver in ver_num])
    for ver in ver_num:
        while len(ver) < num_digit:
            ver.append(0)

    # Sort version numbers
    ver_num = sorted(ver_num, key=itemgetter(slice(0, num_digit, 1)))

    # Get the software name corresponding to the latest version
    latest_version = sorted(versions)[-1]
    for ver_check in versions:
        ver_str_check = re.search(r"[0-9\.]+", ver_check).group().split(".")
        ver_num_check = [int(i) for i in ver_str_check if i != ""]
        while len(ver_num_check) < num_digit:
            ver_num_check.append(0)
        difference = [abs(ver_num_check[i] - ver_num[-1][i])
                      for i in range(num_digit)]
        if sum(difference) == 0:
            latest_version = ver_check
            break
    return latest_version