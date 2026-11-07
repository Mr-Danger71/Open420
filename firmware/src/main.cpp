// SPDX-FileCopyrightText: 2026 Mr-Danger71 and Open420 contributors
// SPDX-License-Identifier: GPL-3.0-or-later
//
// Open420 firmware: bring-up blinky. Proves the toolchain, C++ support and
// board definition all work before real radio code lands.

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

static const gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);

int main()
{
    if (!gpio_is_ready_dt(&led)) {
        return 0;
    }
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);

    while (true) {
        gpio_pin_toggle_dt(&led);
        k_msleep(500);
    }
}
