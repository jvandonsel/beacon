
# Weather Beacon for ESP32

This project is meant to replicate the famous weather beacon from Boston's [Berkeley Building](https://en.wikipedia.org/wiki/Berkeley_Building), formerly known as the Old John Hancock Building.


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

## Materials
-  A lantern. I acquired an old ship's lantern on EBay
- [SparkFun Thing Plus](https://www.sparkfun.com/products/17381) ESP32 board. Chosen because of its external antenna connector, important if the device is mounted in a metal lantern
- [WiFi Antenna](https://www.sparkfun.com/products/18086)
- 3x IRL540PBF N-Chanel MOSFETs, chosen because of their low Gate-Source voltage threshold. This allows them to be driven directly from a 3.3v GPIO pin.
- [RGB LEDs](https://www.adafruit.com/product/848) 
- Resistors
- Misc. Hardware


## Construction
TODO

## Software Notes
This is my first time using [MicroPython](https://docs.micropython.org). It has some deficiencies, especially when it comes to threading, but it's certainly quicker to throw projects together in MicroPython than writing directly to the Espressif IDF API in C.

I ended up single-threading everything, with polling loops and using select() to watch for serial characters from the user.

## Weather API
The beacon uses [OpenMeteo](https://open-meteo.com/en/docs) for the weather API.  My first choice was the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) but the SSL certificate logic in MicroPython choked on the site.

## Usage Notes
The beacon must be configured with the latitude and longitude for determining local weather. In addition, the WiFi SSID and password must be set.  Connect a computer to the USB port, open a serial console(115200) and hit a key to enter the interactive console. From there, you can run the following commands:

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

Blinking <span style="color:red">red</span> - Snow

Solid <span style="color:magenta">magenta</span> - No WiFi connection

Solid white - No weather received



