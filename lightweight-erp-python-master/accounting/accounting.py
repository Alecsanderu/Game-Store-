""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-master/accounting/items.csv'


def start_module():
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Accounting Manager", common.submenu_options("accounting"),
                  "Go back to the main menu")
    option = ui.get_inputs(["Please enter a number: "], "")[0]
    if option == "1":
        add(table)
    elif option == "2":
        id_ = ui.get_inputs(["Enter id to remove: "], "")
        remove(table, id_)
    elif option == "3":
        id_ = ui.get_inputs(["Enter id to update: "], "")
        update(table, id_)


def show_table(table):
    title_list = ["id", "month", "day", "year", "type", "amount"]
    ui.print_table(table, title_list)


def add(table):
    id_ = common.generate_random(table)
    new_element = ui.get_inputs(['Month:', 'Day:', 'Year:', 'Type(in/out):',
                                 'Amount:'], 'Provide the informations of the new elememnt!')
    new_element.insert(0, id_)
    table.append(new_element)
    del(table[0])
    data_manager.write_table_to_file(filename, table)


def remove(table, id_):
    for line in table:
        if line[0] == id_[0]:
            table.remove(line)
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


def update(table, id_):
    list_of_imputs = ui.get_inputs(
        ['Please write the position of the item you want to change starting from 1 (wich is month): ', 'Write your change: '], "")
    print(list_of_imputs)
    position = int(list_of_imputs[0])
    new_change = list_of_imputs[1]
    n = len(table)
    for i in range(n):
        if id_[0] == table[i][0]:
            if position == 1:
                table[i][1] = new_change
            elif position == 2:
                table[i][2] = new_change
            elif position == 3:
                table[i][3] = new_change
            elif position == 4:
                table[i][4] = new_change
            elif position == 5:
                table[i][5] = new_change
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    # your code
    return table


# special functions:
# ------------------

def which_year_max(table):
    """
    Question: Which year has the highest profit? (profit = in - out)

    Args:
        table (list): data table to work on

    Returns:
        number
    """

    # your code


def avg_amount(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        number
    """

    # your code
