# hydroqc2mqtt

**The full updated project documentation can be found at [https://hydroqc.ca](https://hydroqc.ca)**

We have a discord server where you can come to discuss and find help with the project [https://discord.gg/2NrWKC7sfF](https://discord.gg/2NrWKC7sfF)

This module extracts data from your Hydro-Quebec account using the [Hydro Quebec API Wrapper](https://gitlab.com/hydroqc/hydroqc) and will post it to your MQTT server. Home-Assistant MQTT Discovery topics are also provided, automating the creation of your sensors in Home-Assistant.

We have implemented a feature that will send historical hourly consumption from Hydro-Quebec to your Home-Assistant statistics to be used in the Energy Dashboard. This feature does not work over MQTT but send the information directly to Home-Assistant via Websocket.

## Donations

We put a lot of heart and effort in this project, any contribution is greatly appreciated!

[![Donate](https://img.shields.io/badge/Donate-Hydroqc-green)](https://hydroqc.ca/en/donations)
## Disclaimer
### **Not an official Hydro-Quebec API**

This is a non official way to extract your data from Hydro-Quebec, while it works now it may break at anytime if or when Hydro-Quebec change their systems.
### **Special message to Hydro-Quebec's employees**

We would very much like to improve this module and it's [API](https://gitlab.com/hydroqc). We tried to reach out to HQ but never were able to get in contact with anyone there interested in discussing this project. If you have some feedback, complaints or are interested to discuss this project, please reach out to us on our [development discord channel](https://discord.gg/NWnfdfRZ7T).
