#inventory.py
#This script manages inventory as dictionary
#It allows:
#   - showing inventory both as a table and in a simplified version
#   - adding loot as a list
#   - import and export from and to a .csv file
# Script generates errors log, if import errors are found


def display_inventory(inventory):
    """Function to show inventory content in a simplified version"""
    print("Inventory:")
    for item in inventory: #prints every value and key(item) in inventory dict
        print(inventory[item], item)
    print(total_items_count(inventory)) #generates a text line with summed items (with default text defined in function argument)


def total_items_count(inv_to_count, total_text="Total number of items: "):
    """Function that summes up the values of all items in inventory. Default text is declared
       in argument, but can be changed in easy way by adding the second argument.
       In this version of program it is possible to use non-integer floats as values,
       so if a float is used, the total sum will be float too. """
    total_items_sum = 0
    for item in inv_to_count: #loop to sum items values (float format)
        total_items_sum = total_items_sum + float(inv_to_count[item])
    if total_items_sum.is_integer(): #if sum in float is an integer, the sum will change to int format
        total_items_sum = int(total_items_sum)
    total_items_sum = str(total_items_sum)
    total_text_with_sum = total_text + total_items_sum + "\n" #final text
    return total_text_with_sum


def add_to_inventory(inventory, items):
    """Function adds items from items list (without values) to inventory dict.
       Items names are prepared before adding"""
    items = [item.lower() for item in items] #changing all to smallcaps
    items = [item.strip("    .") for item in items] #removing unnecessary spaces
    items = [item.replace("  ", " ") for item in items] #removing double spaces
    for item in items: #loop for all items in list
        if item in inventory: #if the item is in inventory, its value will be increased by one
            inventory[item] += 1
        else: #if the item is not found in inventory, it will be added to dict with value 1
            inventory[item] = 1
    return inventory


def add_to_inventory_with_values(inventory, items_with_values,item_position=0,value_position=1,starting_point=0):
    """Function adds items from items 2-dimentional list (item + value) to inventory dict"""
    for item in items_with_values[starting_point:]: #loop for items in list, starting_point argument allows to omit title row
        if item[item_position] in inventory: #if the item is in inventory, its value will be increased by the added number
            inventory[item[item_position]] += item[value_position]
            if inventory[item[item_position]] < 0: #allows substracting values from inventory, but resulting number cannot be lower than 0
                inventory[item[item_position]] = 0
        else: #if the item is not found in inventory, it will be added to dict with added number
            inventory[item[item_position]] = item[value_position]
    return inventory


def print_table(inventory, order=None):
    """Function displays the inventory as a table.
       It is quite easy to customize table appereance and to add new columns"""
    #table constans: column names, left and right column edge marks and row separator mark
    #default table columns structure - left_edge::column1::right_edge::left_edge::column2
    #table structure can be changed by changing "rows_make" func
    TABLE_COUNT_COLUMN_NAME = "count"
    TABLE_ITEM_COLUMN_NAME = "item name"
    LEFT_EDGE = "  " #default 2 spaces, but it can be for example "| "
    RIGHT_EDGE = "  " #default 2 spaces, but it can be for example " |"
    ROW_SEPARATOR_MARK = "-" #row separator looks can be changed here

    #Define columns size (2 stages)
    #Stage 1 - making list of items and values lengths
    item_length_list = [len(item) for item in inventory]
    value_length_list = [len(str(inventory[item])) for item in inventory]

    #Stage 2 - comparision between max value length and first column title length
    #and between max item name length and second column title length
    #to find the longest phrase which determines column width
    if len(TABLE_COUNT_COLUMN_NAME) >= max(value_length_list):
        value_column_size = len(TABLE_COUNT_COLUMN_NAME)
    else:
        value_column_size = max(value_length_list)

    if len(TABLE_ITEM_COLUMN_NAME) >= max(item_length_list):
        item_column_size = len(TABLE_ITEM_COLUMN_NAME)
    else:
        item_column_size = max(item_length_list)

    #define first row (using rows_make function), table size (width), row separator and text under table (using total_items_count function)
    table_first_row = rows_make(LEFT_EDGE, RIGHT_EDGE, TABLE_COUNT_COLUMN_NAME, TABLE_ITEM_COLUMN_NAME, value_column_size, item_column_size)
    table_size = len(table_first_row) #table size (width) is equal to row length
    row_separator = ROW_SEPARATOR_MARK * table_size
    text_under_table = total_items_count(inventory) #text with default content, can be changed by adding the second argument

    #dicts aren't sortable, so it's required to change the dictionary to a sortable list if order argument differs to None
    if order != None:
        inventory_list = list([inventory[item], item] for item in inventory) #value as first column for easier sorting
        if order == "count,desc": #sorting values from the biggest to the smallest
            inventory_list = sorted(inventory_list, reverse=True)
        if order == "count,asc": #sorting values from the smallest to the biggest
            inventory_list = sorted(inventory_list)

    #printing table
    #In unsorted state, table body is made from 'inventory' dictionary (funcion table_body_from_dict)
    #In sorted state, table body is made from 'inventory_list' list (function table_body_from_list)
    print("Inventory:")
    print(table_first_row)
    print(row_separator)
    if order == None:
        table_body_from_dict(inventory, LEFT_EDGE, RIGHT_EDGE, value_column_size, item_column_size)
    else:
        table_body_from_list(inventory_list, LEFT_EDGE, RIGHT_EDGE, value_column_size, item_column_size)
    print(row_separator)
    print(text_under_table)


