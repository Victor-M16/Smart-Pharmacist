import requests
import json
import logging

# Configure logging
logging.basicConfig(filename='vending_machine.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# IP addresses
django_backend_url = "http://192.168.8.168:8000"
esp32_url = "http://192.168.8.124:80"

def get_prescription(vending_code):
    try:
        url = f"{django_backend_url}/api/prescriptions/"
        response = requests.get(url)
        # print(response.json())
        response.raise_for_status()
        prescriptions = response.json()

        # Find the prescription that matches the vending_code
        for prescription in prescriptions:
            if prescription['code'] == vending_code:
                return prescription
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching prescription: {e}")
        return None

def get_prescription_medications(prescription_id):
    try:
        url = f"{django_backend_url}/api/prescription-medications/?prescription={prescription_id}"
        response = requests.get(url)
        print(response.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching prescription medications: {e}")
        return []

def get_vending_slots(medication_ids):
    try:
        url = f"{django_backend_url}/api/vending-slots/"
        response = requests.get(url)
        response.raise_for_status()
        vending_slots = response.json()
       

        slots = []
        for slot in vending_slots:
            if slot['medication']['id'] in medication_ids:
                slots.append(slot)
                print(slots)
        return slots
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching vending slots: {e}")
        return []

def send_positions_to_esp32(positions):
    try:
        url = f"{esp32_url}/rotate"
        data = {"positions": positions}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending positions to ESP32: {e}")
        return None, str(e)

def main():
    while True:
        try:
            vending_code = input("Enter vending code: ")

            # Validate vending code
            if len(vending_code) != 4 or not vending_code.isalnum():
                print("Invalid vending code. Please enter a 4-character alphanumeric code.")
                continue

            # Get the prescription matching the vending_code
            prescription = get_prescription(vending_code)
            if not prescription:
                print("No matching prescription found.")
                continue

            # Get the prescription medications
            prescription_medications = get_prescription_medications(prescription['id'])
            medication_ids = [med['medication'] for med in prescription_medications]
            print(medication_ids)

            # Get the vending slots corresponding to the medications
            vending_slots = get_vending_slots(medication_ids)
            slot_numbers = [slot['slot_number'] for slot in vending_slots]

            # Prepare JSON array for ESP32
            json_data = {"positions": slot_numbers}
            print(f"Sending positions to ESP32: {json_data}")

            # Send positions to ESP32
            status_code, response_text = send_positions_to_esp32(slot_numbers)
            if status_code == 200:
                print("Rotation command sent successfully!")
            else:
                print(f"Failed to send command to ESP32: {response_text}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print("An unexpected error occurred. Please check the log file for details.")

if __name__ == "__main__":
    main()
