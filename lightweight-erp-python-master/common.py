""" Common module
implement commonly used functions here
"""

import random


def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation:
         - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letter
         - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """

    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    lowers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    specials = ['§', '+', '!', '%', '/', '=', '(', ')', '~', 'ˇ', 'ˇ', '^', '˘', '°', '|', 'Ä', '€',
                'Í', '÷', '×', 'ä', 'đ', 'Đ', 'í', 'ł', 'Ł', '$', 'ß', '¤', '<', '>', '#', '&', '@', '.']
    characters = [nums, lowers, uppers, specials]
    generated = ''
    for character in characters:
        generated += random.choice(character)
        generated += random.choice(character)
    generated = ''.join(random.sample(generated, len(generated)))

    for lines in table:
        if lines[0] == generated:
            return generate_random(table)
    return generated

    # your code


def submenu_options(module):
    options = ["Add", "Remove", "Update"]
    if module == "store":
        options.append(
            "How many different kinds of game are available of each manufacturer?")
        options.append(
            "What is the average amount of games in stock of a given manufacturer?")
    elif module == "sales":
        options.append(
            "What is the id of the item that was sold for the lowest price?")
        options.append("Which items are sold between two given dates?")
    elif module == "inventory":
        options.append(
            "Which items have not exceeded their durability yet (in a given year)?")
        options.append(
            "What are the average durability times for each manufacturer?")
    elif module == "hr":
        options.append("Who is the oldest person?")
        options.append("Who is the closest to the average age?")

    return options


def check_submenu_option(option):
    options = [1, 2, 3, 4, 5]
    try:
        if int(option) not in options:
            return False
        else:
            return True
    except ValueError as error:
        return ValueError


def check_functions_inputs(element, table, column):
    item_list = [item[column] for item in table]
    if element[0] not in item_list:
        return False
    else:
        return True


def check_date(month, day, year):
    month = int(month)
    day = int(day)
    year = int(year)

    if year > 2020:
        return "at least one date error -> The current year is 2020! The year input must be below 2020!"

    if year % 4 != 0:
        year = "common year"
    elif year % 100 != 0:
        year = "leap year"
    elif year % 400 != 0:
        year = "common year"
    else:
        year = "leap year"

    months_30_days = [4, 6, 9, 11]
    months_31_days = [1, 3, 5, 7, 8, 10, 12]
    february = [2]
    all_months = months_30_days + months_31_days + february

    if month not in all_months:
        return "at least one date error -> Month input must be between 1 and 12!"
    elif month in all_months:
        if day <= 31 and day >= 1:
            if month in months_30_days:
                if day == 31:
                    return "at least one date error -> You have entered a 30 days month!"
                else:
                    return True
            elif month in february:
                if year == "leap year" and day > 29:
                    return "at least one date error -> You have entered February in a leap year, so the day input must be between 1 and 29!"
                elif year == "common year" and day > 28:
                    return "at least one date error -> You have entered February in a common year, so the day input must be between 1 and 28!"
                else:
                    return True
            else:
                return True
        else:
            return "at least one date error -> Day input must be between 1 and 31"
