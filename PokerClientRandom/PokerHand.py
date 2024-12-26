from enum import Enum
from collections import Counter

class PokerHand(Enum):
    STRAIGHT_FLUSH = ("Straight Flush", 0.0015)
    FOUR_OF_A_KIND = ("Four of a Kind", 0.024)
    FULL_HOUSE = ("Full House", 0.14)
    FLUSH = ("Flush", 0.20)
    STRAIGHT = ("Straight", 0.39)
    THREE_OF_A_KIND = ("Three of a Kind", 2.11)
    TWO_PAIR = ("Two Pair", 4.75)
    ONE_PAIR = ("One Pair", 42.26)
    HIGH_CARD = ("High Card", 50.12)

    def __init__(self, name, probability):
        self.name = name
        self.probability = probability

    def __str__(self):
        return f"{self.name}: {self.probability}%"

    @staticmethod
    def identify_hand(hand):

        # Extract ranks and suits
        ranks = [card[0] for card in hand]
        suits = [card[1] for card in hand]

        # Count occurrences of ranks and suits
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        # Sort ranks for easier straight detection
        sorted_ranks = sorted(ranks)

        # Check for flush (all cards have the same suit)
        is_flush = len(suit_counts) == 1

        # Check for straight (ranks are consecutive)
        is_straight = len(rank_counts) == 5 and (sorted_ranks[-1] - sorted_ranks[0] == 4)

        # Handle Ace-low straight (e.g., A, 2, 3, 4, 5)
        if sorted_ranks == [0, 1, 2, 3, 12]:  # Special case for Ace-low
            is_straight = True
            sorted_ranks = [0, 1, 2, 3, 4]  # Normalize to lowest rank for consistency

        # Determine the hand type
        if is_straight and is_flush:
            return PokerHand.STRAIGHT_FLUSH
        elif 4 in rank_counts.values():
            return PokerHand.FOUR_OF_A_KIND
        elif 3 in rank_counts.values() and 2 in rank_counts.values():
            return PokerHand.FULL_HOUSE
        elif is_flush:
            return PokerHand.FLUSH
        elif is_straight:
            return PokerHand.STRAIGHT
        elif 3 in rank_counts.values():
            return PokerHand.THREE_OF_A_KIND
        elif list(rank_counts.values()).count(2) == 2:
            return PokerHand.TWO_PAIR
        elif 2 in rank_counts.values():
            return PokerHand.ONE_PAIR
        else:
            return PokerHand.HIGH_CARD
