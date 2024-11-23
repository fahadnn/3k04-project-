import serial
import struct
import time
#import serial.tools.list_ports  #Used to check available com ports


class serialCommunication:
    def __init__(self, port = "COM3", baudrate = 57600, timeout = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.data = [None] * 37 # List with 37 locations
           
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
            print(f"Serial Port Opened Successfully On {self.port} ! ") #prints which cport is connected
        except serial.SerialException as e:
            print(f"Error Opening Serial Port On {self.port} : {e}")
            self.ser = None
            
    def is_connected(self):    # Ensure the serial object exists & the connection is open
        if self.ser is not None and self.ser.is_open:
            return True
        return False
            
    def close_conn(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed!")
            
    def checksum(self, data):
        checksum = 0x34
        return checksum
            
    def create_packet(self, function_code, data, pacing_mode):   # Create a packet of 37 bytes from integer inputs
        sync = 0x16     # 22 in decimal
        packet = struct.pack('B', sync) #pack sync as 1 byte
        packet += struct.pack('B', function_code)   #pack fxn_code as 1 byte
        packet += struct.pack('B', pacing_mode)   #pack pacing_mode as 1 byte
        # packed 3 1 byte values so far sync and fxn code
        # Add the 1-byte, 2-byte, and 4-byte values for the parameters:
        if data:
            # `data` is structured as:
            # 5 1-byte codes, 6 2-byte codes, 4 4-byte codes, and 1 1-byte code
            # Example data layout: [1_byte_values, 2_byte_values, 4_byte_values, 1_byte_end]
            one_byte_values = data[3:8]   # First 5 values are 1-byte. Slice indexes 3 to 7 (inclusive to exclusive)
            two_byte_values = data[8:14]  # Next 6 values are 2-byte. Slice indexes 8 to 19
            four_byte_values = data[14:18]  # Next 4 values are 4-byte. Slice indexes 20 to 35
            
            # Pack 6 1-byte values (5B)
            packet += struct.pack('5B', *one_byte_values)   # '*' unpacks list & each element passed seperately to struct.pack
            # Pack 6 2-byte values (6H)
            packet += struct.pack('6H', *two_byte_values)
            # Pack 4 4-byte values (4I)
            print(four_byte_values)  # Log the values before packing
            packet += struct.pack('4I', *four_byte_values)
            # Pack the final 1-byte checksum value
            checksum = self.checksum(packet)
            packet += struct.pack('B', checksum)
            return packet
    
    def send_packet(self, function_code, data, pacing_mode):     # Used to Send the 37 byte packet(s) from DCM to Simulink
        if not self.ser or not self.ser.is_open:
            self.open_conn()
        if self.ser is None or not self.ser.is_open:
            print("Serial port is not open. Cannot complete send_packet method.")
            return
        packet = self.create_packet(function_code, data, pacing_mode)
        self.ser.write(struct.pack('37B', *packet)) # Writes 37Byte packet to com3. packet is list of bytes but struct.pack
        self.ser.write(packet)                      # expects individual bytes so use * operator which passes list 1 at a time
        print(f"Sent packet: {packet}")
        #self.close_conn()

    def receive_packet(self):       # Used to receive the 37 byte packet(s) from Simulink
        if not self.ser or not self.ser.is_open:
            self.open_conn()
            
        if self.ser is None or not self.ser.is_open:
            print("Failed to open serial connection. Cannot receive packet.")
            return None

        packet = self.ser.read(37) #37 bytes in a single packet transmission
        if len(packet) < 37:
            print("Invalid packet received")
            return None
        
        self.sync, function_code = struct.unpack('BB', packet[:2])  # Unpack sync(0x16) & FxnCode(bytes1&2, Packet[0&1])
        data = struct.unpack('34B', packet[2:-1])                   # Data goes from index 2 -> index 36
        data = struct.unpack('B', packet[36:37])                    # Unpack checksum byte index 36 (last position)
        checksum = packet[-1:]
        data = struct.unpack('B', checksum)                 # expects bytes-like object like bytes, slice, bytes array
        
        #validate checksum
        calculated_checksum = self.checksum(packet[:-1])    # Checksum excluding the checksum byte
        if checksum != calculated_checksum:
            print("Invalid checksum")
          #  self.close_conn()
            return None

        print(f"Received packet:\nFunction Code: {function_code}\nData: {data}")
        #self.close_conn()
        return function_code, data
    
    def receive_data_continuously(self):
        if not self.ser or not self.ser.is_open:
            self.open_conn()
        if not self.ser or not self.ser.is_open:
            print("Failed to open serial connection. Cannot receive data.")
            return
        print("Starting to receive data...")
        try:
            while True:
                # Attempt to receive a packet
                packet = self.receive_packet()
                if packet:
                    self.function_code, data = packet
                    # Process received data here (you can add your own logic)
                    print(f"Received data: {data}")
                
                # Optional: Add a small delay to avoid overloading the CPU or serial buffer
                time.sleep(0.2)
        finally:
            self.close_conn() #for testing

#if __name__ == "__main__":
