
# Weather Beacon for ESP32

This project is meant to replicate the famous weather beacon from Boston's [Berkeley Building](https://en.wikipedia.org/wiki/Berkeley_Building), formerly known as the Old John Hancock Building.

This replica is housed in a small lantern and is powered by a USB cable connected to a wall adapter. An ESP32 inside the beacon connects to the local WiFi network to fetch the weather forecast for your location from a public weather API. It then lights LEDs with a color and pattern indicating the weather.

![](https://github.com/jvandonsel/beacon/blob/main/lantern.jpg)

## The Berkeley Building Weather Beacon
There's an old mnemonic poem for the color scheme of the Berkeley Building beacon:

<em>

>Steady blue, clear view.
>
>Flashing blue, clouds due.
>
>Steady red, rain ahead.
>
>Flashing red, snow instead.
</em>

The Berkeley Beacon also will flash red during baseball season to indicate that the Red Sox home game has been canceled. My ESP32 beacon doesn't.

## Materials
-  A lantern. I acquired an old ship's lantern on EBay
- [SparkFun Thing Plus](https://www.sparkfun.com/products/17381) ESP32 board. Chosen because of its external antenna connector, important if the device is mounted in a metal lantern
- [WiFi Antenna](https://www.sparkfun.com/products/18086)
- 3x IRL540PBF N-Chanel MOSFETs
- 4x [10 mm RGB LEDs](https://www.adafruit.com/product/848) 
- Resistors
- Misc. Hardware

## Hardware Notes
The IRL540PBF N-Channel MOSFETs are really handy for this sort of LED PWM application. They have a low gate-source voltage threshold and so can be driven directly from the 3.3v GPIO pins on the ESP32 for PWM control of the LEDs.

The LEDs I chose have a recommended maximum current of 20 mA per color. I used 4 LEDS in my beacon, so this is a maximum of 80 mA per color, or 240 mA total.  Resistor values were chosen to keep the current just under this per-LED current limit, with a 5V rail. They can certainly be overdriven for a brighter beacon, but obviously their lifetime will be shortened.

## Schematic
![PDF Schematic](https://github.com/jvandonsel/beacon/blob/main/beacon-schematic.pdf)


## Software Notes
This is my first time using [MicroPython](https://docs.micropython.org). It has some deficiencies, especially when it comes to threading, but it's certainly quicker to throw projects together in MicroPython than writing directly to the Espressif IDF API in C.

I ended up single-threading everything, with polling loops and using select() to watch for serial characters from the user.

There's no MicroPython type annotation library available, but comment-based type annotations kinda work, and are better than nothing.

NTP is used to determine UTC time. The Meteo weather library returns a UTC time zone offset for the given latitude/longitude along with the weather, which I use to determine local time. Local time is then used to determine a single weather forecase for the next 8 hours.  NTP on MicroPython is flaky, but more or less works.

At my family's request, the beacon stops indicating weather and turns itself into a night-light from 11:00pm to 7:00am.

The actual Boston beacon blinks with a harsh on-off pattern. I chose to produce a softer pulsing pattern using PWM.


## Construction Notes
I used perfboard and cut out a circular shape with a Dremel.  I also needed to Dremel out a hole near the metal base of the lantern to accomodate a USB plug.  Some plastic screws and standoffs were enough to hold the board in place.

![](https://github.com/jvandonsel/beacon/blob/main/lantern-bottom.jpg)


## Weather API
The beacon uses [OpenMeteo](https://open-meteo.com/en/docs) for the weather API. This API returns JSON weather info with WMO numeric weather codes rather than text descriptions.  The most severe weather during the next 8 hours is then chosen for display.

My first choice was the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) but the SSL certificate logic in MicroPython choked on the site.

## Usage Notes
The beacon must be configured with the latitude and longitude for determining local weather. In addition, the WiFi SSID and password must be set.  These are stored in non-volatile storage (NVS) on the ESP32 and will be retrieved on the next boot.

Connect a computer to the USB port, open a serial console (115200) and hit a key to enter the interactive menu. From there, you can run the following commands:

- **location** - Prompts you for latitide and longitude
- **wifi** - Prompts you for SSID and WiFi password
- **about** - Displays information about the device, including the above data
- **help** - Show menu options
- **exit** - Exit menu and return to weather operation

While the menu is active the weather polling function is paused. Type 'exit' to return to weather polling.

## Color Patterns
Solid <span style="color:blue">blue</span> - Clear

Blinking <span style="color:blue">blue</span> - Cloudy

Solid <span style="color:red">red</span> - Rain

Blinking <span style="color:red">red</span> - Snow or Thunderstorm

Solid <span style="color:magenta">magenta</span> - No WiFi connection

Solid white - No weather received, or unknown weather code
