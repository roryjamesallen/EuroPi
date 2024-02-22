# EuroPi X

#### 13/03/2023 - EuroPi-X Discord channel is created
The EuroPi-X Discord channel is created and feature discussions began

#### 13/03/2023 - Enoki
Toadstool Tech Enoki becomes a front runner for the OLED display (128x64 SSD1306, I2C)

#### 19/04/2023 - Routing begins for prototype 1
KiCad development of prototype 1 begins, and PCB development follows

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/7c565093-3bae-4b18-a76a-cdc466a3cfea)

#### 23/04/2023 - Hardware configuration pins
The idea to use GPIO pins of the RP2040 to allow the hardware to 'detect' what model it is is added to the design for prototype 1

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/a35759b2-12fd-4330-9e7f-8c54f81d3ee8)

#### 28/04/2023 - QR code added to PCB
![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/4e3c1ff9-d688-467a-990b-833684b4906d)

#### 02/06/2023 - Prototype 1 PCBs arrived
Testing showed *a lot* of issues. The main ones discovered were:
- Power protection diodes soldered in reverse
- USB-C CC resistors not included
- 3.3V regulator pinout incorrect so non-working
A lot of bodging later and still no sign of life from the RP2040

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/975e607d-b74b-45a0-bb2a-64489c14d2bc)

Enoki PCBs arrived, and the FPC connector is on backwards so it's impossible to fit the display with the pins in the correct order

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/fb9f99c1-0c01-4968-b200-e23ba742d63e)

#### 04/10/2023 - Building blocks idea
I had the idea to start prototyping using smaller blocks, which really I should've done to begin with, and would've done if not for overconfidence

#### 15/01/2024 - The first building blocks
KiCad projects for the building blocks begin to come together

#### 31/01/2024 - Building blocks order
A panelised PCB with the input stage, output stage, and Enoki was ordered from JLC

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/9011a8ff-97ef-4ec7-beaa-0a3b44cd65ce)

#### 13/02/2024 - Enoki lives!
Basic testing of the Enoki boards proved the design to work. The only alterations needed before a final version are:
- Add an RC circuit to the reset pin so that it is held low during startup
- Make the I2C jumpers closed by default rather than open (or pull them to the other rail and use open jumpers again)
- Move the FPC connector so that there isn't slack in the ribbon cable at the bottom

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/65c8164e-f000-4cd5-a37c-f7de7897abff)

PR submitted and merged to allow the menu to display on the taller display and lay groundwork for rewriting scripts in a way that fully respects the ability for the display to be differerent dimensions as defined in config settings

#### 21/02/2024 - Analogue input testing
Successful testing and software development of the analogue input building block PCB. Input detection works consistently, and analogue voltage is detected, however a mistake in resistor values means the range is set at 0-3V into the ADC despite the ADC range being 0-2.048V, so negative voltages lower than ~2V cannot be read

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/fcf70bad-958e-4776-b045-4cc93729183d)

Input detection works for all 4 channels, but a yet undetermined issue is causing the ADC to not read channel 4. All other 3 channels work perfectly

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/1063a4a7-e716-4d2a-b3b2-b2bd6dc89bfd)

The software wrappers for using the new outputs is beginning to take shape. Input detection implementation will need extra components compared to what was initially expected as the jack must have a direct connection to the GPIO to allow hardware interrupts to be used for digital communication. The current proposal is to use a transistor, resistor, and diode per input as per the current EuroPi hardware digital input

#### 22/02/2024 - Analogue input development
To fix the input range error, digital input stage, and bipolar control, I designed a new circuit which uses an analogue switch (one for all 4 inputs, polarity setting is global) to allow ±5V or 0-10V input, with the entire ADC range used for either. Even though the MCP6004 only clamps the signal to 0-3.3V, the ADC's input limits are to VDD (3.3V as well) and not 2.048V, so the reading will just clip rather than damage the IC

![image](https://github.com/roryjamesallen/EuroPi/assets/79809962/8d14d592-1124-45cf-b7cf-e3d282a928f0)
