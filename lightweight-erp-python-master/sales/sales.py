""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
    * customer_id (string): id from the crm
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-crython/sales/sales.csv'
# filename = '/media/alex/e920e2ae-74d4-4835-8814-02915252ed46/Projects/GitHub/lightweight-erp-python-crython/sales/sales2.csv'

INDEX_ID = 0
INDEX_TITLE = 1
INDEX_PRICE = 2
INDEX_MONTH = 3
INDEX_DAY = 4
INDEX_YEAR = 5
INDEX_CUSTOMER = 6


def start_module():
    table = data_manager.get_table_from_file(filename)
    show_table(table)
    ui.print_menu("Sales Manager Menu", common.submenu_options(
        "sales"), "Go back to the main menu")
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
        get_lowest_price_item_id(table)
    elif option == "5":
        month_from = ui.get_inputs(["Month from: "], "")
        day_from = ui.get_inputs(["Day from: "], "")
        year_from = ui.get_inputs(["Year from: "], "")
        answer_1 = common.check_date(month_from[0], day_from[0], year_from[0])
        if answer_1 is not True:
            ui.print_error_message(answer_1)
            exit()
        month_to = ui.get_inputs(["Month to: "], "")
        day_to = ui.get_inputs(["Day to: "], "")
        year_to = ui.get_inputs(["Year to: "], "")
        answer_2 = common.check_date(month_to[0], day_to[0], year_to[0])
        if answer_2 is not True:
            ui.print_error_message(answer_2)

        get_items_sold_between(table, month_from, day_from,
                               year_from, month_to, day_to, year_to)
    elif option == "6":
        id = input("Please Enter ID: ")
        get_title_by_id(id)
    elif option == "7":
        get_item_id_sold_last_from_table(table)
    elif option == "8":
        get_item_title_sold_last_from_table(table)
    elif option == "9":
        item_ids = ui.get_inputs(
            ["Please enter the ID's,separated by comma, to get the sum of the titles assigned to the IDs: "], "")
        splitted_given_ids = item_ids[0].split(",")
        get_the_sum_of_prices_from_table(table, splitted_given_ids)
    elif option == "10":
        sale_id = ui.get_inputs(["Enter Id of Sale:"], "")
        get_customer_id_by_sale_id_from_table(table, sale_id)
    elif option == "11":
        get_all_customer_ids_from_table(table)
    elif option == "12":
        get_all_sales_ids_for_customer_ids_from_table(table)
    elif option == "13":
        get_num_of_sales_per_customer_ids_from_table(table)
    elif option == "0":
        pass


def show_table(table):
    title_list = ["id", "title", "price",
                  "month", "day", "year", "customer_id"]
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
    to_remove = [[]]
    for line in table:
        if int(line[INDEX_YEAR]) < int(year_from[0]) or int(line[INDEX_YEAR]) > int(year_to[0]):
            to_remove.append(line)
        elif int(line[INDEX_YEAR]) == int(year_from[0]) and int(line[INDEX_MONTH]) < int(month_from[0]):
            to_remove.append(line)
        elif int(line[INDEX_YEAR]) == int(year_from[0]) and int(line[INDEX_MONTH]) == int(month_from[0]) and int(line[INDEX_DAY]) < int(day_from[0]):
            to_remove.append(line)
        elif int(line[INDEX_YEAR]) == int(year_to[0]) and int(line[INDEX_MONTH]) > int(month_to[0]):
            to_remove.append(line)
        elif int(line[INDEX_YEAR]) == int(year_to[0]) and int(line[INDEX_MONTH]) == int(month_to[0]) and int(line[4]) > int(day_to[0]):
            to_remove.append(line)

    for line in to_remove:
        if line in table:
            table.remove(line)

    ui.print_result("These are the items sold between your given dates ", "")
    ui.print_table(table, ["id", "title", "price", "month", "day", "year"])
    return table

    # for r in table:
    #     return '%s %s %s %s %s %s' % tuple(r)


# functions supports data analyser
# --------------------------------


