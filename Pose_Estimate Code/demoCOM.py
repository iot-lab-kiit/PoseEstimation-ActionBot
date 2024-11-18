import serial
import time

# Replace with your COM port (e.g., "COM3" for Windows or "/dev/ttyUSB0" for Linux)
COM_PORT = "COM5"  
BAUD_RATE = 9600  # Baud rate must match the device's configuration


virtual_port1 = '/dev/pts/0'  # Example for Linux; use the appropriate name for your system
virtual_port2 = '/dev/pts/1'  # Example for Linux; use the appropriate name for your system



# Initialize serial connection
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud rate.")
except Exception as e:
    print(f"Error opening COM port: {e}")
    exit()


try:
    ser_virtual1 = serial.Serial(virtual_port1, BAUD_RATE, timeout=1)
    ser_virtual2 = serial.Serial(virtual_port2, BAUD_RATE, timeout=1)
    print(f"Connected to virtual ports: {virtual_port1} and {virtual_port2} at {BAUD_RATE} baud rate.")
except Exception as e:
    print(f"Error opening virtual ports: {e}")
    exit()    

# Send data serially
try:
    while True:
        # Example data to send
        data_to_send = "Hello, COM Port!"
        
        # Encode string to bytes and send it
        ser.write(data_to_send.encode())
        print(f"Sent: {data_to_send}")

        ser_virtual1.write(data_to_send.encode())
        ser_virtual2.write(data_to_send.encode())
        print(f"Sent to virtual ports: {data_to_send}")

        # Read data from virtualport2
        #if ser_virtual2.in_waiting > 0:
           # response = ser_virtual2.readline().decode('utf-8').rstrip()
           # print(f"Received: {response}")
        
        # Wait before sending again
        #time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Close the serial connection
    if ser.is_open:
        ser.close()
        print("Serial port closed.")

    if ser_virtual1.is_open:
        ser_virtual1.close()

    if ser_virtual2.is_open:
        ser_virtual2.close()
