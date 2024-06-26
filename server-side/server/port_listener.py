import socket
import time
import dbStore as send_to_db
import singleRowData as srd
import json
import motorState

# Variable to store the status of data processing
data_processing_status = "Error"
motor_state = 0

def extracting_values(data):
    global data_processing_status
    try:
        # Parse the JSON data
        data_dict = json.loads(data)

        # Extract the pH, turbidity, TDS, temperature, longitude, latitude, and motorState values
        ph = data_dict.get('pH')
        turbidity = data_dict.get('turbidity')
        tds = data_dict.get('tds')
        temp = data_dict.get('temperature')
        longitude = data_dict.get('longitude')
        latitude = data_dict.get('latitude')
        # Default value -1 if motorState is not present
        #motor_state = int(data_dict.get('motorState'))
        motor_state = motorState.fetch_motor_state()

        # Check if all values are present
        if ph is not None and turbidity is not None and tds is not None and temp is not None and longitude is not None and latitude is not None and motor_state != -1:
            # Print the extracted values
            print(f"pH: {ph}, temperature: {temp}, TDS: {tds}, turbidity: {turbidity}, longitude: {longitude}, latitude: {latitude}, motorState: {motor_state}")

            # Store the data in the database
            send_to_db.store_data(ph, tds, temp, turbidity,longitude, latitude, motor_state)
            print("All data sent to the database successfully\n")
            srd.__update_view__()
            data_processing_status = True  # Data processed successfully
        else:
            print("\nError: Insufficient or missing data elements.\n")
            data_processing_status = False  # Error occurred while processing data
    except Exception as e:
        print("\nError occurred while extracting and processing data:", e)
        data_processing_status = False  # Error occurred while processing data


def start_listening():
    global data_processing_status
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("64.227.188.253", 80))
    server_socket.listen(1)
    print(f"Server is listening on Port 80...\n")

    try:
        while True:
            print("\nWaiting for a connection...\n")
            client_socket, client_address = server_socket.accept()
            print(f"\nConnection from {client_address} has been established!\n")
            data = client_socket.recv(1024)
            if data:
                # Print received data for debugging
                print("Received data:", data)

                # Check if it's a GET or POST request
                if b"POST /" in data:
                    # Handle POST request
                    payload_start = data.find(b'\r\n\r\n')
                    if payload_start != -1:
                        payload = data[payload_start + 4:].decode('utf-8')
                        extracting_values(payload)
                    else:
                        data_processing_status = False  # Invalid POST request format
                elif b"GET /" in data:
                    # Handle GET request
                    if data_processing_status is None:
                        response_data = {'status': 'None' }
                    else:
                        motor_state = motorState.fetch_motor_state()
                        response_data = {'status': 'Success', "motorState": motor_state if data_processing_status else 'Error'}
                    # Convert the response data to JSON format
                    response_json = json.dumps(response_data)

                    # Construct the HTTP response
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_json)}\r\n\r\n{response_json}"

                    # Send the response to the client
                    client_socket.sendall(response.encode('utf-8'))
                client_socket.close()
                time.sleep(5)

    except KeyboardInterrupt:
        print("\nClosing server socket...")
        server_socket.close()


if __name__ == "__main__":
    start_listening()
