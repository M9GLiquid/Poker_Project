from collections import Counter
from ClientBase import Card, BettingAnswer as ACTION
import PokerHand

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Memory'
CURRENT_HAND = []

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

        # Memory for tracking opponents
        self.opponentActions = {}  # Track actions for each opponent
        self.showdownHands = {}   # Track hands revealed at showdown
        self.cardsThrown = {}   # Track card exchanges

# Get the player's name, default to POKER_CLIENT_NAME if none is provided
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

# Initialize the Memory Agent
agent = pokerGames()

# Handle the start of a new round
def queryOpenAction(
        _minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")
    opponentStrategies = {
        opponent: PokerHand.deduceOpponentStrategy(agent.opponentActions.get(opponent, []),
                                                   agent.showdownHands.get(opponent, []))
        for opponent in agent.opponentActions
    }

    # Calculate how much more is required to meet the minimum pot
    additionalBetRequired = _minimumPotAfterOpen - _playersCurrentBet

    # Ensure the agent can afford the bet
    if additionalBetRequired > _playersRemainingChips:
        print(
            f"Insufficient chips to open: Needed {_minimumPotAfterOpen}, "
            f"Available {_playersRemainingChips}. Checking instead."
        )
        return ACTION.ACTION_CHECK

    # Adjust based on chip levels
    if _playersRemainingChips < _minimumPotAfterOpen * 2:
        print("Low chip count: Playing conservatively.")
        return ACTION.ACTION_CHECK
    elif _playersRemainingChips > _minimumPotAfterOpen * 5:
        print("High chip count: Playing aggressively.")
        return ACTION.ACTION_OPEN

    # Weight-based decision system
    strategy_weights = {
        PokerHand.OpponentStrategy.AGGRESSIVE: -2,
        PokerHand.OpponentStrategy.PASSIVE: 3,
        PokerHand.OpponentStrategy.BLUFFER: 1,
        PokerHand.OpponentStrategy.RISK_TAKER: -1,
        PokerHand.OpponentStrategy.SHOWDOWN_ORIENTED: 2,
        PokerHand.OpponentStrategy.CONSERVATIVE: 1
    }

    total_weight = sum(
        strategy_weights[strategy] * list(opponentStrategies.values()).count(strategy)
        for strategy in strategy_weights
    )

    print(f"Total strategy weight: {total_weight}")

    # Adjust behavior based on weighted strategies
    if total_weight > 0:
        print("Positive weight: Playing aggressively.")
        return ACTION.ACTION_OPEN

    print("Negative weight: Playing conservatively.")
    return ACTION.ACTION_CHECK

# Decide the call/raise action
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    opponentStrategies = {opponent: PokerHand.deduceOpponentStrategy(opponent) for opponent in agent.opponentActions}

    # Adjust behavior based on opponents
    if PokerHand.OpponentStrategy.BLUFFER in opponentStrategies.values():
        print("Opponent identified as a bluffer: Calling more frequently.")
        return ACTION.ACTION_CALL
    if PokerHand.OpponentStrategy.CONSERVATIVE in opponentStrategies.values():
        print("Opponent identified as conservative: Avoiding unnecessary raises.")
        return ACTION.ACTION_CHECK

    # Default behavior
    return ACTION.ACTION_RAISE
    

# Decide which cards to throw
def queryCardsToThrow(_hand):
    print("Memory Agent: Deciding which cards to throw.")
    handStrength = PokerHand.evaluate(_hand)
    # Memory Agent: Discard Action

    # Extract ranks and suits from the hand
    ranks = [card.rank for card in _hand]
    suits = [card.suit for card in _hand]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    # Decide based on specific hand rankings
    if handStrength == PokerHand.ONE_PAIR:
        # Keep the pair and discard other cards
        pairRank = [rank for rank, count in rank_counts.items() if count == 2][0]
        return ' '.join(str(card) for card in _hand if card.rank != pairRank)

    elif handStrength == PokerHand.TWO_PAIR:
        # Keep both pairs and discard the fifth card
        pairRanks = [rank for rank, count in rank_counts.items() if count == 2]
        return ' '.join(str(card) for card in _hand if card.rank not in pairRanks)

    elif handStrength == PokerHand.THREE_OF_A_KIND:
        # Keep the three of a kind and discard the other two cards
        tripletRank = [rank for rank, count in rank_counts.items() if count == 3][0]
        return ' '.join(str(card) for card in _hand if card.rank != tripletRank)

    elif handStrength == PokerHand.STRAIGHT or \
            handStrength == PokerHand.STRAIGHT_FLUSH or \
            handStrength == PokerHand.FLUSH or \
            handStrength == PokerHand.FULL_HOUSE or \
            handStrength == PokerHand.FOUR_OF_A_KIND:
        # Keep all cards; these hands are already strong and cannot be improved.
        return ''

    elif handStrength == PokerHand.HIGH_CARD:
        # Discard all cards below Jack unless they are part of a flush draw or straight draw
        flushSuit = max(suit_counts, key=suit_counts.get) if max(suit_counts.values()) >= 4 else None
        straightDrawRanks = [rank for rank in ranks if any(rank + i in ranks for i in range(-3, 4))]

        return ' '.join(
            str(card)
            for card in _hand
            if (card.rank < Card.JACK and
                (flushSuit is None or card.suit != flushSuit) and
                card.rank not in straightDrawRanks)
        )

    # Default: Keep all cards if the hand is strong or cannot be improved
    return ''
