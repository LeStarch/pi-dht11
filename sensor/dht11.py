try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Super-user access needed",file=sys.stderr)
import time

class HTSensor:
    '''
    Interfaces with the DHT-11 temperature sensor to gather temperature and humidity.
    @author lestarch
    '''
    def __init__(self, pin):
        '''
        Initializes the pin
        pin - pin number to read 
        '''
        tmp = GPIO.getmode()
        if tmp == GPIO.BCM:
            raise RuntimeError("Incompatible GPIO pin enumeration scheme")
        GPIO.setmode(GPIO.BOARD)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT,initial=GPIO.HIGH)
    def read(self):
        '''
        Starts the reading
        '''
        vals = [None] * 4000
        times = [None] * 4000
        # Send 19ms start pulse
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.019000)
        # Switch to input and read
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN)
        readings = sequence(self.pin,vals,times)
        if detect(readings,GPIO.LOW) < 40:
            raise ReadError("Failed to get sensor 80µs response")
        if detect(readings,GPIO.HIGH) < 40:
            raise ReadError("Failed to get sensor 80µs rest")
        # Read 5 bytes of 8 bits each (40 bits)
        lst = []
        for i in range(0,5):
            byt = 0
            for j in range(0,8):
                byt = (byt << 1) | self.bit(readings)
            lst.append(byt)
        # Checksum calculation
        cksum=(lst[3] + lst[2] + lst[1] + lst[0]) & 0xFF
        if lst[4] != cksum:
            raise ChecksumError("Checksum calculation failed: "+str(cksum)+" != "+str(lst[4]))
        GPIO.setup(self.pin, GPIO.OUT,initial=GPIO.HIGH)
        return (lst[0],lst[2])
    def bit(self,readings):
        '''
        Read a bit (less than 70 microseconds is a 0)
        readings - array of read values
        '''
        if detect(readings,GPIO.LOW) < 30:
            raise ReadError("Failed to get sensor 50µs setup bit")
        dur = detect(readings,GPIO.HIGH)
        if dur < 6:
            raise ReadError("Failed to get sensor data")
        if dur > 70-30:
            return 1
        return 0
    def cleanup(self):
        ''' Cleanup '''
        GPIO.cleanup(self.pin)
def sequence(pin,vals,times):
    '''
    Read pin in a tight loop
    pin - pin to read
    vals - values array to fill
    times - times array to fill
    '''
    # Super tight loop to read 
    i = len(vals)-1
    while i >= 0:
        times[i] = time.time()
        vals[i] = GPIO.input(pin)
        i = i - 1
    # Now zip up result and reverse
    readings = list(zip(times,vals))
    readings.reverse()
    return readings
def detect(readings,val):
     '''
     Find duration of saught value.
     readings - list of results to search
     val - value looking for
     '''
     try:
         time,read = readings.pop(0)
         otime = time
         while read != val:
             otime = time
             time,read = readings.pop(0)
         start = otime
         while read == val:
             time,read = readings.pop(0)
         tm = (time-start)*1000000
     except IndexError:
         raise ReadError("Device responded improperly")
     return tm 
class ReadError(Exception):
    ''' Error upon reading '''
    pass
class ChecksumError(ReadError):
    ''' Checksum missmatch '''
    pass
