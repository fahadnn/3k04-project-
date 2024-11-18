import serial
import struct

class serialCommunication:
    def __init__(self, port = "COM3", baudrate = 57600, timeout = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        
    def open_conn(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            print(f"Serial connection opened!")
        except serial.SerialException as e:
            print(f"Serial connection failed: {e}")
            self.ser = None
            
    def close_conn(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed!")
            
    def create_packet(self, function_code, data):
        sync = 0x16
        packet = struct.pack('B', sync)
        packet += struct.pack('B', function_code)
        
        if data:
            packet += struct.pack(f'{len(data)}B', *data)
            
        return packet
    
    def send_packet(self, function_code, data=None):
        if not self.ser or not self.ser.is_open:
            self.open_conn()

        packet = self.create_packet(function_code, data if data else [])
        self.ser.write(packet)
        print(f"Sent packet: {packet}")

        self.close_conn()

    def receive_packet(self):
        if not self.ser or not self.ser.is_open:
            self.open_conn()

        packet = self.ser.read(40)
        if len(packet) < 3:
            print("Invalid packet received")
            self.close_connection()
            return None

        sync, function_code = struct.unpack('BB', packet[:1])
        data = packet[2:]

        print(f"Received packet:\nFunction Code: {function_code}, Data: {data}")
        self.close_conn()
        return function_code, data

# Example usage
if __name__ == "__main__":
    comm = serialCommunication(port='COM3', baudrate=57600)
    comm.send_packet(0x55, [1, 2, 3, 4])  # Example function code and data
    response = comm.receive_packet()
    if response:
        function_code, data = response
        print(f"RECEIVED\nfunction code: {function_code}, data: {data}")
        
        