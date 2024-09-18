
# Teltonika GPS Server

This project is a basic implementation of a GPS server that receives AVL data from Teltonika devices, decodes the data, and stores it into a MySQL database. It includes two main components:

1. **database.py** - Handles saving the decoded data into a MySQL database.
2. **gps_server.py** - Listens for incoming connections from Teltonika devices, receives AVL data, decodes it, and saves it using `database.py`.

## Requirements

- Python 3.x
- PyMySQL
- MySQL Server

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/teltonika-gps-server.git
    cd teltonika-gps-server
    ```

2. Install the required Python packages:
    ```bash
    pip install pymysql
    ```

3. Set up the MySQL database:
    - Create a database and a table to store the GPS data:
    ```sql
    CREATE DATABASE gps_data_db;
    
    USE gps_data_db;
    
    CREATE TABLE gps_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        imei VARCHAR(15) NOT NULL,
        timestamp DATETIME NOT NULL,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        altitude INT NOT NULL,
        angle INT NOT NULL,
        satellites INT NOT NULL,
        speed INT NOT NULL,
        google_maps_url VARCHAR(255) NOT NULL
    );
    ```

4. Update the database connection details in `database.py`:
    ```python
    connection = pymysql.connect(host='127.0.0.1', user='username', password='password', db='database', cursorclass=pymysql.cursors.DictCursor)
    ```
    Replace `'username'`, `'password'`, and `'database'` with your MySQL credentials.

## Usage

1. Start the GPS server:
    ```bash
    python gps_server.py
    ```
    The server will start listening on `0.0.0.0:50262`.

2. The server will accept incoming connections from Teltonika devices, decode the AVL data, and store it into the MySQL database.

## How It Works

- When a Teltonika device connects to the server, it sends an IMEI which is used to identify the device.
- The server sends a "start" command to the device after receiving the IMEI.
- The device then starts sending AVL data packets.
- The server decodes the AVL data to extract GPS information such as timestamp, latitude, longitude, altitude, angle, satellites, and speed.
- The extracted data is saved into the MySQL database using the `database.py` script.

## Troubleshooting

- Ensure that your MySQL server is running and the credentials in `database.py` are correct.
- Make sure that the port `50262` is open and not blocked by any firewall.
- Verify that the Teltonika device is correctly configured to send data to the server's IP address and port.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Teltonika for their AVL data protocol.
