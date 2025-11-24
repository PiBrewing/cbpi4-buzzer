# CBPi4 Buzzer Plugin

## Buzzer Plugin calls buzzer on cbpi notifications

- Settings will be added by this plugin
- buzzer_gpio: GPIO your buzzer is conected to
- buzzer_gpio_inverted: Set to 'yes', if your buzzer is connected via inverted GPIO (High on Low)
- buzzer_level: Sound level(High or Low)
- Different sounds for error, warning and other message types

### Installation:

Please have a look at the [Craftbeerpi4 Documentation](https://openbrewing.gitbook.io/craftbeerpi4_support/readme/plugin-installation)

- Package name: cbpi4-buzzer
- Package link: https://github.com/PiBrewing/cbpi4-buzzer/archive/main.zip

### Changelog

- 24.11.25: (0.1.0) Add pyproject.toml to support pip 25.3+
- 25.06.23: (0.0.8) internal change on startup with respect to logging of parameter check for gpio_inverted
- 10.06.23: (0.0.7) fix issues in setup.py
- 10.06.23: (0.0.6) bump version to release
- 02.06.23: (0.0.6.rc1) added cbpi version requirement
- 16.04.23: (0.0.6.a4) bug fix for parameter generation
- 05.04.23: (0.0.6.a3) Test for plugin settings selection test branch of cbpi
- 12.03.23: (0.0.4) Added option for inverted GPIO
- 10.04.21: (0.0.3) changed from asyncio.sleep to a thread as buzzer sound was impacted by asyncio.sleep accuracy
- 01.04.21: Initial release
