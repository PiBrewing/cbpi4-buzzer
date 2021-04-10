# CBPi4 Buzzer Plugin

## Buzzer Plugin calls buzzer on cbpi notifications

- Settings will be added by this plugin
- buzzer_gpio: GPIO your buzzer is conected to
- buzzer_level: Sound level(High or Low)
- Different sounds for error, warning and other message types

-  Changelog

**10.04.21: changed from asyncio.sleep to a thread as buzzer sound was impacted by asyncio.sleep accuracy

**01.04.21: Initial release
