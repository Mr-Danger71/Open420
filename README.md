<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/open420-logo-3d-topdown-white.svg">
    <img src="assets/open420-logo-3d-topdown-black.svg" alt="Open420 logo" width="320">
  </picture>
</p>

<h1 align="center">Open420</h1>

<p align="center"><b>An open-source, repairable 70 cm (420–450 MHz) amateur radio handheld.</b><br>
Named for 420 MHz, the bottom edge of the US 70 cm amateur band.</p>

---

**Status: early design / prototyping.** Expect Major Revisions to everything.

## What it is

Open420 is a handheld UHF transceiver designed to be fully open: schematics, PCB, firmware and a 3D-printable enclosure are all published so anyone can build, repair, modify and extend it.

### Planned v1 architecture

| Block | Choice |
|---|---|
| RF | NiceRF SA818S-U module (400–480 MHz, 0.5 / 1 W) |
| MCU | STM32U575 (Cortex-M33) |
| Firmware | Zephyr RTOS, application in C++ |
| Power | 1S Li-ion, USB-C charging with power path, low-Iq 3.3 V LDO |
| RF output | 7-pole Chebyshev low-pass filter, SMA antenna connector |
| Audio | Electret mic, class-D speaker amp, MCU voice prompts |
| Expansion | Module header (power, I²C, SPI, UART, IRQ) with ID EEPROM |
| Enclosure | Fully 3D-printable |

### Transparency note

The SA818S RF module is a closed, proprietary part controlled over a documented AT-command interface. Open420 uses it only for its RF functions. Everything else in the design is open. A fully open RF section is a long-term goal.

## Legal notice

- **Transmitting requires an amateur radio license.** In the US, a Technician-class license (FCC Part 97) is the minimum to operate on 70 cm.
- **Building or modifying** the hardware and firmware requires no license. Test the transmitter into a dummy load until you are licensed.
- **Outside the US**, check your country's amateur regulations and band plan (for example, 70 cm is 430–440 MHz in IARU Region 1). The firmware will enforce a configurable region band limit.
- Encryption of on-air traffic is not permitted on amateur frequencies and is not part of this project.

## Repository layout

```
firmware/    Zephyr application (C++)
hardware/    KiCad schematics and PCB
enclosure/   3D-printable case (STEP, STL/3MF, link to CAD source)
docs/        Design notes and build guides
assets/      Logos and artwork
LICENSES/    Full license texts
```

## Building the firmware

```bash
mkdir open420-ws && cd open420-ws
git clone https://github.com/Mr-Danger71/Open420.git
west init -l Open420
west update
west build -p always -b nucleo_u575zi_q Open420/firmware/basefirm
```

See the [Zephyr Getting Started guide](https://docs.zephyrproject.org/latest/develop/getting_started/index.html) for toolchain setup.

## License

Open420 is licensed per component (see `REUSE.toml`):

| Component | License |
|---|---|
| Hardware (`hardware/`, `enclosure/`) | [CERN-OHL-S-2.0](LICENSES/CERN-OHL-S-2.0.txt) |
| Firmware (`firmware/`) | [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt) |
| Docs and artwork (`docs/`, `assets/`, this README) | [CC-BY-SA-4.0](LICENSES/CC-BY-SA-4.0.txt) |

Derivative designs must keep all existing copyright notices, so every contributor in the chain stays credited.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All commits require a DCO sign-off (`git commit -s`).
