#################################
# Hydroponic Garden App: User Manual
#################################

## 1. Introduction

Welcome to your smart hydroponic garden! This application allows you to monitor, program, and manage your garden from a web browser. You can track your plants, manage lighting and pump schedules, and get reminders for maintenance.

---

## 2. Accessing the Application

To use the app, you must be connected to the same Wi-Fi network as the garden controller (the Raspberry Pi).

1.  Open a web browser (like Chrome or Firefox) on your phone or computer.
2.  Navigate to the IP address of the controller. This is typically an address like http://192.168.1.XX or a hostname like http://garden-pi.local.

---

## 3. Main Features

The application is divided into several main sections, which you can typically find in the navigation menu.

* Status: This is your main dashboard. It shows you which plants are growing in which pods, when they were planted, and their expected harvest dates.
* Current Program: This section shows the *active* schedule for your garden. It tells you when the lights turn on/off and how often the water pump runs.
* Control: This section allows you to *change* the active program. You can switch from a "Seedling" program to a "Full-Grow" program, for example.
* Maintenance: This tracks important garden chores. It shows you the last time you cleaned the tank or checked the pH and reminds you when to do it next.
* Telemetry: This page displays sensor data from the garden, such as water temperature, air temperature, or humidity (if sensors are connected).
* Logs: This shows a technical log of what the system has been doing, such as "Pump Activated" or "Lights On".

---

## 4. Common Tasks

### How to Add a New Plant

1.  Go to the Status page.
2.  Find the tower and pod where you are planting your new seedling.
3.  Click the "Add Plant" or "Edit" button for that pod.
4.  A form will appear:
    * Plant Name: Select the type of plant from the list (e.g., "Basil" or "Lettuce").
    * Planted Date: Set the date you are planting it.
5.  Click "Save". The system will now track this plant and automatically calculate its estimated harvest date.

### How to Change the Grow Program

1.  Navigate to the Control page.
2.  You will see a list of available programs (e.g., "Seedling," "Fruiting," "Herbs").
3.  Select the program you want to activate.
4.  Click "Activate" or "Save".
5.  The system will immediately adopt the new schedule for lights and the pump.

### How to Log Maintenance

1.  Go to the Maintenance page.
2.  You will see a list of tasks (e.g., "Clean Tank," "Check pH").
3.  When you complete a task, find it in the list and click the "Reset" or "Done" button.
4.  This will update the "Last Performed" date and reset the timer for the next reminder.

---

## 5. Basic Troubleshooting

* Cannot connect to the app:
    * Ensure your phone or computer is connected to the correct Wi-Fi network.
    * Ensure the garden controller (Raspberry Pi) is plugged in and has power.
* Lights/Pump aren't running:
    * Go to the Current Program page and check the schedule.
    * Go to the Logs page to see if the system is reporting any errors.


#######################################
# Hydroponic Garden App: Developer Manual
#######################################

## 1. Introduction & Tech Stack

This project is a Flask-based web application for controlling and monitoring a hydroponic garden. It runs on a Raspberry Pi and communicates with hardware (like pumps and lights) via a serial connection.

### Key Technologies

* Backend: Python 3
* Framework: Flask
* Real-time UI: Flask-SocketIO
* Scheduling: APScheduler (for running background tasks)
* Database (Current): A series of JSON files in the `assets/` directory.
* Database (Intended): Flask-SQLAlchemy (dependencies are present, but core logic relies on JSON).
* Deployment: Gunicorn, `deploy.sh` script.

---

## 2. Project Structure

The application uses a Flask Blueprint and Application Factory pattern.

server/
│
├── .venv/               # Virtual environment
├── assets/              # Data storage
│   ├── plants.json      # Database of plant types
│   ├── programs.json    # List of all available grow programs
│   ├── currentProgram.json # The *active* program
│   └── status.json      # The *current state* of all pods
│
├── blueprints/          # Main application package
│   ├── __init__.py      # Application factory (create_app)
│   ├── api.py           # Core backend functions (data modification)
│   ├── threads.py     # Background tasks (lights, pump, serial)
│   │
│   ├── control/         # Control blueprint
│   ├── currentProgram/  # Current Program blueprint
│   ├── logtail/         # Logtail blueprint
│   ├── maintenance/     # Maintenance blueprint
│   ├── status/          # Status blueprint
│   └── telemetry/       # Telemetry blueprint
│
├── config.py            # Configuration classes (Dev, Prod)
├── requirements.txt     # Python dependencies
├── deploy.sh            # Deployment script
└── wsgi.py              # Entry point for Gunicorn

