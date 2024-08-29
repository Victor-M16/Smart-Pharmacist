# Smart Pharmacist

This project repository holds architecture and website source code for the Smart Pharmacist final year engineering project being implemented at [Malawi University Of Business And Applied Sciences](https://www.mubas.ac.mw/) by Victor Mjimapemba, Khumbolawo Mussa and Grace Chiwaya.

The project consists of a hardware and software element. The hardware element is an electronics project that is a rudimentary prototype of a carousel vending machine meant to dispense prescription medication. Further documentation for these componenents can be found in the `firmware` and `circuit-diagrams` folders.

The software component is a built from the ground up hospital management system meant to work in tandem with the prototype.

## Technologies 

1. [Django](https://docs.djangoproject.com/en/5.1/)
2. [Django-Rest-FrameWork](https://www.django-rest-framework.org/)
3. [HTML/CSS](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)
4. [Tailwind CSS](https://tailwindcss.com/)
5. [ArduinoIDE](https://www.arduino.cc/en/Guide)
6. [Twilio](https://www.twilio.com/en-us)

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
