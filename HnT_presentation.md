---- .aligncenter .bg-black
@unsplash(ASKeuOZqhYU) .dark

.text-data **TWITTER f_cks**
@h4 A geographical, statistical, and orthographic study of all the fucks on twitter.


@footer @div .wrap @div .span
 @button(href="https://github.com/thoppe/twitterf_cks") .alignleft .ghost
   ::github:: Project repo
 @button(href="https://twitter.com/metasemantic") .ghost .alignright
   ::twitter:: @metasemantic 

---- .bg-white

@h1 wait, why?

@h3 .size-80 .wrap .alignleft
    + there are a lot of _fucks_ on twitter
    + in fact, **2.3%** of all tweets on twitter contain the word _fuck_
    + yes, really
    + _..._
    + a study of twitter is a study of its users
    + coincidentally, our head of state uses twitter

---- .bg-black
@unsplash(Skf7HxARcoc) .dark

@h1 .text-landing **Methodology**

@h3 .size-80 .wrap .alignleft
    <br>
    + Open up the twitter *FIREHOSE* (60000 tweets/hr)
    + Set a US bounding box and require location
    + Collect data for two weeks ~ 10^7 tweets
    + Filter to remove matches in mentions (@'s) and links
    <br>
    [https://github.com/thoppe/twitterf_cks](https://github.com/thoppe/twitterf_cks)

---- .aligncenter .bg-black
# Geographical analysis, city level
@figure(figures/fucks_given_per_city.png)

---- .aligncenter .bg-black
# Geographical analysis, state level
@figure(figures/fucks_given_national.png)

---- .bg-black
@unsplash(zlABb6Gke24) .dark

# Least fucks given
```
State, total, # of fucks per 1000 tweets
=====================================================
MT     9976    10.4
AR     36957   11.2 
DC     94142   11.7
NE     42636   13.6
MO     108180  13.7
```

# Most fucks given
```
State, total, # of fucks per 1000 tweets
=====================================================
ND     7699     23.4
LA     216023   23.4
AZ     173604   24.8
NV     127481   25.9
CA     1377434  26.7
WY     5357     27.6
```

---- .bg-white
@unsplash(FFZjSpUwc_I) .dark

.wrap 
  # .text-landing **Orthography**
  ### Examine variations in the _spelling_, ex. fuuuck, fvck, f$$$uck, ...
  <br><br>  <br><br>  <br><br>

  ## Fucking *regex*
  ## `(f+)([aoyvu%s]+)(c+k+)` % `"!@#$%^*+-"`

----- .bg-black
.wrap
  ## Spelling Variants

  ```
word, count
==================================
fuck      248091
f*ck        1031 <---------- self-censorship?
fuckkkk      419
fuckkk       390
fvck         387
fuckk        383
fuckkkkk     337
fuuuuck      263 <---------- peak repeat?
fack         242
fuuuuuck     227
fuuuck       206 
fuckkkkkk    157
fuuuuuuck    130
fock         125
fvckk         79
fuuuuuuuck    72
  ```
  Link to [full list](data/fuck_variations.csv).

----- .aligncenter .bg-black
## Number of repeated vowels peaks at 4
@figure(figures/fuuuucks.png)

----- .wrap

@h1 .text-landing **Statistics**
"shit" is (ever so slightly) more popular than "fuck"!? <br>
List taken from Slate article [Top Swear Words on Facebook](http://www.slate.com/blogs/lexicon_valley/2013/09/11/top_swear_words_most_popular_curse_words_on_facebook.html).
```
curse, fraction of curse words
==================================
shit       0.333857
fuck       0.331616
bitch      0.125879
damn       0.088843
dick       0.027923
piss       0.026053
pussy      0.017165
crap       0.015854
asshole    0.011103
cock       0.010084
douche     0.002595
bastard    0.002477
slut       0.002449
fag        0.002342
darn       0.001761
```

----- .aligncenter
## Curse word colocation
$P(fuck|darn) \gg P(*|darn)$
$P(more\ cock|cock) \gg P(*|cock)$
$P(fuck|shit) > P(shit|fuck)$
@figure(figures/curse_colocation.png)


---- .bg-black
@unsplash(y9zUTieUc-U) .dark

@h1 .text-landing **Sentiment analysis**

#### Used [VADER](https://github.com/cjhutto/vaderSentiment) (Valence Aware Dictionary and sEntiment Reasoner), a sentiment analysis tool tuned for social media. Cat examples:
<br><br>

.wrap .text-intro
  + I hate cats.. just evil little fuckers *(-0.9137)*
  + I just want to go to fucking sleep these stupid ass cats are fighting right outside my window *(-0.8542)*
  + I just got a cat fucking drunk and he's abusive *(-0.7841)*

  <br>
  
  + Let your cat be a fucking cat. (0.0)
  + honestly scaring cats is fucking hilarious **(0.4754)**
  + I FUCKING LOVE MY CATS SO MUCH LOOK AT THIS BEAUTIFUL GUY I SWEAR WHAT A SMART LOYAL LOVING ANIMAL GIFTED TO ME **(0.9577)**


----- .size-80 .wrap

# Thanks, you.
### [https://github.com/thoppe/twitterf_cks](https://github.com/thoppe/twitterf_cks)
### [@metasemantic](https://twitter.com/metasemantic")

<br><br>

## Shoutout to Rebecca Meseroll for the fucking feedback.

