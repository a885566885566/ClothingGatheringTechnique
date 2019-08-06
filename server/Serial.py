import serial
import Machine

class Serial:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        self.msg = ""
        self.buf = []

    def sendCmd(self, task):
        if not ser.isOpen():
            print("Error, can not open serial")
            return
        cmd = task.encode()
        ser.write(cmd)

    def available(self):
        while ser.in_waiting:
            byte_in = ser.read(1)
            c = byte_in.decode(encoding='utf-8', 
                                 errors='ignore')
            if c == Machine.Task.ENDING_CHAR:
                self.buf.append(self.msg)
                return True
            else:
                self.msg += c
        return False

    def pop(self):
        cmd = self.buf.pop(index=0)
        # Parse needed
        return cmd

    def close(self):
        ser.close()
