# Smart Pharmacist Vending Machine

## Project Overview

The Smart Pharmacist Vending Machine is an automated system designed to dispense medications based on prescriptions. It leverages Django for the backend, a Raspberry Pi for hardware control, and MySQL for database management. This system aims to automate the dispensing process, ensuring patients receive their prescribed medications efficiently and accurately.

## Key Features

- **Automated Medication Dispensing**: Uses a Raspberry Pi to control the dispensing mechanism of the vending machine.
- **Prescription Management**: Stores and manages patient prescriptions, including multiple medications per prescription.
- **Inventory Management**: Tracks medication inventory in each vending machine and each slot within the machine.
- **User Authentication**: Allows patients to retrieve medications using unique prescription codes.


## Setting Up the Project

### Prerequisites

- Python 3.x
- Django
- MySQL

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/smart-pharmacist-vending-machine.git
   cd smart-pharmacist-vending-machine

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Configure the Database**:
   Update the database settings in settings.py to match your MySQL configuration.

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser

6. **Start the server**:
   ```bash
   python manage.py runserver




