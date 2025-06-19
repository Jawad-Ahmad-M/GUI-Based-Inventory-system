import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QFont
import re
import pandas as pd

df = pd.read_excel('inventory_data.xlsx')

Name = df['Name'].tolist()
Description = df['Description'].tolist()
Price = df['Price'].tolist()
Quantity = df['Quantity'].tolist()
Condition = df['Condition'].tolist()
Location = df['Location'].tolist()


def load_stylesheet(filename):
    """ Load the CSS file into the PyQt5 application """
    file = QFile(filename)
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        return stream.readAll()
    return ""

def update_table(table):
    """ Updates the table with larger text in each cell """
    table.clearContents()  # Clear the existing contents
    table.setRowCount(len(Name))  # Update the row count dynamically
    
    # Create a font object with a larger size
    font = QFont()
    font.setPointSize(12)  # Set font size (increase the number to make text larger)

    # Populate the table with updated data and apply font to each cell
    for row in range(len(Name)):
        name_item = QTableWidgetItem(Name[row])
        name_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 0, name_item)

        description_item = QTableWidgetItem(Description[row])
        description_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 1, description_item)

        price_item = QTableWidgetItem(str(Price[row]))
        price_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 2, price_item)

        quantity_item = QTableWidgetItem(str(Quantity[row]))
        quantity_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 3, quantity_item)

        condition_item = QTableWidgetItem(str(Condition[row]))
        condition_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 4, condition_item)

        location_item = QTableWidgetItem(str(Location[row]))
        location_item.setFont(font)  # Set the font for this cell
        table.setItem(row, 5, location_item)

    # Adjust row heights dynamically to fit content
    table.resizeRowsToContents()

    # Automatically adjust column widths based on content
    table.resizeColumnsToContents()
    
def set_fixed_row_height(table, height):
    """ Set a fixed height for all rows in the table """
    for row in range(table.rowCount()):
        table.setRowHeight(row, height)



def is_valid_input(text):
    """ Check if the input is valid: only letters and underscores and spaces are allowed. """
    pattern = r'^[a-zA-Z_ ]+$'  # Regex pattern to allow only alphabets and underscores
    return bool(re.match(pattern, text))


