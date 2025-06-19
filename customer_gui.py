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


    # Check Availability Button
    check_availability_button = QPushButton("Check Availability")
    check_availability_button.clicked.connect(lambda: check_availability(table))
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
