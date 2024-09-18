import socket
import threading
import struct
import datetime
from database import save_data

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 50262

def decode_avl_data(hex_data, imei):
    print("Decoding AVL data packet...")
    
    # Decodificar el timestamp
    index_timestamp = 10  # Después de Preamble, Data Field Length, Codec ID, Number of Data 1
    timestamp_bytes = hex_data[index_timestamp:index_timestamp+8]
    timestamp = struct.unpack('>Q', timestamp_bytes)[0] / 1000.0
    timestamp_datetime = datetime.datetime.utcfromtimestamp(timestamp)
    print(f"Timestamp: {timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')} UTC")

    # Indices para GPS Data
    index_gps_data = index_timestamp + 8 + 1  # Añadir 1 por el byte de Priority
    
    # Decodificar GPS Data
    longitude_bytes = hex_data[index_gps_data:index_gps_data+4]
    latitude_bytes = hex_data[index_gps_data+4:index_gps_data+8]
    altitude_bytes = hex_data[index_gps_data+8:index_gps_data+10]
    angle_bytes = hex_data[index_gps_data+10:index_gps_data+12]
    satellites = hex_data[index_gps_data+12]
    speed_bytes = hex_data[index_gps_data+13:index_gps_data+15]
    
    longitude = struct.unpack('>i', longitude_bytes)[0] / 10000000
    latitude = struct.unpack('>i', latitude_bytes)[0] / 10000000
    altitude = struct.unpack('>h', altitude_bytes)[0]
    angle = struct.unpack('>h', angle_bytes)[0]
    speed = struct.unpack('>h', speed_bytes)[0]
    save_data(imei, timestamp_datetime, latitude, longitude, altitude, angle, satellites, speed)
    print(f"Longitude: {longitude}, Latitude: {latitude} ({latitude},{longitude})")
    print(f"Altitude: {altitude} meters, Angle: {angle} degrees")
    print(f"Satellites: {satellites} visible, Speed: {speed} km/h")

def send_command(client_socket, start_sending):
    command = b'\x01' if start_sending else b'\x00'
    client_socket.sendall(command)
    print(f"Sent {'start' if start_sending else 'stop'} command to device.")

def handle_client(client_socket):
    try:
        imei_data = client_socket.recv(1024)
        if not imei_data:
            raise ValueError("No IMEI received")
        imei_data_decoded = imei_data.decode()
        print(f"Received IMEI: {imei_data_decoded}")

        # Envío del comando 'start' después de recibir el IMEI
        send_command(client_socket, start_sending=True)

        while True:
            data = client_socket.recv(1024)
            if not data:
                print("No more data received. Ending session.")
                break

            print("Received data:", data.hex())
            decode_avl_data(data, imei_data_decoded)

        # Opcional: enviar comando 'stop' al finalizar la sesión
        send_command(client_socket, start_sending=False)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()

