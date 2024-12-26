import random
import ClientBase
from itertools import combinations
from PokerHand import PokerHand



# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Reflex'
CURRENT_HAND = []

playerAllIn = False

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0



# Get the player's name, default to POKER_CLIENT_NAME if none is provided
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

def evaluate(hand_):
    pass

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

    # Step 1: Assess hand strength and retrieve probability
    hand_type = evaluate(CURRENT_HAND)  # Returns a string like "Straight", "Flush", etc.

    # Find the probability for the hand type
    hand_probability = next(
        (hand.probability for hand in PokerHand if hand.hand_name == hand_type),
        None  # Default to None if no match is found
    )

    # Raise an error if hand type is invalid
    if hand_probability is None:
        raise ValueError(f"Invalid hand type returned by evaluateHandStrength: {hand_type}")

    # Step 2: Reflex decision rules based on hand probability
    if hand_probability > 40:  # Weak hand (High Card, One Pair)
        print(f"Hand is weak ({hand_type}). Choosing to CHECK.")
        return ClientBase.BettingAnswer.ACTION_CHECK

    if 5 < hand_probability <= 40:  # Moderate hand (Two Pair, Three of a Kind)
        print(f"Hand is moderate ({hand_type}). Opening with minimum bet.")
        return ClientBase.BettingAnswer.ACTION_OPEN, max(_minimumPotAfterOpen, _playersCurrentBet + 10)

    if 1 <= hand_probability <= 5:  # Strong hand (Straight, Flush)
        print(f"Hand is strong ({hand_type}). Opening with aggressive bet.")
        return ClientBase.BettingAnswer.ACTION_OPEN, min(_playersRemainingChips, _minimumPotAfterOpen * 2)

    if hand_probability < 1:  # Very strong hand (Full House, Four of a Kind, Straight Flush)
        print(f"Hand is very strong ({hand_type}). Going ALL-IN.")
        return ClientBase.BettingAnswer.ACTION_ALLIN

    # Default fallback (this should rarely execute)
    print("Default fallback triggered. Choosing to CHECK.")
    return ClientBase.BettingAnswer.ACTION_CHECK

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
    """
    Decide the agent's action during the call/raise phase based on detailed hand strength and probabilities.
    """
    print("Player requested to choose a call/raise action.")

    # Step 1: Assess hand strength and retrieve probability
    hand_type = evaluate(CURRENT_HAND)  # Returns a string like "Straight", "Flush", etc.

    # Find the probability for the hand type
    hand_probability = next(
        (hand.probability for hand in PokerHand if hand.hand_name == hand_type),
        None  # Default to None if no match is found
    )

    # Raise an error if hand type is invalid
    if hand_probability is None:
        raise ValueError(f"Invalid hand type returned by evaluateHandStrength: {hand_type}")

    # Step 2: Reflex decision rules based on detailed hand type
    if hand_type == "High Card" or hand_type == "One Pair":
        # Weak hands
        print(f"Hand is weak ({hand_type}). Choosing to FOLD.")
        return ClientBase.BettingAnswer.ACTION_FOLD

    elif hand_type == "Two Pair" or hand_type == "Three of a Kind":
        # Moderate hands
        if playerAllIn:
            return ClientBase.BettingAnswer.ACTION_FOLD
        else:
            print(f"Hand is moderate ({hand_type}). Choosing to CALL.")
            if _playersCurrentBet + _playersRemainingChips >= _maximumBet:
                return ClientBase.BettingAnswer.ACTION_CALL
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD

    elif hand_type == "Straight" or hand_type == "Flush":
        # Strong hands
        print(f"Hand is strong ({hand_type}). Choosing to RAISE.")
        raise_amount = min(_playersCurrentBet + 10, _playersRemainingChips, _maximumBet + _minimumAmountToRaiseTo)
        if raise_amount > _minimumAmountToRaiseTo:
            return ClientBase.BettingAnswer.ACTION_RAISE, raise_amount
        else:
            return ClientBase.BettingAnswer.ACTION_CALL

    elif hand_type == "Full House" or hand_type == "Four of a Kind":
        # Very strong hands
        print(f"Hand is very strong ({hand_type}). Choosing to RAISE aggressively.")
        raise_amount = min(_playersRemainingChips, _maximumBet + _minimumAmountToRaiseTo * 2)
        return ClientBase.BettingAnswer.ACTION_RAISE, raise_amount

    elif hand_type == "Straight Flush":
        # Extremely strong hand
        print(f"Hand is extremely strong ({hand_type}). Going ALL-IN.")
        return ClientBase.BettingAnswer.ACTION_ALLIN

    # Default fallback (this should rarely execute)
    print("Default fallback triggered. Choosing to FOLD.")
    return ClientBase.BettingAnswer.ACTION_FOLD


'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)
    return _hand[random.randint(0,4)] + ' '

# InfoFunction:

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
    print("Player "+_playerName +" called.")

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
    if _playerName != "Reflex":
        playerAllIn = True
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