def add_item(table):
    """ Opens dialog to add a new item to the inventory """
    
    # Step 1: Collect inputs with validation
    while True:
        name, ok1 = QInputDialog.getText(None, 'Add Item', 'Enter item name:')
        if not ok1 or not name:
            name = "---"  # Default value for name
            break
        elif not is_valid_input(name):
            QMessageBox.warning(None, 'Invalid Input', 'Item name can only contain letters, spaces, and underscores.')
            continue  # Prompt the user to enter a valid name
        else:
            break  # Valid name, proceed to the next field
    
    while True:
        description, ok2 = QInputDialog.getText(None, 'Add Description', 'Enter item description:')
        if not ok2 or not description:
            description = "---"  # Default value for description
            break
        elif not is_valid_input(description):
            QMessageBox.warning(None, 'Invalid Input', 'Description can only contain letters, spaces, and underscores.')
            continue  # Prompt the user to enter a valid description
        else:
            break  # Valid description, proceed to the next field
    
    price, ok3 = QInputDialog.getInt(None, 'Add Price', 'Enter item price:', 0, 0, 10000)
    if not ok3:
        price = 0  # Default value for price
    
    quantity, ok4 = QInputDialog.getInt(None, 'Add Quantity', 'Enter item quantity:', 0, 0, 10000)
    if not ok4:
        quantity = 0  # Default value for quantity
    
    condition, ok5 = QInputDialog.getInt(None, 'Add Condition', 'Enter item condition:', 0, 0, 10)
    if not ok5:
        condition = 10  # Default value for condition
    
    while True:
        location, ok6 = QInputDialog.getText(None, 'Add Location', 'Enter item location:')
        if not ok6 or not location:
            location = "---"  # Default value for location
            break
        elif not is_valid_input(location):
            QMessageBox.warning(None, 'Invalid Input', 'Location can only contain letters, spaces, and underscores.')
            continue  # Prompt the user to enter a valid location
        else:
            break  # Valid location, proceed
    
    # Step 2: Show summary of entered values
    summary = (f"Name: {name}\n"
               f"Description: {description}\n"
               f"Price: {price}\n"
               f"Quantity: {quantity}\n"
               f"Condition: {condition}\n"
               f"Location: {location}")
    
    reply = QMessageBox.question(None, 'Confirm Values', f"The following values were entered:\n\n{summary}\n\nProceed with adding this item?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
    if reply == QMessageBox.No:
        # Step 3: Allow modification of specific value
        options = ['Name', 'Description', 'Price', 'Quantity', 'Condition', 'Location']
        attribute, ok = QInputDialog.getItem(None, 'Select Attribute', 'Select the attribute to modify:', options, 0, False)
        if ok and attribute:
            row = table.currentRow()  # Find the row to modify (assuming the table is selected)
            
            if attribute == 'Name':
                while True:
                    new_value, ok = QInputDialog.getText(None, 'Modify Name', 'Enter new name:', text=name)
                    if ok and is_valid_input(new_value) or new_value == "---":
                        name = new_value
                        break
                    else:
                        QMessageBox.warning(None, 'Invalid Input', 'Name can only contain letters, spaces, and underscores.')
            
            elif attribute == 'Description':
                while True:
                    new_value, ok = QInputDialog.getText(None, 'Modify Description', 'Enter new description:', text=description)
                    if ok and is_valid_input(new_value) or new_value == "---":
                        description = new_value
                        break
                    else:
                        QMessageBox.warning(None, 'Invalid Input', 'Description can only contain letters, spaces, and underscores.')
            
            elif attribute == 'Price':
                new_value, ok = QInputDialog.getInt(None, 'Modify Price', 'Enter new price:', value=price, min=0, max=10000)
                if ok:
                    price = new_value
            
            elif attribute == 'Quantity':
                new_value, ok = QInputDialog.getInt(None, 'Modify Quantity', 'Enter new quantity:', value=quantity, min=0, max=10000)
                if ok:
                    quantity = new_value
            
            elif attribute == 'Condition':
                new_value, ok = QInputDialog.getInt(None, 'Modify Condition', 'Enter new condition:', value=condition, min=0, max=10)
                if ok:
                    condition = new_value
            
            elif attribute == 'Location':
                while True:
                    new_value, ok = QInputDialog.getText(None, 'Modify Location', 'Enter new location:', text=location)
                    if ok and is_valid_input(new_value) or new_value == "---":
                        location = new_value
                        break
                    else:
                        QMessageBox.warning(None, 'Invalid Input', 'Location can only contain letters, spaces, and underscores.')

            # Update the summary with new values
            summary = (f"Name: {name}\n"
                       f"Description: {description}\n"
                       f"Price: {price}\n"
                       f"Quantity: {quantity}\n"
                       f"Condition: {condition}\n"
                       f"Location: {location}")
            
            # Ask the user to confirm the new values
            reply = QMessageBox.question(None, 'Confirm Modified Values', f"The following modified values were entered:\n\n{summary}\n\nProceed with adding this item?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return  # If still not proceeding, exit the function
    
    # Step 4: Add the item to the inventory after confirmation
    Name.append(name)
    Description.append(description)
    Price.append(price)
    Quantity.append(quantity)
    Condition.append(condition)
    Location.append(location)
    
    # Update the table after adding the new item
    update_table(table)

def modify_specific_value(table):
    """ Modifies a specific value of a selected item """
    row = table.currentRow()
    if row == -1:
        QMessageBox.warning(None, 'Error', 'Please select an item to modify.')
        return
    
    # Ask the user which attribute they want to modify
    options = ['Name', 'Description', 'Price', 'Quantity', 'Condition', 'Location']
    attribute, ok = QInputDialog.getItem(None, 'Select Attribute', 'Select the attribute to modify:', options, 0, False)
    if not ok or not attribute:
        return

    # Depending on the attribute, prompt for the new value
    if attribute == 'Name':
        new_value, ok = QInputDialog.getText(None, 'Modify Name', 'Enter new name:', text=Name[row])
        if ok:
            Name[row] = new_value
    elif attribute == 'Description':
        new_value, ok = QInputDialog.getText(None, 'Modify Description', 'Enter new description:', text=Description[row])
        if ok:
            Description[row] = new_value
    elif attribute == 'Price':
        new_value, ok = QInputDialog.getInt(None, 'Modify Price', 'Enter new price:', value=Price[row], min=0, max=10000)
        if ok:
            Price[row] = new_value
    elif attribute == 'Quantity':
        new_value, ok = QInputDialog.getInt(None, 'Modify Quantity', 'Enter new quantity:', value=Quantity[row], min=0, max=10000)
        if ok:
            Quantity[row] = new_value
    elif attribute == 'Condition':
        new_value, ok = QInputDialog.getInt(None, 'Modify Condition', 'Enter new condition:', value=Condition[row], min=0, max=10)
        if ok:
            Condition[row] = new_value
    elif attribute == 'Location':
        new_value, ok = QInputDialog.getText(None, 'Modify Location', 'Enter new location:', text=Location[row])
        if ok:
            Location[row] = new_value
    
    # Update the table after modification
    update_table(table)

def modify_item(table):
    """ Opens dialog to modify an item """
    row = table.currentRow()
    if row == -1:
        QMessageBox.warning(None, 'Error', 'Please select an item to modify.')
        return

    current_name = Name[row]
    new_name, ok1 = QInputDialog.getText(None, 'Modify Item', 'Enter new item name:', text=current_name)
    if ok1 and new_name:
        new_description, ok2 = QInputDialog.getText(None, 'Modify Description', 'Enter new description:', text=Description[row])
        if ok2 and new_description:
            new_price, ok3 = QInputDialog.getInt(None, 'Modify Price', 'Enter new price:', value=Price[row], min=0, max=10000)
            if ok3:
                new_quantity, ok4 = QInputDialog.getInt(None, 'Modify Quantity', 'Enter new quantity:', value=Quantity[row], min=0, max=10000)
                if ok4:
                    new_condition, ok5 = QInputDialog.getInt(None, 'Modify Condition', 'Enter new condition:', value=Condition[row], min=0, max=10)
                    if ok5:
                        new_location, ok6 = QInputDialog.getText(None, 'Modify Location', 'Enter new location:', text=Location[row])
                        if ok6:
                            Name[row] = new_name
                            Description[row] = new_description
                            Price[row] = new_price
                            Quantity[row] = new_quantity
                            Condition[row] = new_condition
                            Location[row] = new_location
                            update_table(table)  # Update the table after modifying the item

def remove_item(table):
    """ Removes selected item from the inventory """
    row = table.currentRow()
    if row == -1:
        QMessageBox.warning(None, 'Error', 'Please select an item to remove.')
        return

    reply = QMessageBox.question(None, 'Confirm Removal', 'Are you sure you want to remove this item?', 
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        Name.pop(row)
        Description.pop(row)
        Price.pop(row)
        Quantity.pop(row)
        Condition.pop(row)
        Location.pop(row)
        update_table(table)  # Update the table after removing the item

def check_availability(table):
    """ Checks availability of item in the inventory and selects the row if found """
    item_name, ok = QInputDialog.getText(None, 'Check Availability', 'Enter item name:')
    if ok and item_name:
        # Convert the entered item_name to lowercase
        item_name_lower = item_name.lower()

        # Case-insensitive comparison by converting each stored item to lowercase
        found = False
        for i, name in enumerate(Name):
            if name.lower() == item_name_lower:
                # Show a message box with information
                QMessageBox.information(None, 'Item Availability', f'{item_name} is available in the inventory at location: {Location[i]}')

                # Select the row in the table
                table.selectRow(i)
                found = True
                break

        if not found:
            QMessageBox.warning(None, 'Item Not Found', f'{item_name} is not available in the inventory.')

def setup_table(table):
    """ Configure the table settings """
    table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing of table cells
    table.setSelectionBehavior(QTableWidget.SelectRows)  # Highlight entire rows on selection
    # table.setSizePolicy(1, 1)  # Make the table expand and contract with the window size

def is_click_outside_table(event, table):
    """ Detects if the click happened outside the table and resets the current cell """
    if not table.rect().contains(event.pos()):
        table.setCurrentCell(-1, -1)  # Reset the current selected cell
        return True
    return False



def main():
    app = QApplication(sys.argv)
    
    # Load the CSS file and apply it
    stylesheet = load_stylesheet('inventory_css.css')  # Load your specific CSS file
    app.setStyleSheet(stylesheet)  # Apply the stylesheet to the app

    # Set up the main window
    window = QWidget()
    window.setWindowTitle("Inventory Management System")
    window.setGeometry(100, 100, 800, 600)

    
    screen_geometry = window.screen().geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    window_width = 1200
    window_height = 800
    center_x = (screen_width - window_width) // 2
    center_y = (screen_height - window_height) // 2

    window.setGeometry(center_x, center_y, window_width, window_height)  # Center the window

    
    layout = QVBoxLayout()

    # Header Label
    header_label = QLabel("Inventory Management System")
    layout.addWidget(header_label)

    # Inventory Table
    table = QTableWidget(window)
    table.setRowCount(len(Name))
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["Name", "Description", "Price", "Quantity", "Condition", "Location"])
    setup_table(table)
    update_table(table)

    set_fixed_row_height(table, 50)
    
    # Disable any automatic row selection
    table.setCurrentCell(-1, -1)  # This ensures no row is selected at the start.
    
    layout.addWidget(table)

    # Buttons layout
    buttons_layout = QHBoxLayout()

    # Add Item Button
    add_item_button = QPushButton("Add Item")
    add_item_button.clicked.connect(lambda: add_item(table))
    buttons_layout.addWidget(add_item_button)

    # Modify Item Button
    modify_item_button = QPushButton("Modify Whole Item")
    modify_item_button.clicked.connect(lambda: modify_item(table))
    buttons_layout.addWidget(modify_item_button)

    # Modify Specific Entity Button
    modify_specific_button = QPushButton("Modify Specific Entity")
    modify_specific_button.clicked.connect(lambda: modify_specific_value(table))
    buttons_layout.addWidget(modify_specific_button)

    # Remove Item Button
    remove_item_button = QPushButton("Remove Item")
    remove_item_button.clicked.connect(lambda: remove_item(table))
    buttons_layout.addWidget(remove_item_button)

    # Check Availability Button
    check_availability_button = QPushButton("Check Availability")
    check_availability_button.clicked.connect(check_availability)
    buttons_layout.addWidget(check_availability_button)

    # Clear Selection Button
    clear_selection_button = QPushButton("Clear Selection")
    clear_selection_button.clicked.connect(lambda: table.clearSelection())
    buttons_layout.addWidget(clear_selection_button)

    # Add buttons to Layout
    layout.addLayout(buttons_layout)

    # Set the layout
    window.setLayout(layout)

    # Show window
    window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
