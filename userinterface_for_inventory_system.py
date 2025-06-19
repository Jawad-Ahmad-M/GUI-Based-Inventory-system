import sys
import pandas as pd
import subprocess  # For running another Python file
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

# File paths
user_file = 'passwords.xlsx'

# Load user records (username, password, role)
def load_user_data():
    try:
        data = pd.read_excel(user_file)
        return data
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Password", "Role"])

# Check if user exists and match their password
def check_user_login(username, password, users_data):

    user = users_data[users_data["Username"] == username]
    if not user.empty:
        if user.iloc[0]["Password"] == password:
            return user.iloc[0]["Role"]
    return None

# Function to dynamically run another Python GUI file based on the user's role
def run_role_specific_gui(role):
    try:
        # Running the corresponding Python file based on the user's role
        if role == "Admin":
            subprocess.run(['python', 'admin_gui.py'])  # Replace 'admin_gui.py' with the correct filename
        elif role == "Staff":
            subprocess.run(['python', 'staff_gui.py'])  # Replace 'staff_gui.py' with the correct filename
        elif role == "Customer":
            subprocess.run(['python', 'customer_gui.py'])  # Replace 'customer_gui.py' with the correct filename
        else:
            print("Role not found")
    except Exception as e:
        print(f"Error: {str(e)}")

# Create the login window
def create_login_window():
    # Main window
    window = QWidget()
    window.setWindowTitle("Login Application")
    window.setGeometry(100, 100, 400, 300)

    screen_geometry = window.screen().geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()
    window_width = 600
    window_height = 400
    center_x = (screen_width - window_width) // 2
    center_y = (screen_height - window_height) // 2

    window.setGeometry(center_x, center_y, window_width, window_height)  # Center the window


    # Create layouts
    main_layout = QVBoxLayout()
    form_layout = QVBoxLayout()
    button_layout = QVBoxLayout()  # This will hold the login and open file buttons separately

    # Widgets
    login_label = QLabel("Login", window)
    login_label.setAlignment(Qt.AlignCenter)
    login_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")

    username_input = QLineEdit(window)
    username_input.setPlaceholderText("Enter Username")
    username_input.setStyleSheet("padding: 10px; font-size: 14px;")

    password_input = QLineEdit(window)
    password_input.setEchoMode(QLineEdit.Password)
    password_input.setPlaceholderText("Enter Password")
    password_input.setStyleSheet("padding: 10px; font-size: 14px;")

    login_button = QPushButton("Login", window)
    login_button.setStyleSheet("""
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
    """)

    open_file_button = QPushButton("Open File", window)
    open_file_button.setStyleSheet("""
        background-color: #C0C0C0;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
    """)
    open_file_button.setEnabled(False)  # Initially disabled until login is successful

    status_label = QLabel("", window)
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setStyleSheet("font-size: 14px; color: red;")

    # Add widgets to form layout
    form_layout.addWidget(login_label)
    form_layout.addWidget(username_input)
    form_layout.addWidget(password_input)
    form_layout.addWidget(login_button)

    # Add spacer to center the widgets
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    main_layout.addLayout(form_layout)
    main_layout.addItem(spacer)  # Add space between the form and the buttons

    # Add status label to the main layout
    main_layout.addWidget(status_label)

    # Add the open file button at the bottom
    button_layout.addWidget(open_file_button)
    main_layout.addLayout(button_layout)

    window.setLayout(main_layout)

    # Load users data
    users_data = load_user_data()

    # Handle login action
    def login():
        username = username_input.text()
        password = password_input.text()

        role = check_user_login(username, password, users_data)
        if role:
            status_label.setText(f"Logged in as: {role}")
            status_label.setStyleSheet("font-size: 14px; color: green;")  # Success message in green
            open_file_button.setEnabled(True)  # Enable the open file button after successful login
            open_file_button.setStyleSheet("""
                background-color: #2196F3;  /* Blue when file is open */
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            """)
        else:
        
            status_label.setText("Invalid username or password.")
            status_label.setStyleSheet("font-size: 14px; color: red;")  # Error message in red

    # Connect login button to login function
    login_button.clicked.connect(login)

    # Handle open file action (run role-specific GUI)
    def show_role_specific_gui():
        role = status_label.text().split(" ")[-1]  # Extract the role from the status label
        if role:
            run_role_specific_gui(role)  # Run the corresponding Python script based on the user's role

    open_file_button.clicked.connect(show_role_specific_gui)

    return window

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and display the login window
    login_window = create_login_window()
    login_window.show()

    # Start the application
    sys.exit(app.exec_())
