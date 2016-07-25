from gpiozero import LightSensor
from time import clock, sleep

ldr = LightSensor(16)

count = 0
time_shaded = 0

def poll_high_five():
    global count
    global time_shaded
    time_now = clock()
    if ldr.value < 0.65:
        time_shaded = time_now
    elif time_shaded > 0 and time_now - time_shaded > 0.4:
        count += 1
        time_shaded = 0

    return count

if __name__ == "__main__":
    prev_count = -1
    while True:
        new_count = poll_high_five()
        if new_count > prev_count:
            print new_count
            prev_count = new_count
        sleep(0.05)
