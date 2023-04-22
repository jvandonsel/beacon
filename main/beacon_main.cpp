/*
 * Weather Beacon for ESP32
 *
 * Author: J Van Donsel
 * Date: 4/22/2023
 */

#include <math.h>
#include <stdio.h>

#include <iostream>
#include <string>

#include "esp_console.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"

/**
 * Constants
 */

// Non-volatile storage (NVS) keys
const char NVS_KEY_HOME[] = "home";

/**
 * Globals
 */


/**
 * Console command handler for printing the about message
 */
static int about_handler(int argc, char **argv) {
    std::cout << "Weather Beacon" << std::endl;
    std::cout << "Designed and built by Jim Van Donsel, April 2023." << std::endl;
    return 0;
}

/**
 * Main
 */
extern "C" void app_main() {
    nvs_flash_init();

    // Set up interactive console
    esp_console_repl_t *repl = NULL;
    esp_console_repl_config_t repl_config = ESP_CONSOLE_REPL_CONFIG_DEFAULT();
    repl_config.prompt = "beacon>";
    esp_console_dev_uart_config_t uart_config = ESP_CONSOLE_DEV_UART_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_console_new_repl_uart(&uart_config, &repl_config, &repl));

    // Add console commands
    const esp_console_cmd_t status_cmd = {
        .command = "about",
        .help = "About Weather Beacon",
        .hint = NULL,
        .func = &about_handler,
        .argtable = nullptr};
    ESP_ERROR_CHECK(esp_console_cmd_register(&status_cmd));

    // Start the console
    ESP_ERROR_CHECK(esp_console_start_repl(repl));

}
