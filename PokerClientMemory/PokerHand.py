from collections import Counter
from ClientBase import Card, BettingAnswer as ACTION

from enum import Enum

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
    self.hand_name = name
    self.probability = probability

  def __str__(self):
    return f"{self.name}: {self.probability}%"

class OpponentStrategy(Enum):
    CONSERVATIVE = "Conservative"
    AGGRESSIVE = "Aggressive"
    BLUFFER = "Bluffer"
    RISK_TAKER = "Risk-Taker"
    PASSIVE = "Passive"
    NON_ADAPTABLE = "Non-Adaptable"
    OPPORTUNISTIC = "Opportunistic"
    SHOWDOWN_ORIENTED = "Showdown-Oriented"
    CAUTIOUS_CALLER = "Cautious Caller"
    BALANCED = "Balanced"
    UNKNOWN = "Unknown"

# Evaluate a poker hand
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

def deduceOpponentStrategy(opponentActions, showdownHands):
    actions = opponentActions

    if not actions:
        return OpponentStrategy.UNKNOWN

    totalActions = len(actions)
    foldCount = sum(1 for action in actions if action['action'] == ACTION.FOLD)
    betCount = sum(1 for action in actions if action['action'] == 'Bet')
    raiseCount = sum(1 for action in actions if action['action'] == 'Raise')
    checkCount = sum(1 for action in actions if action['action'] == 'Check')
    callCount = sum(1 for action in actions if action['action'] == 'Call')
    cardExchangeCount = sum(1 for action in actions if action.get('cardExchange', 0) > 0)
    showdownCount = len(showdownHands)

    # Deduce strategy based on the patterns of actions
    if foldCount / totalActions > 0.5:
        return OpponentStrategy.CONSERVATIVE
    elif raiseCount / totalActions > 0.4:
        return OpponentStrategy.AGGRESSIVE
    elif betCount > raiseCount and checkCount > callCount:
        return OpponentStrategy.PASSIVE
    elif showdownCount > 0 and all(hand == PokerHand.HIGH_CARD for hand in showdownHands):
        return OpponentStrategy.BLUFFER
    elif betCount > 0 and foldCount == 0:
        return OpponentStrategy.RISK_TAKER
    elif cardExchangeCount == 0 and totalActions > 0:
        return OpponentStrategy.NON_ADAPTABLE
    elif all(action['action'] == 'Raise' for action in actions if action['action'] == 'Raise') and checkCount > 0:
        return OpponentStrategy.OPPORTUNISTIC
    elif showdownCount == totalActions:
        return OpponentStrategy.SHOWDOWN_ORIENTED
    elif betCount > 0 and raiseCount == 0 and callCount / totalActions > 0.6:
        return OpponentStrategy.CAUTIOUS_CALLER

    return OpponentStrategy.BALANCED
