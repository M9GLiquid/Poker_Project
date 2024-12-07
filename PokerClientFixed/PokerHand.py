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
    self.name = name
    self.probability = probability

  def __str__(self):
    return f"{self.name}: {self.probability}%"

# Example Usage
for hand in PokerHand:
  print(hand)
