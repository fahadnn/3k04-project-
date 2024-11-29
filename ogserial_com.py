import serial
import struct
import time
import serial.tools.list_ports  #Used to check available com ports
import os   #operating system

class serialCommunication:
    def __init__(self, port = "COM3", baudrate = 57600, timeout = 1):
        self.list_available_ports()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.data = [None]*37
    
    def list_available_ports(self):
        """Prints all available serial ports for the user to choose from."""
        if os.name == 'posix':  # Check if the system is Linux (Ubuntu or similar)
            # List all files in /dev and filter for serial port names (ttyUSB or ttyACM)
            ports = [port for port in os.listdir('/dev') if port.startswith('tty') and (port.startswith('ttyUSB') or port.startswith('ttyACM'))]
            if not ports:
                print("No available serial ports were found.")
            else:
                print("Available serial ports: ")
                for port in ports:
                    print(f"/dev/{port}")  # Display ports found in /dev
        else:
            # Fallback for non-Linux systems (Windows, macOS)
            ports = serial.tools.list_ports.comports()
            if not ports:
                print("No available serial ports were found.")
            else:
                print("Available serial ports: ")
                for port, desc, hwid in sorted(ports):
                    print(f"{port}: {desc} (ID: {hwid})")
                           
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
            print(f"Serial connection opened on {self.port}!") #prints which cport is connected
        except serial.SerialException as e:
            print(f"Serial connection failed: {e}")
            self.ser = None
            
    # Method to check if the connection is open
    def is_connected(self):
        return self.ser is not None and self.ser.is_open
            
    def close_conn(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed!")
            
    def checksum(self, data):
        checksum = 0x34
        return checksum
            
    def create_packet(self, function_code, data):
        sync = 0x16
        packet = struct.pack('B', sync)
        packet += struct.pack('B', function_code)
        
        if data:
            packet += struct.pack(f'{len(data)}B', *data)
            
        checksum = self.checksum(packet)
        packet += struct.pack('B', 0x34)
        
        return packet
    
    def send_packet(self, function_code, data=None):
        if not self.ser or not self.ser.is_open:
            self.open_conn()
            
        if self.ser is None or not self.ser.is_open:
            print("Failed to open serial connection. Cannot send packet.")
            return

        packet = self.create_packet(function_code, data if data else [])
        self.ser.write(packet)
        print(f"Sent packet: {packet}")

        self.close_conn()

    def receive_packet(self):
        if not self.ser or not self.ser.is_open:
            self.open_conn()
            
        if self.ser is None or not self.ser.is_open:
            print("Failed to open serial connection. Cannot receive packet.")
            return None

        expected_packet_size = 37  
        packet = b""
        while len(packet) < expected_packet_size:
            chunk = self.ser.read(expected_packet_size - len(packet))
            if not chunk:
                print("Timeout while reading packet")
                return None
            packet += chunk

        print(f"Raw packet: {packet}")
        if len(packet) != expected_packet_size:
            print(f"Incomplete packet received. Length: {len(packet)}")
            return None
        
        """
        if self.sync != 0x16:
        print(f"Invalid sync byte: {sync}")
        return None
        """
        """packet = self.ser.read(37)
        if len(packet) < 37:
            print("Invalid packet received")
          #  self.close_conn()
            return None
        """    
    
        sync, function_code = struct.unpack('BB', packet[:2])   # Unpack the syncbyte(h16) & function code(h49-echo) (should both be 1 byte)
        data = packet[2:-1] # Data is everything except the sync byte and checksum
        checksum = packet[-1]
        checksum = struct.unpack('B', bytes([checksum]))[0]
        
        #validate checksum
        ''' 
        calculated_checksum = self.checksum(packet[:-1])    # Checksum excluding the checksum byte
        if checksum != calculated_checksum:
            print("Invalid checksum")
          #  self.close_conn()
            return None
        '''
        print(f"Received packet:\nFunction Code: {function_code}, Data: {data}")
        #self.close_conn()
        return function_code, data
    
    def receive_data_continuously(self, callback):
        if not self.ser or not self.ser.is_open:
            self.open_conn()

        if not self.ser or not self.ser.is_open:
            print("Failed to open serial connection. Cannot receive data.")
            return

        print("Starting to receive data...")

        try:
            while True:
                if not self.ser or not self.ser.is_open:
                    print("Serial connection lost. Stopping thread")
                    break
                    
                # Attempt to receive a packet
                packet = self.receive_packet()
                if packet:
                    function_code, data = packet
                    callback(data)
                    # Process received data here (you can add your own logic)
                    print(f"Processed data: {data}")
                
                # Optional: Add a small delay to avoid overloading the CPU or serial buffer
                time.sleep(0.1)

        except Exception as e: #KeyboardInterrupt:
           print(f"Error in receive_data_continuously: {e}")
           # print("Receiving interrupted by user.")

        finally:
            self.close_conn() #for testing
    def request_egram(self):
    #request egram data from the pacemaker by sending k_egram function code (0x10)
        function_code = 0x10
        data = []
        self.send_packet(function_code, data)
        print("Requested egram data from pacemaker")
        
    def stop_egram(self):
        #stop egram data transmission by sendinf the k_estop function code (0x11)
        
        function_code = 0x11
        data = []
        self.send_packet(function_code, data)
        print("Sent stop egram request to pacemaker")
        
    def parse_egram_data(self, packet):
        #Parse egram data received from the pacemaker
        if len(packet) < 6:
            print("Invalid egram packet received")
            return None
        
        sync,fn_code = struct.unpack('BB', packet[:2]) 
        v_raw, f_marker = struct.unpack('HH', packet[2:6])
        checksum_received = packet[-1] 
        
        calculated_checksum = self.checksum(packet[:-1])    # Checksum excluding the checksum byte
        if checksum_received != calculated_checksum:
            print("Invalid checksum for egram packet")
            return None
        
        return [v_raw, f_marker]
    
        
            
            
    

#example testing

'''if __name__ == "__main__":
    comm = serialCommunication(port='COM3', baudrate=57600)
    comm.send_packet(0x55, [1, 2, 3, 4]) #test
    comm.receive_data_continuously()  # Start receiving data from Simulink
#   response = comm.receive_packet()
 #   if response:
  #      function_code, data = response
   #     print(f"RECEIVED\nfunction code: {function_code}, data: {data}")'''