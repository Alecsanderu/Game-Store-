""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-master/store/games.csv'
INDEX_ID = 0
INDEX_TITLE = 1
INDEX_MANUFACTURER = 2
INDEX_PRICE = 3
INDEX_STOCK = 4


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    # your code
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Store manager", common.submenu_options("store"),
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
    elif option == "0":
        pass
    elif option == "4":
        get_counts_by_manufacturers(table)
    elif option == "5":
        manufacturer = ui.get_inputs(["What Manufacturer you want?"], "")
        get_average_by_manufacturer(table, manufacturer)


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """

    # your code
    title_list = ["id", "title", "manufacturer", "price", "in-stock"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    # your code

    id_ = common.generate_random(table)
    new_element = ui.get_inputs(['Game name:', 'Manufacturer:', 'Price:',
                                 'Stock:'], 'Provide the informations of the new elememnt!')
    new_element.insert(INDEX_ID, id_)
    table.append(new_element)
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """

    # your code
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
                table[i][INDEX_TITLE] = new_change
            elif position == 2:
                table[i][INDEX_MANUFACTURER] = new_change
            elif position == 3:
                table[i][INDEX_PRICE] = new_change
            elif position == 4:
                table[i][INDEX_STOCK] = new_change
    del(table[0])
    data_manager.write_table_to_file(filename, table)
    return table


# special functions:
# ------------------

def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """

    # your code
    manufacturer_games_count = {}
    del(table[0])
    for lines in table:
        if lines[INDEX_MANUFACTURER] in manufacturer_games_count:
            manufacturer_games_count[lines[INDEX_MANUFACTURER]] += 1
        else:
            manufacturer_games_count[lines[INDEX_MANUFACTURER]] = 1
    result = ""
    for manufacturer, count in manufacturer_games_count.items():
        result += "{0} : {1} games \n".format(manufacturer, count)

    ui.print_result(result, "Games by:")
    return manufacturer_games_count


def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """

    # your code
    total_items_manufacturer = 0
    total_games_by_manufacturer = 0
    for line in table:
        if manufacturer[INDEX_ID] == line[INDEX_MANUFACTURER]:
            line[INDEX_STOCK] = int(line[INDEX_STOCK])
            total_games_by_manufacturer += line[INDEX_STOCK]
            total_items_manufacturer += 1
    average = total_games_by_manufacturer/total_items_manufacturer
    ui.print_result(average, "Average manufacturer")
    return average
