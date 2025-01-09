# Energy Tariff Scheduler

Enables smart actions based on daily pricing from utilities.

```sh
pip install energy-tariff-scheduler
```

Full documentation: [https://craigwh10.github.io/energy-tariff-scheduler/](https://craigwh10.github.io/energy-tariff-scheduler/)

## Supported tariff's (so far)

- [Octopus Agile](https://octopus.energy/smart/agile/) (import only)
- [Octopus Go](https://octopus.energy/smart/go/) (import only)
- [Intelligent Octopus Go](https://octopus.energy/smart/intelligent-octopus-go/) (import only)

## FAQ

> Do I need my account number?

Yes, you currently need your account number and API key for the Octopus tariffs, this is documented in the relevant tariff section <a href="https://craigwh10.github.io/energy-tariff-scheduler" target="_blank">Getting API key and Account number</a>.

This is only required to fetch your latest tariff code from Octopus as to match you with the correct product and get the prices for today.

> Why are no actions running between 11pm and 12am for Octopus Agile?

This is due to data availability, Octopus only provide pricing data from 12am-11:00pm.
