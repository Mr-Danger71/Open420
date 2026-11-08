# Firmware

The Following is the Open420 Firmware folder that is all licensed under [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt).

Firmware is currently under heavy revision and this file and files in firmware are expected to change snigifantly.

### Firmware Layout

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

## basefirm

**basefirm** is the C++20 Application that runs on Zephyr RTOS that is the foundation for every other feature, driver, and expanision module that can connect to or is used on the origional board and hardware for Open420.

More details on basefirm can be found in the [basefirm Roadmap](https://github.com/Mr-Danger71/Open420/blob/main/docs/basefirm%20Roadmap.md)