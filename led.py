from machine import PWM, Pin
import utils
import time

# LED GPIO pins
RED_GPIO = 16
BLUE_GPIO = 17
GREEN_GPIO = 21

LED_PWM_PERIOD_US = 1000
DUTY_NS_HIGH = LED_PWM_PERIOD_US * 1000

class PwmPins:
    """
    Three PWM objects, one for each LED.
    """
    def __init__(self, red, green, blue):
        # type:  (PWM, PWM, PWM) -> None
        self.red = red
        self.green = green
        self.blue = blue

class RGB:
    """
    RGB Color
    """
    def __init__(self, r, g, b):
        # type:  (int, int, int) -> None
        self.red = r
        self.green = g
        self.blue = b

    def to_str(self):
        return f"r:{self.red} g:{self.green} b:{self.blue}"
    

WHITE    = RGB(0xFF, 0xFF, 0xFF)
RED      = RGB(0xFF, 0, 0)
GREEN    = RGB(0, 0xFF, 0)
BLUE     = RGB(0, 0, 0xFF)
YELLOW   = RGB(0xFF, 0x96, 0)
AQUA     = RGB(0, 0xFF, 0x96)
MAGNENTA = RGB(0xFF, 0, 0xFF)

def create_pwm_pins():
    """
    Create a PwmPins object for our 3 GPIO pins.
    @return PwmPins object.
    """
    return PwmPins(init_pwm(RED_GPIO, 1.0), init_pwm(GREEN_GPIO, 1.0), init_pwm(BLUE_GPIO, 1.0))

def init_pwm(pin, duty):
    # type:  (int, float) -> PWM
    """
    Configure the given pin for PWM.
    @param pin Pin number
    @param duty Duty cycle, 0.0-1.0
    #return 
    """
    pwm = PWM(Pin(pin))
    freq = int(1000000.0/LED_PWM_PERIOD_US)
    duty_ns =  LED_PWM_PERIOD_US * duty * 1000
    print("Setting pin " , pin, " to freq=", freq, " duty_ns=", duty_ns)
    pwm.init(freq=int(freq), duty_ns=int(duty_ns))
    return pwm


def breathe_wait(pwmPins, rgb, duration_seconds):
    # type: (PwmPins, RGB, float) -> int
    """
    Displays the "breathe" pattern. Blocks for the given time period, or until a key is hit.

    @param pwms PWM object
    @param rgb RGB color to display
    @param duration_seconds Duration to display pattern. After duration has expired
           we will exit after the next full cycle.
    @return 0 if timeout expired, 1 if key was hit
    """
    # Start fully on
    duty_ns = DUTY_NS_HIGH
    step_ns = 5000
    direction = -1
    start_time_secs = time.time()
    while not utils.read_one_char():
        pwmPins.red.duty_ns(int(rgb.red * duty_ns/ 255))
        pwmPins.green.duty_ns(int(rgb.green * duty_ns / 255))
        pwmPins.blue.duty_ns(int(rgb.blue * duty_ns / 255))
        duty_ns += step_ns * direction
        if duty_ns < 0:
            direction = 1
            duty_ns = 0
        if duty_ns >= DUTY_NS_HIGH:
            direction = -1
            duty_ns = DUTY_NS_HIGH
            # Check if our timer has elapsed
            if time.time() - start_time_secs > duration_seconds:
                return 0
        time.sleep(0.010)
    # Indicate that a key was hit
    return 1

def solid_wait(pwmPins, rgb, duration_seconds):
    # type:  (PwmPins, RGB, float) -> int
    """
    Displays a solid pattern. Blocks for the given time period, or until a key is hit.

    @param pwms PWM object
    @param rgb RGB color to display
    @param duration_seconds Duration to display the color
    @return 0 if timeout expired, 1 if key was hit
    """

    start_time_secs = time.time()
    while not utils.read_one_char():
        solid_rgb(pwmPins, rgb)
        # Check if our timer has elapsed
        if time.time() - start_time_secs > duration_seconds:
            return 0
        time.sleep(1)
    # Indicate that a key was hit
    return 1


def solid_(pwm, duty):
    # type: (PWM, float) -> None
    """
    Sets the given pwm pin to the given duty cycle.
    @param pwm PWM pin
    @param duty float 0.0-1.0
    """
    pwm.duty_ns(int(DUTY_NS_HIGH * duty))

def solid_rgb(pwmPins, rgb):
    # type: (PwmPins, RGB) -> None
    """
    Sets the given pwm pins to the given RGB color.
    @param pwms PWM pins
    @param rgb RGB color
    """
    print("solid_rgb", rgb.to_str())
    # Set the PWM pins to the given color.
    # Note: The PWM pins are set to a duty cycle of 1.0, so we divide the
    #       color values by 255.0 to get the actual duty cycle.
    solid_(pwmPins.red, rgb.red / 255.0)
    solid_(pwmPins.green, rgb.green / 255.0)
    solid_(pwmPins.blue, rgb.blue / 255.0)
    


