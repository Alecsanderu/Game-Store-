""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-crython/inventory/inventory.csv'

INDEX_ID = 0
INDEX_NAME = 1
INDEX_MANUFACTURER = 2
INDEX_PURCHASE_YEAR = 3
INDEX_DURABILITY = 4


def start_module():
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Inventory manager", common.submenu_options(
        "inventory"), "Go back to the main menu")
    while True:
        option = ui.get_inputs(["Please enter a number: "], "")[0]
        if common.check_submenu_option(option) == False:
            ui.print_error_message("Index out of range!\n")
        elif common.check_submenu_option(option) == ValueError:
            ui.print_error_message("Please enter a number!\n")
        else:
            break
    if option == "1":
        add(table)
    elif option == "2":
        while True:
            id_ = ui.get_inputs(["Enter id to remove: "], "")
            if common.check_functions_inputs(id_, table, 0) == False:
                ui.print_error_message(
                    "'{0}' does not exist in your file!".format(id_[0]))
            else:
                break
        remove(table, id_)
    elif option == "3":
        while True:
            id_ = ui.get_inputs(["Enter id to update: "], "")
            if common.check_functions_inputs(id_, table, 0) == False:
                ui.print_error_message(
                    "'{0}' does not exist in your file!".format(id_[0]))
            else:
                break
        update(table, id_)
    elif option == "4":
        year = ui.get_inputs(["Enter year:"], "")
        if type(year) != int:
            ui.print_error_message("Incorrect year")
        else:
            get_available_items(table, year)
    elif option == "5":
        get_average_durability_by_manufacturers(table)
    elif option == "0":
        pass


def show_table(table):
    title_list = ["id", "name", "manufacturer", "purchase_year", "durability"]
    ui.print_table(table, title_list)


def add(table):
    id_ = common.generate_random(table)
    new_element = ui.get_inputs(['Name:', 'Manufacturer:', 'Purchase Year:',
                                 'Durability: Years it can be used'], 'Provide the informations of the new elememnt!')
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


def update(table, id_):
    list_of_imputs = ui.get_inputs(
        ['Please write the position of the item you want to change starting from 1 (wich is title): ', 'Write your change: '], "")
    print(list_of_imputs)
    position = int(list_of_imputs[INDEX_ID])
    new_change = list_of_imputs[1]
    n = len(table)
    for i in range(n):
        if id_[INDEX_ID] == table[i][INDEX_ID]:
            if position == 1:
                table[i][INDEX_NAME] = new_change
            elif position == 2:
                table[i][INDEX_MANUFACTURER] = new_change
            elif position == 3:
                table[i][INDEX_PURCHASE_YEAR] = new_change
            elif position == 4:
                table[i][INDEX_DURABILITY] = new_change
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


# special functions:
# ------------------

def get_available_items(table, year):
    """
    Question: Which items have not exceeded their durability yet (in a given year)?

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        list: list of lists (the inner list contains the whole line with their actual data types)
    """

    specific_products = []
    del(table[0])
    for product in table:
        if int(year[0]) - int(product[INDEX_PURCHASE_YEAR]) < int(product[INDEX_DURABILITY]) and int(year[0]) - int(product[INDEX_PURCHASE_YEAR]) >= 0:
            specific_products.append(product)
    if len(specific_products) > 0:
        ui.print_table(specific_products, [
                       "id", "name", "manufacturer", "purchase_year", "durability"])
    else:
        ui.print_result(
            "All the item from {} have exceeded their durability".format(year[0]), "")
    return specific_products


def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """

    results = {}
    del(table[0])
    for line in table:
        if line[INDEX_MANUFACTURER] not in results.keys():
            count = 1
            results[line[INDEX_MANUFACTURER]] = [
                int(line[INDEX_DURABILITY]), count]
        else:
            results[line[INDEX_MANUFACTURER]][INDEX_ID] += int(line[-1])
            results[line[INDEX_MANUFACTURER]][INDEX_NAME] += 1

    for key in results.keys():
        results[key] = results[key][INDEX_ID] / results[key][INDEX_NAME]

    results_str = str(results)

    ui.print_result(
        results_str.strip("{}").replace(", ", "\n"), "Average durability times for every manufacturer:\n")
