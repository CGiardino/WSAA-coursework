# web-services-and-applications
Web services and applications ATU course

### Author

Carmine Giardino

## Installation

**Requirements**: Python 3.6 or higher

Before running any assignments, install the required dependencies:

```bash
pip3 install -r requirements.txt
```

This will install all necessary Python packages needed for the assignments.

## Table of Contents

- [Assignment 2: Card Draw Game](#assignment-2-card-draw-game)
- [Assignment 3: CSO dataset retrieval](#assignment-3-cso-dataset-retrieval)
- [Assignment 4: GitHub Text Replacer](#assignment-4-github-text-replacer)

## Assignment 2: Card Draw Game

A Python program that uses the [Deck of Cards API](https://deckofcardsapi.com/) to simulate dealing cards and playing a multiplayer card game.

### Features

- **Shuffle and Deal**: Automatically shuffles a new deck and deals five cards to each player
- **Hand Evaluation**: Evaluates poker-style hands including:
  - Straight flush (five sequential cards of the same suit)
  - Flush (all cards same suit)
  - Straight (five sequential cards)
  - Three of a kind (triple)
  - Pair (two cards of the same value)
  - High card
- **Multiplayer Support**: Play with 1–10 players from the same deck
- **Winner Determination**: Compares all hands and announces the winner with the winning hand type
- **Tie Handling**: Properly handles ties between multiple players

### How to Run

#### Single Player Mode (Default)
```bash
python3 assignment2-carddraw.py
```

This will deal five cards to one player and show their hand result.

#### Multiple Players (2–10 players)
```bash
python3 assignment2-carddraw.py -p 5
```

Replace `5` with any number from 1 to 10. For example:

```bash
# 3 players
python3 assignment2-carddraw.py -p 3

# Maximum 10 players
python3 assignment2-carddraw.py -p 10
```

**Note**: Maximum 10 players (52 cards in deck ÷ 5 cards per player = 10 max). If you request more than 10 players, the program will display a warning explaining the deck size limitation and limit it to 10 players.

### Example Output

#### Single Player:
```
Player 1 hand: 5 of DIAMONDS, JACK of HEARTS, KING of CLUBS, ACE of DIAMONDS, 3 of SPADES
Player 1 result: High card
```

#### Multiple Players with Winner:
```
Player 1 hand: 7 of CLUBS, 7 of HEARTS, 3 of DIAMONDS, 10 of SPADES, QUEEN of CLUBS
Player 1 result: Pair
Good job! You have a pair. Congratulations!

Player 2 hand: 4 of CLUBS, 7 of HEARTS, 10 of HEARTS, 6 of CLUBS, 5 of HEARTS
Player 2 result: High card

Player 1 wins with Pair!
```

### Command Line Options

- `-p, --players`: Number of players (1-10). Default is 1.
- `-h, --help`: Show help message and exit

### API Usage

This program uses the Deck of Cards API:
- **Shuffle endpoint**: `https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1`
- **Draw cards endpoint**: `https://deckofcardsapi.com/api/deck/<<deck_id>>/draw/?count=N`

### How It Works

1. Program shuffles a new deck using the API and receives a `deck_id`
2. Uses the `deck_id` to draw the required number of cards (5 × number of players)
3. Splits cards into hands for each player
4. Evaluates each hand for poker-style rankings
5. Compares all hands and announces the winner(s)

### Troubleshooting

#### SSL Certificate Error on macOS

If you encounter this error when running the script:

```
Error shuffling deck: URL error while accessing https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1: 
<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)>
```

**Cause**: Python 3.x on macOS doesn't use the system's certificate store by default, causing SSL verification to fail for HTTPS requests.

**Solution**: Install the SSL certificates for Python by running this command in your terminal:

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

Replace `3.13` with your Python version if different (e.g., `3.12`, `3.11`, `3.10`).

After installing certificates, the script should work without any SSL errors.

#### Other Network Errors

If you encounter other network errors:
- Check your internet connection
- The Deck of Cards API may be temporarily unavailable
- Try running the program again after a few moments

## Assignment 3: CSO dataset retrieval

A Python program that retrieves the dataset for the "exchequer account (historical series)" from the CSO, and stores it into a file called "cso.json".

### How to Run
```bash
python3 assignment3-cso.py
```

## Assignment 4: GitHub Text Replacer

A Python program that reads a README from a GitHub repository, replaces whole words, and pushes the changes back.

### Configuration

Edit the dictionaries in your `config.py` file:

```python
api_keys = {
    'github_aprivateone': 'your_github_token_here'
}

assignment04_github_config = {
    'repo_owner': 'your-username',
    'repo_name': 'your-repo',
    'file_path': 'README.md',
    'old_text': 'OldWord',
    'new_text': 'NewWord',
    'encoding': 'utf-8'
}
```

### How to Run

```bash
python3 assignment04-github.py
```