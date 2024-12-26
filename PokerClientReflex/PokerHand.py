from enum import Enum
from collections import Counter
from ClientBase import Card

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

  def __init__(self, hand_name, probability):
    self.hand_name = hand_name
    self.probability = probability


  def __str__(self):
    return f"{self.hand_name}: {self.probability}%"
  
  def evaluate(hand):
    # Extract ranks and suits from the hand
    ranks = [card.rank for card in hand]
    suits = [card.suit for card in hand]

    # Count occurrences of each rank and suit
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    # Check for flush (all cards of the same suit)
    is_flush = len(suit_counts) == 1

    # Check for straight (consecutive ranks)
    sorted_ranks = sorted(ranks)
    is_straight = all(
        sorted_ranks[i] + 1 == sorted_ranks[i + 1] for i in range(len(sorted_ranks) - 1)
    )
    # Handle the special case of A-2-3-4-5 straight
    is_low_straight = set(ranks) == {Card.ACE, Card.TWO, Card.THREE, Card.FOUR, Card.FIVE}

    # Check for specific hand rankings
    if is_flush and (is_straight or is_low_straight):
        return PokerHand.STRAIGHT_FLUSH
    if 4 in rank_counts.values():
        return PokerHand.FOUR_OF_A_KIND
    if sorted(rank_counts.values()) == [2, 3]:
        return PokerHand.FULL_HOUSE
    if is_flush:
        return PokerHand.FLUSH
    if is_straight or is_low_straight:
        return PokerHand.STRAIGHT
    if 3 in rank_counts.values():
        return PokerHand.THREE_OF_A_KIND
    if list(rank_counts.values()).count(2) == 2:
        return PokerHand.TWO_PAIR
    if 2 in rank_counts.values():
        return PokerHand.ONE_PAIR

    # Default to high card
    return PokerHand.HIGH_CARD

# Example Usage
for hand in PokerHand:
  print(hand)