def rows_make(left, right, first_column, second_column, longest_value, longest_key):
    """This function allows standarding the looks of the first row and the rows
       in table body. Colums are adjusted to the right"""
    row = left + str(first_column).rjust(longest_value) + right + left + str(second_column.rjust(longest_key))
    return row


def table_body_from_dict(inv_dict, left, right, longest_value, longest_key):
    """Prints table rows with data from item dictionary.
       Rows are formatted according to the 'rows_make' function.
       Arguments: dictionary with items, left and right edge marks, lengths of the longest word
       in first and second column"""
    for item in inv_dict: #item - key in dict, inv_dict[item] - value in dict
        print(rows_make(left, right, inv_dict[item], item, longest_value, longest_key))


def table_body_from_list(inv_list, left, right, longest_value, longest_key):
    """prints table rows with data from list (which was created from the dict).
       Rows are formatted according to the 'rows_make' function.
       Arguments: list with items, left and right edge marks, lengths of the longest word
       in the first and the second column"""
    for i in range(len(inv_list)): #inv_list[i][0] - item value, inv_list[i][1] - item name
        print(rows_make(left, right, inv_list[i][0], inv_list[i][1], longest_value, longest_key))


def import_inventory(inventory, filename, ignore_error_lines=True, allows_negative_values=True):
    """A function for importing items from a csv file and adding them to inventory.
       In this version it is possible to import items with float non-integer values. It can be changed
       to mark this values as errors or round it by use int()
       If there are more than 2 columns (more than 1 coma in line) in csv file, it's still working.
       In case of csv file not existence or emptiness inventory is not changed.
       If ignore_error_lines argument is True and if csv file contains inline errors, wrong ones will be logged,
       correct will be added to inventory.
       If ignore_error_lines argument is False the inventory will not be changed and error lines will be logged
       If allows_negative_values is False, item with negative value will not be imported and will be added to errors log"""
    #define column names
    ITEM_HEADER = "item_name"
    COUNT_HEADER = "count"
    errors_log = [] #list for collecting error entries
    try: #checking for file existence
        open(filename, "r", encoding="utf-8")
        import_file = open(filename, "r", encoding="utf-8")
    except:
        errors_log["Import file doesn't exist"]
        return inventory, errors_log

    import_list = import_file.readlines() #import text from file into list
    import_file.close()

    #check whether the file is empty or there is no comma (not csv list). If any errors are found import is stopped and error is logged
    if import_list == [] or not "," in str(import_list):
        errors_log = ["Import file is empty or has incorrect content"]
        return inventory, errors_log

    #turning unformatted input list into usable list (removing /n and splitting lines)
    csv_to_list(import_list)

    #checking for correct title lines. If any errors are found import is stopped and error is logged
    if not ITEM_HEADER in import_list[0] or not COUNT_HEADER in import_list[0]:
        errors_log = ["Invalid titles in csv file"]
        return inventory, errors_log

    #defining column indexes - variables item_index and count_index store position of item and value column
    #when collumn order is different in csv file, this indexes will apply to correct collumn
    item_index = import_list[0].index(ITEM_HEADER)
    count_index = import_list[0].index(COUNT_HEADER)

    #searching for errors in count column
    errors_list = [] #a list storing indexes of error lines
    for i in range(1,len(import_list)): #from 1 to omit title line
        if len(import_list[i]) == 1:
            errors_list.append(i)
        elif import_list[i][count_index].isnumeric(): #if value is numeric, it will be turn to int
            import_list[i][count_index] = int(import_list[i][count_index])
            #if allows_negative_values argument is False, when the negative value will be found
            #the item will be not imported and error will be logged
            if allows_negative_values == False and import_list[i][count_index] < 0:
                errors_list.append(i)
        elif import_list[i][count_index].isalpha(): #if value is alpha string, it's an error for sure, the index of this line will be saved
            errors_list.append(i)
        elif isfloat(import_list[i][count_index]): #check if the string can be turn to float
            import_list[i][count_index] = float(import_list[i][count_index])
            if allows_negative_values == False and import_list[i][count_index] < 0:
                errors_list.append(i)
            if import_list[i][count_index].is_integer(): #if float is integer, it will be turned to int type
                import_list[i][count_index] = int(import_list[i][count_index])
        else: #everything else is an error
            errors_list.append(i)
    #if there are no errors, import list will be used to adding to inventory
    if errors_list == []:
        inventory = add_to_inventory_with_values(inventory,import_list,item_index,count_index,1)
        return inventory
    else: #if errors are found, there are 2 ways depending on 'ignore_error_lines' argument value
        if ignore_error_lines == False:
            for i in errors_list: #looking for lines from import_list with index located in the errors_list
                errors_log.append(import_list[i])
            return inventory, errors_log
        else:
            #creating list without errors for import to inventory
            import_list_without_errors = import_list[:] #assigning the primary list content
            for i in errors_list: #marking wrong lines
                import_list_without_errors[i] = ["error"]
            for i in range(len(errors_list)):
                for n in range(1,len(import_list_without_errors)): #from 1 to omit title line
                    if import_list_without_errors[n] == ["error"]:
                        del import_list_without_errors[n] #deletes marked wrong lines
                        break
            #final addition to inventory with add_to_inventory_with_values function
            #starting_point is equal to 1 to omit title line
            inventory = add_to_inventory_with_values(inventory,import_list_without_errors,item_index,count_index,1)
            #creating a list of lines, that couldn't be imported (error log), it can be used for an error check.
            #It returns tuple with inventory and error log
            for i in errors_list: #looking for lines from import_list with index located in the errors_list
                errors_log.append(import_list[i])
            return (inventory, errors_log)


