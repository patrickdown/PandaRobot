from math import ceil

ldr = None

try:
    from gpiozero import LightSensor
    ldr = LightSensor(16)
except ImportError:
    pass

activation_value = 0.65 # value below which the sensor is considered activated
hold_length = 0.4 # Amount of time in secods the sensor needs to be held
sampling_rate = 20.0 # Number of times per second tha we are going to read the sensor

number_of_samples = ceil(sampling_rate * hold_length)

sample = [1.0] * int(number_of_samples) # array to hold samples
current_sum = number_of_samples
current_sample = 0

sensor_active = False
high_five_count = 0

def sensor_toggled(value):
    global current_sum
    global current_sample
    global sensor_active
    # compute moving average of senesor values
    current_sum -= sample[current_sample]
    current_sum += value
    sample[current_sample] = value
    current_sample = (current_sample + 1) % len(sample)

    average = current_sum / number_of_samples

    # Increment the count
    if average < activation_value:
        # but only if it's not been prev counted
        if not sensor_active:
            sensor_active = True
            return True
        else:
            pass
    else: # Has to becove inactive before we reset
        sensor_active = False

    return False

# Use data from actual sensor
def poll_high_five():
    global high_five_count
    if sensor_toggled(ldr.value):
        high_five_count += 1
    return high_five_count

#use fake data 
def test_high_five():
    count = 0
    for i in range(int(number_of_samples) * 2):
        if sensor_toggled(activation_value - 0.01):
            count += 1
    assert(count == 1)
    for i in range(int(number_of_samples) * 2):
        if sensor_toggled(activation_value + 0.01):
            count += 1
    assert(count == 1)
    for i in range(int(number_of_samples) * 2):
        if sensor_toggled(activation_value - 0.01):
            count += 1
    assert(count == 2)

# if run with 'test' parameter then test otherwise use sensor data
if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2 and argv[1] == 'test':
        test_high_five()
    else:
        prev_count = -1
        while True:
            new_count = poll_high_five()
            if new_count > prev_count:
                print new_count
                prev_count = new_count
            sleep(1.0/sampling_rate)
