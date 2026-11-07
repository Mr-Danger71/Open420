# Prototype Parts Lost

The following is the parts selected for the protoyping of the Open420 v1 Board.

**Check Before Ordering**

- Pick the <u>**UHF (U)**</u> option on the SA818S listing, <u>**DO NOT** Select VHF</u>
- Ham radio uses plain **SMA**, not RP-SMA (Wi-Fi). Chinese part numbers use **J = male, K = female**.
- **SMA-K (F) on radio side | SMA-J (M) Antenna**. Baofeng-style convention.

| Block | Choice | Qty | Link | Notes |
| --- | --- | --- | --- | --- |
| MCU | NUCLEO-U575ZI-Q | 1 | [DigiKey](https://www.digikey.com/short/dhw97p79) | Built-in STLINK-V3 programmer. Zephyr board: `nucleo_u575zi_q` |
| RF | SA818S-U (400–470 MHz) | 1 | [AliExpress](https://www.aliexpress.us/item/3256807926261125.html) | Select the **UHF** option. Castellated pads, **no u.FL connector** |
| RF Connector | SMA-KE female jack, through-hole PCB mount (straight) | 1 | [AliExpress](https://www.aliexpress.us/item/3256808128195000.html) | 50 Ω, DC-12.4 GHz, VSWR ≈ 1.10 at 435 MHz. Solder beside the SA818: ANT -> center pin ≤5 mm, all four ground posts -> SA818 GND |
| Antenna | TC-213UV-J | 1 | [AliExpress](https://www.aliexpress.us/item/3256807865368396.html) | `-J` = SMA male. Confirm the connector option on the listing matches the SMA-K pigtail |
| Audio amp | PAM8302 2.5 W class-D | 1 | [AliExpress](https://www.aliexpress.us/item/3256806228764878.html) | 2.0–5.5 V supply. `SD` pin goes to SA818 Audio ON / MCU |
| Bulk cap | UVR1C471MPD1TD (220–470 µF electrolytic, ≥10 V) | 2 | [DigiKey](https://www.digikey.com/short/wnm0qjzh) | Across SA818 `VBAT`/`GND`, as close to the module as possible |
| Decoupling cap | A104K15X7RF5UAAP (100 nF ceramic) | 5 | [DigiKey](https://www.digikey.com/short/jwb89p04) | One at the SA818 `VBAT` pin, spares for the amp |
| Speaker / mic | Stock walkie-talkie speaker + electret mic | 1 each | (salvaged) | Mic needs 2.2 kΩ bias from 3.3 V + coupling cap into `MIC_IN` |
| Prototyping | Perfboard, 2.54 mm headers, jumper wires | - | (on hand) | |

| Block | Choice | Qty | Link | Notes |
| --- | --- | --- | --- | --- |
| MCU | NUCLEO-U575ZI-Q | 1 | [DigiKey](https://www.digikey.com/short/dhw97p79) | Built-in STLINK-V3 programmer. Zephyr board: `nucleo_u575zi_q` |
| RF | SA818S-U (400–470 MHz) | 1 | [AliExpress](https://www.aliexpress.us/item/3256807926261125.html) | Select the **UHF** option. Castellated pads, **no u.FL connector** |
| RF Connector | SMA-KE female jack, through-hole PCB mount (straight) | 1 | [AliExpress](https://www.aliexpress.us/item/3256808128195000.html) | 50 Ω, DC-12.4 GHz, VSWR ≈ 1.10 at 435 MHz. Solder beside the SA818: ANT -> center pin ≤5 mm, all four ground posts -> SA818 GND |
| Antenna | TC-213UV-J | 1 | [AliExpress](https://www.aliexpress.us/item/3256807865368396.html) | `-J` = SMA male. Confirm the connector option on the listing matches the SMA-K pigtail |
| Audio amp | PAM8302 2.5 W class-D | 1 | [AliExpress](https://www.aliexpress.us/item/3256806228764878.html) | 2.0–5.5 V supply. `SD` pin goes to SA818 Audio ON / MCU |
| Bulk cap | UVR1C471MPD1TD (220–470 µF electrolytic, ≥10 V) | 2 | [DigiKey](https://www.digikey.com/short/wnm0qjzh) | Across SA818 `VBAT`/`GND`, as close to the module as possible |
| Decoupling cap | A104K15X7RF5UAAP (100 nF ceramic) | 5 | [DigiKey](https://www.digikey.com/short/jwb89p04) | One at the SA818 `VBAT` pin, spares for the amp |
| Speaker / mic | Stock walkie-talkie speaker + electret mic | 1 each | (salvaged) | Mic needs 2.2 kΩ bias from 3.3 V + coupling cap into `MIC_IN` |
| Prototyping | Perfboard, 2.54 mm headers, jumper wires | - | (on hand) | |
