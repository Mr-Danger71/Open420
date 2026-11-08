# basefirm Roadmap
 
**basefirm** is the core firmware for the Open420 main board: the foundation every other feature,
driver and expansion module builds on. It is written in C++20 on Zephyr RTOS and targets the
STM32U575 (`nucleo_u575zi_q` for prototyping, `native_sim` for testing on a PC).
 
**Build order: easy to complex.** Everything that doesn't touch hardware comes first and is
unit-tested on `native_sim`. Hardware drivers come last and plug in behind interfaces that
already exist.
 
---
 
## Design decisions
 
| Area | Decision |
| --- | --- |
| Language / RTOS | C++20 on Zephyr. No exceptions, no RTTI, no heap after startup |
| Internal messaging | Zephyr **zbus** publish/subscribe. Drivers publish events; services react |
| Testing | Zephyr **ztest** on `native_sim`, run in CI on every push |
| Channels | 10 programmable channels, saved to flash, selected by a 10-position **BCD rotary dial** |
| Channel announcement | Turning the dial announces the new channel, e.g. *"Channel 4, 448.0"* |
| Transmit timeout | **60 s**, warning beep at **50 s**. After a timeout, PTT must be released and pressed again to transmit |
| Preamble | **600 ms** wake-up preamble before voice, then a **talk-permit tone** |
| Battery saver | Receiver awake **100 ms** of every **500 ms** while idle; Audio ON wakes the MCU |
| Region | Transmit limited to the configured amateur band (US default: 420–450 MHz) |
 
### Channel dial behavior
 
- **Responsive:** each BCD line uses an external high-value pull-up (470 kΩ–1 MΩ) and a pin-change
  interrupt, so a turn is detected instantly with only a few µA of standby current.
- **Debounce:** a reading counts only after it is stable for ~20–30 ms. BCD is not Gray code, so
  in-between positions can briefly read as the wrong channel while the dial is moving.
- **Settle, then speak:** the announcement starts ~150–300 ms after the dial stops, so spinning
  past several positions announces only where it lands.
- **Interruptible:** turning the dial again cuts off an announcement in progress.
### Channel data
 
| Field | Notes |
| --- | --- |
| RX frequency | Hz, validated against the region band plan |
| TX frequency | Same as RX for simplex; offset for repeaters (70 cm is commonly ±5 MHz) |
| TX / RX tone | CTCSS or DCS, or none |
| Bandwidth | 12.5 or 25 kHz |
| Power | High or low |
| Name | Optional, for the USB CLI and future screen versions |
 
---
 
## Firmware layout
 
```
firmware/
├── basefirm/              Zephyr application for the main board
│   ├── CMakeLists.txt, prj.conf, Kconfig
│   ├── boards/            nucleo_u575zi_q.overlay, native_sim.overlay
│   └── src/
│       ├── core/          events, state machine, channels, settings
│       ├── services/      prompts, battery saver, shell commands
│       └── drivers/       sa818, audio, inputs, power
└── tests/                 ztest suites that run on native_sim
```
 
---
 
## Milestones
 
### M1 — Skeleton
 
- [ ] Move the blinky app into `firmware/basefirm/` and update the CI build path
- [ ] Logging and a firmware version string
- [ ] Zephyr shell with `o420 version`, running on `native_sim` and the Nucleo
- [ ] First ztest suite running in CI
**Done when:** `o420 version` works on both targets and CI runs the tests.
 
### M2 — Channels
 
- [ ] Channel data structure and validation (band limits, tone and bandwidth values)
- [ ] Save and load all 10 channels to flash (Zephyr settings)
- [ ] Shell commands: `channel show`, `channel set <n> rx <MHz>` and the other fields
- [ ] Tests: invalid frequencies rejected, settings survive a reboot
**Done when:** channels can be programmed from the shell and persist across restarts.
 
### M3 — Event bus and simulated inputs
 
- [ ] zbus channels for inputs (PTT, dial position, mute) and radio status (Audio ON, battery)
- [ ] Simulated inputs from the shell: `sim ptt press`, `sim dial 4`, `sim audio-on`
- [ ] Dial debounce and settle logic (see *Channel dial behavior*)
**Done when:** simulated inputs drive events that other modules can subscribe to.
 
### M4 — Radio state machine
 
- [ ] States: `BOOT`, `RX_IDLE`, `SLEEP`, `RX_ACTIVE`, `TX_PREAMBLE`, `TX_ACTIVE`, `TX_TIMEOUT`, `LOW_BATT`, `OFF`
- [ ] 600 ms preamble, then the talk-permit tone
- [ ] 60 s transmit timeout with the 50 s warning and release-to-retransmit
- [ ] Transmit blocked outside the region band
- [ ] Tests using Zephyr's simulated time for every timer
**Done when:** every transition is covered by a test.
 
### M5 — Prompt sequencer
 
- [ ] Turn a channel and frequency into a clip list: *"channel", "four", "four", "four", "eight", "point", "zero"*
- [ ] Prompt priority and interruption (a dial turn cancels an announcement in progress)
- [ ] Prompts: channel change, talk permit, timeout warning, low battery
**Done when:** tests confirm the clip sequence for every channel format.
 
### M6 — Battery saver
 
- [ ] 100 ms / 500 ms receive duty cycle driven by the state machine
- [ ] Wake on Audio ON, back to sleep after a period of silence
- [ ] Tests for the timing and wake behavior
**Done when:** sleep and wake timing are verified in simulation.
 
---
 
## Drivers (after basefirm)
 
Each driver implements an interface the services already use, so the simulated version is simply swapped for the real one.
 
- [ ] **Inputs:** PTT, mute switch, BCD channel dial (GPIO interrupts)
- [ ] **Power:** battery ADC, charger status (CHG / PGOOD), soft-latch
- [ ] **Audio:** DAC prompt playback, amp enable
- [ ] **SA818:** UART AT commands, PTT / PD / H/L control, Audio ON input