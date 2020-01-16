""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-master/sales/sales.csv'
INDEX_ID = 0
INDEX_TITLE = 1
INDEX_PRICE = 2
INDEX_MONTH = 3
INDEX_DAY = 4
INDEX_YEAR = 5


def start_module():
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Sales Manager Menu", common.submenu_options("sales"),
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
        get_lowest_price_item_id(table)
    elif option == "5":
        month_from = ui.get_inputs(["Month from: "], "")
        day_from = ui.get_inputs(["Day from: "], "")
        year_from = ui.get_inputs(["Year from: "], "")
        answer_1 = common.check_date(month_from[0], day_from[0], year_from[0])
        if answer_1 is not True:
            ui.print_error_message(answer_1)
        month_to = ui.get_inputs(["Month to: "], "")
        day_to = ui.get_inputs(["Day to: "], "")
        year_to = ui.get_inputs(["Year to: "], "")
        answer_2 = common.check_date(month_to[0], day_to[0], year_to[0])
        if answer_2 is not True:
            ui.print_error_message(answer_2)
        get_items_sold_between(table, month_from, day_from,
                               year_from, month_to, day_to, year_to)


def show_table(table):
    title_list = ["id", "title", "price", "month", "day", "year"]
    ui.print_table(table, title_list)


def add(table):
    id_ = common.generate_random(table)
    new_element = ui.get_inputs(['Title:', 'Price:', 'Month:', 'Day:',
                                 'Year:'], 'Provide the informations of the new elememnt!')
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
    new_change = list_of_imputs[INDEX_TITLE]
    n = len(table)
    for i in range(n):
        if id_[INDEX_ID] == table[i][INDEX_ID]:
            if position == 1:
                table[i][INDEX_TITLE] = new_change
            elif position == 2:
                table[i][INDEX_PRICE] = new_change
            elif position == 3:
                table[i][INDEX_MONTH] = new_change
            elif position == 4:
                table[i][INDEX_DAY] = new_change
            elif position == 5:
                table[i][INDEX_YEAR] = new_change
    del(table[0])
    data_manager.write_table_to_file(filename, table)


# special functions:
# ------------------

def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title

    Args:
        table (list): data table to work on

    Returns:
         string: id
    """

    del(table[0])
    actual_id = None
    first_price = int(table[INDEX_ID][INDEX_PRICE])
    for i in table:
        actual_price = int(i[INDEX_PRICE])
        if actual_price < first_price:
            first_price = actual_price
            actual_id = i[INDEX_ID]
    result = actual_id

    ui.print_result(
        result, "The id of the item that was sold for the lowest price:")
    # return result


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)

    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)

    Returns:
        list: list of lists (the filtered table)
    """

    # your code
    del(table[0])
    for line in table:
        if int(line[INDEX_YEAR]) < int(year_from[0]) or int(line[INDEX_YEAR]) > int(year_to[0]):
            table.remove(line)
        elif int(line[INDEX_YEAR]) == int(year_from[0]) and int(line[INDEX_MONTH]) < int(month_from[0]):
            table.remove(line)
        elif int(line[INDEX_YEAR]) == int(year_from[0]) and int(line[INDEX_MONTH]) == int(month_from[0]) and int(line[INDEX_DAY]) < int(day_from[0]):
            table.remove(line)
        elif int(line[INDEX_YEAR]) == int(year_to[0]) and int(line[INDEX_MONTH]) > int(month_to[0]):
            table.remove(line)
        elif int(line[INDEX_YEAR]) == int(year_to[0]) and int(line[INDEX_MONTH]) == int(month_to[0]) and int(line[4]) > int(day_to[0]):
            table.remove(line)

    # for r in table:
    #     return '%s %s %s %s %s %s' % tuple(r)
    ui.print_result("This is the list of games", "")
    ui.print_table(table, ["id", "title", "price", "month", "day", "year"])
