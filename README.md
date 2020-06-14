# flagsy

A board game to help kids to learn world countries' flags.

## How to play

Very simple: shuffle all cards, deal 4 to each participant, "big flag picture" up. In turn, each participant proposes one of own card and tries to "guess" to which country it belongs.

If nailed it, the card is discarded, the participant has a card less, if zero he/she wins.

If wrong, the card is discarded, the partipant gets another one from the deck.

Variations can be made as the cards have other country info (e.g., to get rid of the card the participant must guess the country name and its capital).


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

1. Go to `raw` subdir:

    1.1. Run `get_countries_data.py`, will leave a json with some data for all countries

    1.2. Run `get_coi_data.py`, will leave a json with some data for COI codes

    1.3. Run `fill_country_info.py', which will improve each item in the countries json data

    1.4. Run `download_images.py`, which will leave a `images` directory

2. Move metadata and images from raw to art directory:

    ```
    mv raw/countries_data.json art/
    mv raw/images/ art/
    ```

3. Got `art` subdir:

    3.1. Run `convert_images.py` to get all images as PNGs

    3.2. Run `generate_cards.py` to generate all PDFs with the cards

    3.3. Smash all of them together for easier inspection: 

    ```
    pdftk result/card-back*pdf cat output ../final-back.pdf
    pdftk result/card-front*pdf cat output ../final-front.pdf
    ```

4. Print them, and play
