# flagsy

A board game to help kids to learn world countries' flags.

## How to play

Very simple: shuffle all cards, deal 4 to each participant, "big flag picture" up. In turn, each participant proposes one of own card and tries to "guess" to which country it belongs.

If nailed it, the card is discarded, the participant has a card less, if zero he/she wins.

If wrong, the card is discarded, the partipant gets another one from the deck.


## What this project is about

Tools and whatever necessary to build PDFs/images/files to build the game.


### Components/parts/information:

- Raw information; for each country:
    - its name
    - its flag
    - other textual info (capital city, languages, continent, etc.)
    - an image representing the position of the country in the world map

- Look and feel of each card
    - side A: a generic background (ToDo) with country's big flag
    - side B: same generic background, with all the rest of the info; need a design here (ToDo)

- Tools/steps for putting everything together


### Steps

1. Run `get_countries_data.py`, will leave a json with some data for all countries

2. Run `get_coi_data.py`, will leave a json with some data for COI codes

3. Run `fill_country_info.py', which will improve each item in the countries json data
