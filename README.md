# 🧮 GUI-Based Inventory Management System

A complete **Inventory Management System** built using Python's `tkinter` GUI framework. It supports multiple user roles—**Admin**, **Staff**, and **Customer**—each with distinct permissions and interfaces. Inventory and authentication data are managed using `.xlsx` files (Excel spreadsheets), enabling easy editing and access without requiring an external database.

---

## 🚀 Features

- 🔐 **Role-based login system**
  - Admin, Staff, and Customer interfaces
- 📦 **Inventory Management**
  - View stock items, quantities, and details
- 🧾 **Excel (.xlsx) Data Storage**
  - No external database required
- 🎨 **User-Friendly GUI**
  - Built entirely with `tkinter`
  - Includes a separate CSS-like styling sheet for theme consistency
- 🧑‍💼 **Admin Tools**
  - View and manage user roles and product information
- 👩‍🔧 **Staff Functions**
  - Update inventory, restock items
- 🧍 **Customer Interface**
  - Browse items available in inventory

---

## 📁 Project Structure

```bash
GUI-Based-Inventory-system/
│
├── admin_gui.py                  # Admin GUI interface
├── staff_gui.py                  # Staff GUI interface
├── customer_gui.py               # Customer GUI interface
├── userinterface_for_inventory_system.py  # Main entry point
├── inventory_data.xlsx           # Inventory data (Excel file)
├── passwords.xlsx                # Login credentials and user roles
├── inventory_css.css             # Styling rules for tkinter elements
```

---

## 🛠️ Requirements

- Python 3.x
- `tkinter` (included with most Python installations)
- `openpyxl` (for reading/writing `.xlsx` files)

### Install Dependencies

```bash
pip install openpyxl
```

---

## 🔧 How to Run

```bash
python userinterface_for_inventory_system.py
```

Make sure `inventory_data.xlsx` and `passwords.xlsx` are in the same directory when running the program.

---

## 📌 Notes

- Make sure Excel files (`inventory_data.xlsx`, `passwords.xlsx`) are **not open** in any external application (like MS Excel) while the system is running.
- Data is persistent using Excel sheets for simplicity and portability.

---

## 📜 License

This project is for educational use only. Please refer to the repository for further licensing information.

---

## 👤 Author

**Jawad Ahmad**  
GitHub: [@Jawad-Ahmad-M](https://github.com/Jawad-Ahmad-M)

---

## 🤝 Contributions

Pull requests and suggestions are welcome! Feel free to fork this repository and enhance the system.
