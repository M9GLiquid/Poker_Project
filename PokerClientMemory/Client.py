from collections import Counter
import random
import ClientBase
from ClientBase import Card, BettingAnswer
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

# Get the player's name, default to POKER_CLIENT_NAME if none is provided
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

# Initialize the Memory Agent
agent = pokerGames()

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")

    # Choose between open or check based on player state
    def chooseOpenOrCheck():
        if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            return BettingAnswer.ACTION_OPEN,  \
                    (random.randint(0, 10) + _minimumPotAfterOpen) if \
                        _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else \
                        _minimumPotAfterOpen
        else:
            return BettingAnswer.ACTION_CHECK

    return {
        0: BettingAnswer.ACTION_CHECK,
        1: BettingAnswer.ACTION_CHECK,
    }.get(random.randint(0, 2), chooseOpenOrCheck())

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    # Random Open Action
    def chooseRaiseOrFold():
        if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
            return BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return BettingAnswer.ACTION_FOLD
    return {
        0: BettingAnswer.ACTION_FOLD,
        1: BettingAnswer.ACTION_FOLD,
        2: BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else BettingAnswer.ACTION_FOLD
    }.get(random.randint(0, 3), chooseRaiseOrFold())

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Memory Agent: Deciding which cards to throw.")
    handStrength = PokerHand.evaluate(_hand)

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

    elif handStrength == PokerHand.STRAIGHT or handStrength == PokerHand.STRAIGHT_FLUSH:
        # Keep all cards; a straight cannot be improved by discarding
        return ''

    elif handStrength == PokerHand.FLUSH:
        # Keep all cards; a flush cannot be improved by discarding
        return ''

    elif handStrength == PokerHand.FOUR_OF_A_KIND:
        # Keep the four of a kind and discard the fifth card
        quadRank = [rank for rank, count in rank_counts.items() if count == 4][0]
        return ' '.join(str(card) for card in _hand if card.rank != quadRank)

    elif handStrength == PokerHand.FULL_HOUSE:
        # Full houses are already strong; keep all cards
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

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print(f"Player {_playerName} called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")