def csv_to_list(csv_input_list):
    """Function turns unformatted input list made from csv file to an usable output list.
       Signs as "/n" and unnecessary spaces are removed. Lines are splitted into a list when a
       comma is found"""
    for i in range(len(csv_input_list)):
        csv_input_list[i] = csv_input_list[i].replace("\n","") #removing "\n" from each line
        csv_input_list[i] = csv_input_list[i].split(",") #dividing the line into list when comma is found
        for n in range(len(csv_input_list[i])): #removing unnecessary spaces in each element of list
            csv_input_list[i][n] = csv_input_list[i][n].strip()
            csv_input_list[i][n] = csv_input_list[i][n].replace("  ", " ")
            csv_input_list[i][n] = csv_input_list[i][n].lower() #changing all letters to smallcaps


def isfloat(value):
    """Function checks whether the string is a float. (An idea from stackoverflow.com)"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def export_inventory(inventory, filename):
    """Function opens or creates csv export file, writes prepared list with inventory
    to it and then closes the file"""
    export_file = open(filename, "w") #using "w" argument makes open function create an empty file if it does not exist
    csv_title_line = "item_name,count" #define title line
    inventory_list_export = csv_from_dict_export_preparing(inventory, csv_title_line) #changes inventory to an exportable list
    export_file.writelines(inventory_list_export)
    export_file.close()


def csv_from_dict_export_preparing(dictionary, title_line):
    """Function prepares pairs from dictionary into "key,value\n" format, that can be export as csv.
    Title line is also prepared and connects with rest of lines."""
    #preparing title_line
    title_line = str(title_line[:])
    title_line = title_line.strip(" ,.  ")
    #\n ending check
    if not "\n" in title_line:
        title_line = title_line + "\n"
    #replace ", " with "," without space
    if ", " in title_line:
        title_line = title_line.replace(", ", ",", title_line.count(", "))
    #this variable isn't necessary, but can be used as an error indicator, when it isn't equal to 2
    columns_in_title = title_line.count(",") + 1
    #preparing list with csv body with title line
    export_ready_list = [title_line] #it's first line, which will be extended with loop, that reads all pairs in inventory dict
    export_ready_list.extend(str(key) + "," + str(dictionary[key]) + "\n" for key in dictionary) #line format: "key,value\n"
    return export_ready_list


def main():
    IMPORT_FILE_NAME = "import_inventory.csv"
    EXPORT_FILE_NAME = "export_inventory.csv"
    inv = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
    display_inventory(inv)
    loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
    inv = add_to_inventory(inv, loot)
    display_inventory(inv)
    print_table(inv)
    print_table(inv,"count,desc")
    print_table(inv,"count,asc")
    display_inventory(inv)
    inv = import_inventory(inv, IMPORT_FILE_NAME)
    if type(inv) == tuple: #when there were errors during import function import_inventory returns tuple with inventory dict and error list
        errors_log = inv[1] #extraction errors list from tuple
        inv = inv[0] #extraction inventory dict from tuple
    print_table(inv)
    export_inventory(inv,EXPORT_FILE_NAME)


if __name__ == '__main__':
    main()
