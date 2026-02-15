# Assignment 2: Card Draw - Draw 5 cards for each player and evaluate the hand
# Author: Carmine Giardino

#!/usr/bin/env python3
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import argparse
from collections import Counter

SHUFFLE_URL = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
DRAW_URL_TEMPLATE = "https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}"

VALUE_MAP = {
    'ACE': 14,
    'KING': 13,
    'QUEEN': 12,
    'JACK': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

RANK_NAMES = {
    7: 'Straight flush',
    6: 'Flush (all same suit)',
    5: 'Straight',
    4: 'Three of a kind (Triple)',
    3: 'Two pairs',
    2: 'Pair',
    1: 'High card',
}


def fetch_json(url, timeout=10):
    """Fetch JSON from the given URL and return a parsed object. Raises RuntimeError on failure."""
    try:
        req = Request(url, headers={"User-Agent": "card-draw-script/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8"))
    except HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code} while accessing {url}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"URL error while accessing {url}: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while accessing {url}: {e}")


def shuffle_deck():
    """Shuffle a new deck and return the deck_id."""
    data = fetch_json(SHUFFLE_URL)
    deck_id = data.get("deck_id")
    if not deck_id:
        raise RuntimeError("Failed to obtain deck_id from shuffle response")
    return deck_id


def draw_cards(deck_id, count=5):
    """Draw count cards from the given deck_id and return a list of cards."""
    url = DRAW_URL_TEMPLATE.format(deck_id=deck_id, count=count)
    data = fetch_json(url)
    if not data.get("success", False):
        raise RuntimeError("API reported failure when drawing cards")
    cards = data.get("cards")
    if cards is None:
        raise RuntimeError("No cards in draw response")
    return cards


def hand_value_counts(cards):
    """Given a list of card dicts, return (values, suits, val_counts, suit_counts)"""
    values = [VALUE_MAP.get(c.get('value'), 0) for c in cards]
    suits = [c.get('suit') for c in cards]
    # Count values and suits
    val_counts = Counter(values)
    suit_counts = Counter(suits)
    return values, suits, val_counts, suit_counts


def is_straight(values):
    """Return (True, high_value) if the given values form a straight, else (False, None)."""
    # values: list of ints (may contain duplicates)
    unique_values = sorted(set(values))
    if len(unique_values) != 5:
        return False, None
    # normal straight
    max_value = max(unique_values)
    min_value = min(unique_values)
    if max_value - min_value == 4:
        return True, max_value
    # wheel straight A-2-3-4-5 -> values [2,3,4,5,14]
    if set(unique_values) == {14, 2, 3, 4, 5}:
        return True, 5
    return False, None


def evaluate_hand(cards):
    """Return (rank_priority, tiebreaker_list, rank_name, details)
    Higher rank_priority is better. Tiebreaker_list is compared lexicographically.
    Details contain info like which value formed the pair/triple.
    """
    values, suits, val_counts, suit_counts = hand_value_counts(cards)
    # Sort values descending for high-card comparisons
    sorted_vals_desc = sorted(values, reverse=True)

    # Check straight first
    straight, straight_high = is_straight(values)
    
    # If straight, check for a flush to determine if it's a straight flush
    if straight:
        is_flush = (len(suit_counts) == 1)
        if is_flush:
            # Straight flush
            return 7, [straight_high], RANK_NAMES[7], {'straight_high': straight_high}
        else:
            # Just straight
            return 5, [straight_high], RANK_NAMES[5], {'straight_high': straight_high}
    
    # Check flush (only if not straight)
    is_flush = (len(suit_counts) == 1)
    if is_flush:
        return 6, sorted_vals_desc, RANK_NAMES[6], {}

    # Three of a kind (triple)
    for val, cnt in val_counts.items():
        if cnt == 3:
            # tiebreaker: triple value, then remaining kicker(s)
            kickers = sorted([v for v in values if v != val], reverse=True)
            return 4, [val] + kickers, RANK_NAMES[4], {'triple': val}

    # Pair (or two pairs)
    pair_vals = [val for val, cnt in val_counts.items() if cnt == 2]
    if pair_vals:
        if len(pair_vals) == 2:
            # Two pairs
            sorted_pairs = sorted(pair_vals, reverse=True)
            # Tiebreaker: high pair, low pair, then kicker
            kickers = sorted([v for v in values if v not in pair_vals], reverse=True)
            return 3, sorted_pairs + kickers, RANK_NAMES[3], {'pairs': sorted_pairs}
        else:
            # Single pair
            primary_pair = pair_vals[0]
            kickers = sorted([v for v in values if v != primary_pair], reverse=True)
            return 2, [primary_pair] + kickers, RANK_NAMES[2], {'pair': primary_pair}

    # High card
    return 1, sorted_vals_desc, RANK_NAMES[1], {}