def get_title_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the item

    Returns:
        str: the title of the item
    """
    table = data_manager.get_table_from_file(filename)
    for line in table:
        result = "No Title with this ID"
        if line[INDEX_ID] == id:
            result = str(line[INDEX_TITLE])
    ui.print_result(result, f"The Title for {id} is:")


def get_title_by_id_from_table(table, id):
    """
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the sales table
        id (str): the id of the item

    Returns:
        str: the title of the item
    """

    for line in table:
        result = "No Title with this ID"
        if line[INDEX_ID] == id:
            result = str(line[INDEX_TITLE])
    ui.print_result(result, f"The Title for {id} is:")


def get_item_id_sold_last():
    """
    Reads the table with the help of the data_manager module.
    Returns the _id_ of the item that was sold most recently.

    Returns:
        str: the _id_ of the item that was sold most recently.
    """
    table = data_manager.get_table_from_file(filename)
    last_sold_item_id = ""
    dates = []
    for line in table:
        temp = []
        temp.append(int(line[INDEX_YEAR]))
        temp.append(int(line[INDEX_MONTH]))
        temp.append(int(line[INDEX_DAY]))
        dates.append(temp)

    dates = list(reversed(common.sorting_algorithm(dates)))
    print(dates)

    for line in table:
        if dates[0][0] == int(line[INDEX_YEAR]) and dates[0][1] == int(line[INDEX_MONTH]) and dates[0][2] == int(line[INDEX_DAY]):
            last_sold_id = str(line[INDEX_ID])
    ui.print_result(last_sold_id, "This is the ID for the last sold game: ")


def get_item_id_sold_last_from_table(table):
    """
    Returns the _id_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _id_ of the item that was sold most recently.
    """

    last_sold_item_id = ""
    dates = []
    del(table[0])

    dates = []
    for line in table:
        temp = []
        temp.append(int(line[INDEX_YEAR]))
        temp.append(int(line[INDEX_MONTH]))
        temp.append(int(line[INDEX_DAY]))
        dates.append(temp)

    dates = list(reversed(common.sorting_algorithm(dates)))
    print(dates)
    # last_sold_id = None
    for line in table:
        if dates[0][0] == int(line[INDEX_YEAR]) and dates[0][1] == int(line[INDEX_MONTH]) and dates[0][2] == int(line[INDEX_DAY]):
            last_sold_id = str(line[INDEX_ID])
    ui.print_result(last_sold_id, "This is the Id for the last sold game")


def get_item_title_sold_last_from_table(table):
    """
    Returns the _title_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _title_ of the item that was sold most recently.
    """

    last_sold_item_id = ""
    dates = []
    del(table[0])

    dates = []
    for line in table:
        temp = []
        temp.append(int(line[INDEX_YEAR]))
        temp.append(int(line[INDEX_MONTH]))
        temp.append(int(line[INDEX_DAY]))
        dates.append(temp)

    dates = list(reversed(common.sorting_algorithm(dates)))
    print(dates)
    # last_sold_id = None
    for line in table:
        if dates[0][0] == int(line[INDEX_YEAR]) and dates[0][1] == int(line[INDEX_MONTH]) and dates[0][2] == int(line[INDEX_DAY]):
            last_sold_id = str(line[INDEX_TITLE])
    ui.print_result(last_sold_id, "This is the Id for the last sold game")


def get_the_sum_of_prices(item_ids):
    """
    Reads the table of sales with the help of the data_manager module.
    Returns the sum of the prices of the items in the item_ids.

    Args:
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """

    table = data_manager.get_table_from_file(filename)
    sum_of_prices = 0
    for i in range(len(table)):
        if table[i][INDEX_ID] in item_ids:
            sum_of_prices += int(table[i][INDEX_PRICE])
    ui.print_result(sum_of_prices, "Sum of prices: ")


def get_the_sum_of_prices_from_table(table, item_ids):
    """
    Returns the sum of the prices of the items in the item_ids.

    Args:
        table (list of lists): the sales table
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """

    sum_of_prices = 0
    del(table[0])
    for i in range(len(table)):
        if table[i][INDEX_ID] in item_ids:
            sum_of_prices += int(table[i][INDEX_PRICE])
    ui.print_result(sum_of_prices, "Sum of prices: ")


def get_customer_id_by_sale_id(sale_id):
    """
    Reads the sales table with the help of the data_manager module.
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
         sale_id (str): sale id to search for
    Returns:
         str: customer_id that belongs to the given sale id
    """
    table = data_manager.get_table_from_file(filename)
    del(table[0])
    customer_id = ""
    for i in range(len(table)):
        if table[i][INDEX_ID] == sale_id[0]:
            customer_id = str(table[i][INDEX_CUSTOMER])
    ui.print_result(customer_id, f"This is the customer ID for {sale_id}: ")


def get_customer_id_by_sale_id_from_table(table, sale_id):
    """
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
        table: table to remove a record from
        sale_id (str): sale id to search for
    Returns:
        str: customer_id that belongs to the given sale id
    """
    del(table[0])
    customer_id = ""
    for i in range(len(table)):
        if table[i][INDEX_ID] == sale_id[0]:
            customer_id = str(table[i][INDEX_CUSTOMER])
    ui.print_result(customer_id, f"This is the customer ID for {sale_id}: ")


def get_all_customer_ids():
    """
    Reads the sales table with the help of the data_manager module.

    Returns:
         set of str: set of customer_ids that are present in the table
    """
    table = data_manager.get_table_from_file(filename)
    customer_ids = set()
    del(table[0])
    for line in table:
        customer_ids.add(line[INDEX_CUSTOMER])
    ui.print_result(customer_ids, "Customers IDs:")


def get_all_customer_ids_from_table(table):
    """
    Returns a set of customer_ids that are present in the table.

    Args:
        table (list of list): the sales table
    Returns:
         set of str: set of customer_ids that are present in the table
    """
    customer_ids = set()
    del(table[0])
    for line in table:
        customer_ids.add(line[INDEX_CUSTOMER])
    ui.print_result(customer_ids, "Customers IDs:")


def get_all_sales_ids_for_customer_ids():
    """
    Reads the customer-sales association table with the help of the data_manager module.
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)

    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
            all the sales id belong to the given customer_id
    """
    table = data_manager.get_table_from_file(filename)
    customer_id = set()
    sale_id_for_customer_id = {}
    del(table[0])
    for line in table:
        customer_id.add(line[INDEX_CUSTOMER])
    for item in customer_id:
        sale_id_for_customer_id[item] = []
    for line in table:
        actual_v = sale_id_for_customer_id[line[INDEX_CUSTOMER]]
        actual_v.append(line[INDEX_ID])
        sale_id_for_customer_id[line[INDEX_CUSTOMER]] = actual_v
    result = ""
    for cust_id, sale_id in sale_id_for_customer_id.items():
        result += "{} : {}  \n".format(cust_id, sale_id)
    ui.print_result(result, "Sales ID For Customers ID:")


def get_all_sales_ids_for_customer_ids_from_table(table):
    """
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Args:
        table (list of list): the sales table
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """

    customer_id = set()
    sale_id_for_customer_id = {}
    del(table[0])
    for line in table:
        customer_id.add(line[INDEX_CUSTOMER])
    for item in customer_id:
        sale_id_for_customer_id[item] = []
    for line in table:
        actual_v = sale_id_for_customer_id[line[INDEX_CUSTOMER]]
        actual_v.append(line[INDEX_ID])
        sale_id_for_customer_id[line[INDEX_CUSTOMER]] = actual_v
    result = ""
    for cust_id, sale_id in sale_id_for_customer_id.items():
        result += "{} : {}  \n".format(cust_id, sale_id)
    ui.print_result(result, "Sales ID For Customers ID:")


def get_num_of_sales_per_customer_ids():
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    table = data_manager.get_table_from_file(filename)
    del(table[0])
    sales_id = {}
    for line in table:
        sales_id[line[INDEX_CUSTOMER]] = sales_id.get(line[INDEX_CUSTOMER], 0) + 1
    ui.print_result(sales_id, "Number of sale per Customer ID:")


def get_num_of_sales_per_customer_ids_from_table(table):
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    del(table[0])
    sales_id = {}
    for line in table:
        sales_id[line[INDEX_CUSTOMER]] = sales_id.get(line[INDEX_CUSTOMER], 0) + 1
    ui.print_result(sales_id, "Number of sale per Customer ID:")
