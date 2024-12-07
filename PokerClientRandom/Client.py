import random
import ClientBase

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

# Get the player's name, default to POKER_CLIENT_NAME if none is provided
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

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
            return ClientBase.BettingAnswer.ACTION_OPEN,  \
                    (random.randint(0, 10) + _minimumPotAfterOpen) if \
                        _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else \
                        _minimumPotAfterOpen
        else:
            return ClientBase.BettingAnswer.ACTION_CHECK

    return {
        0: ClientBase.BettingAnswer.ACTION_CHECK,
        1: ClientBase.BettingAnswer.ACTION_CHECK,
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
            return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return ClientBase.BettingAnswer.ACTION_FOLD
    return {
        0: ClientBase.BettingAnswer.ACTION_FOLD,
        #1: ClientBase.BettingAnswer.ACTION_ALLIN,
        1: ClientBase.BettingAnswer.ACTION_FOLD,
        2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
    }.get(random.randint(0, 3), chooseRaiseOrFold())

# Decide which cards to discard during the draw phase
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)
    return _hand[random.randint(0,4)] + ' '

# InfoFunction:

# Print round start information
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

# Print game over message
def infoGameOver():
    print('The game is over.')

# Print the chips information for a player
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

# Print ante change information
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

# Print forced bet information for a player
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")

# Print player open action information
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

# Print player check action information
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

# Print player raise action information
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

# Print player call action information
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

# Print player fold action information
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

# Print player all-in action information
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

# Print player card exchange information
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

# Print player hand information during showdown
def infoPlayerHand(_playerName, _hand):
    print("Player "+ _playerName +" hand " + str(_hand))

# Print undisputed win information during showdown
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

# Print round result information
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")
