""" Human resources module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * birth_year (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-crython/hr/persons.csv'

INDEX_ID = 0
INDEX_NAME = 1
INDEX_BIRTH_YEAR = 2


def start_module():
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Human resources manager", common.submenu_options(
        "hr"), "Go back to the main menu")
    option = ui.get_inputs(["Please enter a number: "], "")[0]
    if option == "1":
        add(table)
    elif option == "2":
        id_ = ui.get_inputs(["Enter id to remove: "], "")
        remove(table, id_)
    elif option == "3":
        id_ = ui.get_inputs(["Enter id to update: "], "")
        update(table, id_)
    elif option == "4":
        get_oldest_person(table)
    elif option == "5":
        get_persons_closest_to_average(table)
    elif option == "0":
        pass


def show_table(table):
    title_list = ["id", "name", "birth_year"]
    ui.print_table(table, title_list)


def add(table):
    id_ = common.generate_random(table)
    new_element = ui.get_inputs(
        ['Name:', 'Birth Year:'], 'Provide the informations of the new elememnt!')
    new_element.insert(INDEX_ID, id_)
    table.append(new_element)
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


def remove(table, id_):
    for line in table:
        if line[INDEX_ID] == id_[INDEX_ID]:
            table.remove(line)
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table

    return table


def update(table, id_):
    list_of_imputs = ui.get_inputs(
        ['Please write the position of the item you want to change starting from 1 (wich is Name): ', 'Write your change: '], "")
    print(list_of_imputs)
    position = int(list_of_imputs[0])
    new_change = list_of_imputs[1]
    n = len(table)
    for i in range(n):
        if id_[INDEX_ID] == table[i][INDEX_ID]:
            if position == 1:
                table[i][INDEX_ID] = new_change
            elif position == 2:
                table[i][INDEX_NAME] = new_change
            elif position == 3:
                table[i][INDEX_BIRTH_YEAR] = new_change
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


# special functions:
# ------------------

def get_oldest_person(table):
    """
    Question: Who is the oldest person?

    Args:
        table (list): data table to work on

    Returns:
        list: A list of strings (name or names if there are two more with the same value)
    """
    del(table[0])
    result = []
    current_oldest = 9999
    for person in table:
        if int(person[INDEX_BIRTH_YEAR]) < int(current_oldest):
            current_oldest = person[INDEX_BIRTH_YEAR]
    for person in table:
        if int(person[INDEX_BIRTH_YEAR]) == int(current_oldest):
            result.append(person[INDEX_NAME])
    ui.print_result(result, "The Oldest:  ")
    return result


def get_persons_closest_to_average(table):
    """
    Question: Who is the closest to the average age?

    Args:
        table (list): data table to work on

    Returns:
        list: list of strings (name or names if there are two more with the same value)
    """

    # your code
    del(table[0])
    names = []
    birth_years = []
    years_sum = 0
    for years in table:
        birth_years.append(years[INDEX_BIRTH_YEAR])
    for element in birth_years:
        years_sum += int(element)
    average_birth_year = round(years_sum / len(birth_years))

    to_compare = abs(int(table[0][INDEX_BIRTH_YEAR]) - average_birth_year)

    for i in range(len(birth_years)):
        element = int(table[i][INDEX_BIRTH_YEAR])
        temp = abs(element - average_birth_year)

        if temp < to_compare:
            to_compare = temp
            names.append(table[i][INDEX_NAME])

    ui.print_result(str(names).strip('[]').replace(
        "'", ""), "Closest to average: ")
