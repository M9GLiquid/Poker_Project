from Client import agent

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
    if _playerName != agent.PlayerName:
        agent.opponentActions.setdefault(_playerName, []).append({
            'action': 'Chips', 
            'amount': int(_chips)
        })

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
    agent.opponentActions.setdefault(_playerName, []).append({
        'action': 'Check'
    })

# Print player raise action information
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo + " chips.")
    agent.opponentActions.setdefault(_playerName, []).append({
        'action': 'Raise', 
        'amount': int(_amountRaisedTo)
    })

# Print player call action information
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

# Print player fold action information
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")
    agent.opponentActions.setdefault(_playerName, []).append({
        'action': 'Fold'
    })

# Print player all-in action information
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")
    agent.opponentActions.setdefault(_playerName, []).append({
        'action': 'All-in', 
        'amount': int(_allInChipCount)
    })

# Print player card exchange information
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

# Print clients hand information during showdown
def infoPlayerHand(_playerName, _hand):
    agent.CurrentHand = _hand
    print("Player "+ _playerName +" hand " + str(_hand))

# Print undisputed win information during showdown
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

# Print round result information
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")