---

## 3. Installation & Deployment

The application is designed to be run from the `server/` directory.

### Installation

1.  Ensure Python 3 and `venv` are installed.
2.  Run `./deploy.sh` from the `server/` directory.
3.  This script will:
    * Create a Python virtual environment (`.venv`) if one doesn't exist.
    * Activate the virtual environment.
    * Install all dependencies from `requirements.txt`.
    * Start the application using `python3 wsgi.py`.

### Production Deployment

The `deploy.sh` script is set up for development (using `python3 wsgi.py`). For production, you should run the app with `gunicorn` (which is already in `requirements.txt`).

# From the server/ directory, after activating .venv
gunicorn --workers 4 --bind 0.0.0.0:5000 'wsgi:app'

---

## 4. Configuration (`config.py`)

All configuration is handled in `config.py`.

* `Config` (Base):
    * `SECRET_KEY`: [MAINTENANCE] This is currently generated randomly on every app start. This will break user sessions. It should be set to a static value, preferably from an environment variable.
    * `SQLALCHEMY_DATABASE_URI`: Configured for a `db.sqlite` file.
    * `APPLOGFILE`: Sets the path for logging.
* `Hardware`:
    * `SERIALPORT`: The TTY port for the microcontroller (e.g., `/dev/ttyACM0`).
    * `SERIALBAUD`: Baud rate for the serial connection.
* `JSON_Path`:
    * Defines the file paths for all data storage. This is the central "database" of the app.
* `ProdConfig` / `DevConfig`:
    * Set environment-specifics like `DEBUG = True`.

---

## 5. Core Components

### `blueprints/api.py`

This file is the "brain" of the application. It contains all the functions that **modify the state** of the garden. It is called by the frontend (via SocketIO) and by other internal functions.

* `get...()` functions: (`getCurrentProgr`, `getPrograms`, etc.) These functions read directly from the JSON files in `assets/`.
* `newPlant(r)`: Updates `status.json` with a new plant in a specific pod.
* `resetMaintInterval(task)`: Updates `status.json` with a new maintenance date.
* `changePrg(prg)`: This is a critical function. It:
    1.  Updates `currentProgram.json` with the new program data.
    2.  **Stops** the existing `checkLights` and `activatePump` jobs in `APScheduler`.
    3.  **Starts** new scheduler jobs with the new intervals from the selected program.
* `newPlantedDate(cmd)`: Updates the `plantedDate` for a specific pod in `status.json`.

[MAINTENANCE] This file is the biggest bottleneck for data corruption. All functions that `json.dump` to `status.json` create a **race condition**. If `newPlant` and `resetMaintInterval` are called at the same time, one of them will overwrite the other's changes. This should be the top priority for refactoring to use the SQLAlchemy database.

### `blueprints/threads.py` (Inferred from `api.py`)

This file likely contains the functions that are run by `APScheduler`.

* `checkLights(program)`: Called every few seconds. Compares the current time to the `program`'s light schedule and sends a serial command if the state needs to change.
* `activatePump(program)`: Called on an interval (e.g., every 30 minutes). Sends a serial command to run the pump for `program["pumpDuration"]`.
* `readSerial()`: (Inferred) Likely runs on a loop to read sensor data back from the microcontroller.
* `guessHarvest(app)`: Called after a new plant is added. It recalculates estimated harvest dates.

---

## 6. How to Add a New Feature (e.g., "Nutrients")

1.  Create the Blueprint:
    * Create a new folder: `server/blueprints/nutrients/`
    * Add a `nutrients.py` file to define the routes (e.g., `@nutrients_bp.route('/nutrients')`).
    * Add a `templates/` folder inside `nutrients/` with your Jinja2 template.
2.  Register the Blueprint:
    * In `server/blueprints/__init__.py`, import and register your new blueprint with the `app` object (similar to how `create_app` is set up in `wsgi.py`).
3.  Add to Navigation:
    * Edit the base template (e.g., `server/blueprints/templates/nav-standard.j2.html`) to add a link to `/nutrients`.
4.  Add API Logic (if needed):
    * If you need to save data, add a new JSON file to `assets/`.
    * Add "getter" and "setter" functions to `server/blueprints/api.py`.
    * Call these functions from your `nutrients.py` route file.