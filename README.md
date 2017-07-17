# Twitter fucks

A statistical and orthographic study of fucks on twitter.
A total of 10,740,172 tweets were collected, 228,641 contained the word fuck.
The national average is 2.1 fucks per 100 tweets.

#### Geographical analysis

Full dataset provided in [`data/fucks_to_give_geo.csv`](data/fucks_to_give_geo.csv)

![Fuck_per_city](figures/fucks_given_per_city.png "Fucks per city")
![Fuck_per_state](figures/fucks_given_national.png "Fucks per state")

State level aggregation dataset provided in [`data/fucks_to_give_geo_state.csv`](data/fucks_to_give_geo_state.csv). Top and bottom five states listed below:

| State | total tweets | Fraction of fucks per baseline of 21 fucks per 1000 tweets |
| ------| --------- |
|MT	| 9976 |0.493|
|AR	| 36957 |0.532| 
|DC	| 94142| 0.556|
|NE	| 42636|0.647|
|MO	| 108180|0.654|
| ...   | ... |... |
|ND	|7699 |	1.116|
|LA	| 216023| 	1.116|
|AZ	| 173604|	1.179|
|NV	| 127481|	1.231|
|CA	| 1377434|	1.269|
|WY	| 5357|	1.314|


#### Sentiment analysis

Full dataset provided in [`data/fucking_sentiment.csv`](data/fucking_sentiment.csv), selected fucks with the word cat in them are shown.

| cat related tweet | sentiment |
| ------| --------- |
| I hate cats.. just evil little fuckers | -0.9137|
I just want to go to fucking sleep these stupid ass cats are fighting right outside my window |	-0.8542 |
|I just got a cat fucking drunk and he's abusive | -0.7841|
| i want a cat now 😭 who the fuck am i | -0.4939|
| 🗣Let your cat be a fucking cat. | 0|
| honestly scaring cats is fucking hilarious | 0.4754 |
| aye bruh how bout you show yo cats some love too mufucka | 0.6369|
| Cats are just so fucking perfect and I love them and want them all | 0.876|
| I FUCKING LOVE MY CATS SO MUCH LOOK AT THIS BEAUTIFUL GUY I SWEAR WHAT A SMART LOYAL LOVING ANIMAL GIFTED TO ME | 0.9577| 


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

### Processing

Count and collapse data over geolocations

    python src/geo_count.py

Collect the tweets for a given keyword into a single file

    python src/collect.py

Compute sentiment analysis over the collected tweets

    python src/sentiment_analysis.py
    
### Plotting

Plot propensity over the cities

    python src/plot_cities.py
    python src/plot_states.py
