import serial
import time

# Replace with your COM port (e.g., "COM3" for Windows or "/dev/ttyUSB0" for Linux)
COM_PORT = "COM5"  
BAUD_RATE = 9600  # Baud rate must match the device's configuration

# Initialize serial connection
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud rate.")
except Exception as e:
    print(f"Error opening COM port: {e}")
    exit()

# Send data serially
try:
    while True:
        # Example data to send
        data_to_send = "Hello, COM Port!"
        
        # Encode string to bytes and send it
        ser.write(data_to_send.encode())
        print(f"Sent: {data_to_send}")
        
        # Wait before sending again
        #time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Close the serial connection
    if ser.is_open:
        ser.close()
        print("Serial port closed.")
