# Smart Pharmacist

This project repository holds architecture and website source code for the Smart Pharmacist final year engineering project being implemented at [Malawi University Of Business And Applied Sciences](https://www.mubas.ac.mw/) by Victor Mjimapemba, Khumbolawo Mussa and Grace Chiwaya.

The project consists of a hardware and software element. The hardware element is an electronics project that is a rudimentary prototype of a carousel vending machine meant to dispense prescription medication. Further documentation for these componenents can be found in the `firmware` and `concepts` folders.

The software component is a built from the ground up hospital management system meant to work in tandem with the prototype. The main system is a django project named `smartpharmacist`

## Use Case Workflow
1. The patient completes a consultation with the doctor, who enters the prescription details into the web system, such as the patient's name, sickness and prescribed medication and instructions to take the medications.
2. The system automatically generates a unique 4-digit "prescription.code" which it assigns to the prescription the doctor just submitted.
3. The system sends an SMS message to the patient, containing the prescription.code, the names of the prescribed medications and the associated instructions. If the patient has no phone or their phone is off, the code is also displayed on the doctor's screen so the patient can copy it down on a paper or their physical health passport. 
4. The patient goes to the vennding machine prototype,which has already been boooted, has authenticated itself with the backend server using `jwt` and gone into `ready-state`. The patient then inputs the received "prescription.code" on the numeric keypad, using visual feedback from the 16x2 LCD module.
5. The machine goes into `code-validation-state` where it sends the received code to the backend server for processing as a POST request for security.
6. The backend server checks the code against its prescriptions database and if the code exists and corresponds to a prescription that has not been dispensed yet, then it queries the database for the medications assigned to this prescription and the vending slots where these pre-packaged medications were stored. The server responds to to the vending machine after this processing with either an error message if the code was invalid or a list of vending slots in optimised order for the vending machine to rotate to if the code was valid.
7. If the vending machine received a list of vending slots, then it goes into `dispensing-state` where it rotates in order of the received slots, allowing the patient to collect all their assigned medications.
8. The vending machine updates the prescription in the database so that itself and other vending machines know that that prescription code is no longer valid and has been dispensed.
9. The vending machine goes back into `ready-state` to be ready to service the next patient and code.

## Technologies 

1. [Django](https://docs.djangoproject.com/en/5.1/)
2. [Django-Rest-FrameWork](https://www.django-rest-framework.org/)
3. [HTML/CSS](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)
4. [Tailwind CSS](https://tailwindcss.com/)
5. [ArduinoIDE](https://www.arduino.cc/en/Guide)
6. [Twilio](https://www.twilio.com/en-us)

## Hardware 

1. LCD
2. ESP32
3. 4X4 Matrix Keypad
4. NEMA 17 Motors
5. L298N Motor Drivers

## Setting Up The Project

1. Fork and clone this repository

2. Setup your Django development environment. More instructions [here](https://www.djangoproject.com/start/)

3. Make sure to also have node.js installed. Instructions [here](https://nodejs.org/)

4. Create a python virtual environment in the `smartpharmacist` directory

5. Install Django dependencies for the project using the `requirements.txt`

```shell
pip install requirements.txt
```
6. Install django-tailwind dependencies by navigating to `theme\static_src\` in your terminal and typing 

```shell
npm install
```
7. Create a `local_settings.py` file in the `smartpharmacist` directory and include the following Python code

```python
from .base_settings import *
```
Here you can specify any extra configuration specification to your environment, such as database connection.

8. Start the Tailwind Development server by running the following command in your terminal

```shell
python manage.py tailwind start
```

9. Start the Django development server by running the following command in your terminal:

```shell
python manage.py runserver
```

## Contributing To The Project

Feel free to contact the developers with any contributions you would like to make

- [Victor Mjimapemba](https://github.com/Victor-M16/)

- [Khumbolawo Mussa](https://github.com/Khumbolawo/)
