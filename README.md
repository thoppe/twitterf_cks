# Twitter fucks

A statistical and orthographic study of fucks on twitter.

![Fuck_per_city](figures/fucks_given_per_city.png "Fucks per city")

### Data collection

    python src/scrape.py

Requires a file in the local directory named `access_tokens.json` with the following keys:

``` python
{
    "key":"XXXXXXXXXXXXXXXXXXXXXXXXX",
    "secret":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "access":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "access_secret":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

### Geo processing

Count and collapse data over geolocations

    python src/geo_count.py
    
### Plotting

Plot propensity over the cities

    python src/plot_cities.py