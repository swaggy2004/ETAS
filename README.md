# ETAS: Enviro Track Aqua Shield

ETAS (Enviro Track Aqua Shield) is an IoT-based water filtration monitoring system that leverages various sensors and modules to collect and analyze crucial water quality parameters. The project aims to provide a comprehensive solution for continuous monitoring and management of water bodies, enabling proactive measures to maintain optimal water quality.

# Team behind the project
- **S Balasooriya**
- **J.D Victoria**
- **M.M.I.U Bandara**
- **W.I Avarjana**
- **M.F.M Ruhaib**
- **J.S Thirimanna**

## Methodology

The project follows a systematic methodology to ensure effective implementation and reliable results. The key aspects of the methodology are as follows:

### Hardware Integration

ETAS incorporates an array of sensors and modules to gather comprehensive data on water quality parameters. These include:

- Liquid pH Sensor
- Temperature Sensor (DS18B20)
- Analog Total Dissolved Solids (TDS) Sensor
- Analog Turbidity Sensor
- SIM900 Module (GPRS Communication)
- NEO 6M GPS Module (Geolocation)

These components are seamlessly integrated with an Arduino Mega microcontroller board, which acts as the central processing unit for data collection and communication.

### Data Transmission

The SIM900 module plays a crucial role in facilitating data transmission from the Arduino device to a remote server. Leveraging the GPRS protocol, the system sends HTTP POST and GET requests containing sensor data in JSON format to the server.

### Server Infrastructure

The project utilizes a Linux Droplet from DigitalOcean as the server infrastructure. The server hosts the following components:

1. **MariaDB Database**: A relational database system for storing and managing sensor data.
2. **Port Listener**: A component that handles incoming data requests, extracts JSON payloads, and stores the data in the MariaDB database.
3. **Graphical User Interface (GUI)**: A web-based dashboard built using Flask and Plotly libraries for data visualization and analysis.

### Data Analysis and Visualization

The GUI provides users with an interactive dashboard featuring real-time updates, periodical data aggregation, and spatial visualization through heat maps. Users can analyze water quality trends, patterns, and purity indices based on the collected sensor data.

## Repository Contents

This repository contains the following files and directories:

-  `arduino/`: This directory houses the Arduino code responsible for sensor integration, data collection, and communication with the server.
-  `server-side/`: This directory includes the server-side code, such as the port listener and the Plotly dashboard implementation.

By combining hardware integration, data transmission, server infrastructure, and data analysis and visualization, ETAS offers a comprehensive solution for monitoring and managing water quality in real-time, enabling proactive measures to protect and preserve water resources.
