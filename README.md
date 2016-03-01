# Raspberry PI to DHT11 Temperature and Humidity Sensor

Rasberry PI integration with a DHT-11 temperature and humidity sensor. Does not require real time clock or a real time OS to function. All of this is achieved using the GPIO pins of the raspberry pi.

## Language Choice

To be clear, this sensor is not designed in a way that supports easy Python integration. A proper C/interrupt driven solution is recommended if at all possible for your project.  What is wrong? The DHT-11 temperatur and humidity sensor uses a custom communication protocol that sends timed pulses down a wire to communicate data. This means realitively high timing accuracy must be achieved. However, the python interpreter on the PI does not operate fast enough to measure the timings accurately.

**How can it work at all?** Writing the tighest loop possible in python, samples can be taken of the signal and buffered for post analysis. (https://github.com/LeStarch/pi-dht11/blob/master/sensor/dht11.py#L76-L81) Once captured, the waveform of the signal can be approximated from the captured sample points and timings can be deduced from this reconstructed waveform and converted into proper measurments. All of this happens in "post".

**So... why Python?** Simply put, this sensor was to be integrated into a pure-python project. Thus for project-level unity a pure-python solution was created.

## Known Issues

This sensor interacts quite well with the pure-python reader. There are, of course, some known issues.

- Speed: This reader is slower than the C equivalent due to the post-processing step
- Errors: The sensor occationally returns an error value. This may be due to problems with the sensor, and not the solution itself. 


Author: lestarch