def describe_cards(cards):
    return ', '.join([f"{c.get('value')} of {c.get('suit')}" for c in cards])


def compare_hands(eval_a, eval_b):
    """Compare two evaluated hands (rank_priority, tiebreaker_list, ...).
    Return 1 if a wins, -1 if b wins, 0 for tie.
    """
    rank_a, tie_a = eval_a[0], eval_a[1]
    rank_b, tie_b = eval_b[0], eval_b[1]
    if rank_a > rank_b:
        return 1
    if rank_a < rank_b:
        return -1
    # same rank: compare tiebreaker lists lexicographically
    if tie_a > tie_b:
        return 1
    if tie_a < tie_b:
        return -1
    return 0


def congratulate(rank_priority):
    """Return a congratulatory message for the given rank_priority, or None."""
    if rank_priority == 7:
        return "Amazing! Straight flush! Congratulations!"
    if rank_priority == 6:
        return "Excellent! All cards are the same suit — a flush. Congratulations!"
    if rank_priority == 5:
        return "Great! That's a straight. Congratulations!"
    if rank_priority == 4:
        return "Great! You have three of a kind (a triple). Congratulations!"
    if rank_priority == 3:
        return "Nice! You have two pair. Congratulations!"
    if rank_priority == 2:
        return "Good job! You have a pair. Congratulations!"
    return None


def main():
    parser = argparse.ArgumentParser(description='Deal cards using Deck of Cards API')
    parser.add_argument('-p', '--players', type=int, default=1, help='Number of players (1-10).')
    args = parser.parse_args()

    cards_per_player = 5
    
    # Validate player count and explain the limit
    if args.players > 10:
        print(f"Warning: Requested {args.players} players, but limiting to 10 players.")
        print(f"Reason: A standard deck has 52 cards. With {cards_per_player} cards per player,")
        print(f"the maximum is 10 players (10 × {cards_per_player} = 50 cards, leaving 2 cards in deck).")
        print()
    
    players = max(1, min(10, args.players))  # clamp to 1..10 (52 cards / 5 = 10 max)
    total_cards = players * cards_per_player

    try:
        deck_id = shuffle_deck()
    except RuntimeError as e:
        print(f"Error shuffling deck: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        cards = draw_cards(deck_id, count=total_cards)
    except RuntimeError as e:
        print(f"Error drawing cards: {e}", file=sys.stderr)
        sys.exit(1)

    if len(cards) < total_cards:
        print(f"Warning: requested {total_cards} cards but only received {len(cards)}")

    # Split cards into hands
    hands = [cards[i * cards_per_player:(i + 1) * cards_per_player] for i in range(players)]

    evaluations = []
    for idx, hand in enumerate(hands, start=1):
        print(f"\nPlayer {idx} hand: {describe_cards(hand)}")
        ev = evaluate_hand(hand)
        evaluations.append(ev)
        rank_name = ev[2]
        print(f"Player {idx} result: {rank_name}")
        congratulation_message = congratulate(ev[0])
        if congratulation_message:
            print(congratulation_message)

    if players >= 2:
        # Find the winner(s) by comparing all hands
        best_eval = evaluations[0]
        winners = [1]  # player indices (1-based)
        
        for idx in range(1, len(evaluations)):
            cmp = compare_hands(evaluations[idx], best_eval)
            if cmp == 1:
                # This player beats the current best
                best_eval = evaluations[idx]
                winners = [idx + 1]
            elif cmp == 0:
                # Tie with current best
                winners.append(idx + 1)
        
        winning_hand_name = best_eval[2]  # rank_name from evaluation
        if len(winners) == 1:
            print(f"\nPlayer {winners[0]} wins with {winning_hand_name}!")
        else:
            winners_str = ", ".join([f"Player {w}" for w in winners])
            print(f"\nIt's a tie between {winners_str} with {winning_hand_name}!")


if __name__ == "__main__":
    main()
