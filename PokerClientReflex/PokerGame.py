import socket

from Client import *

iMsg = 0
SIGNAL_ALIVE = ''#'==================ALIVE======================'
SIGNAL_START = '\n================== Round Start =============='
SIGNAL_END = '******************* Round End ****************\n'

CURRENT_HAND = []  # Stores the current hand of the agent

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

infoAgent = pokerGames()
MsgFractions = []

GAME_ON = True

while GAME_ON:

    try:
        # Receive data from the server and split into message fragments
        data = s.recv(BUFFER_SIZE)
        message = data.split()

        for fraction in message:
            MsgFractions.append(fraction)

        # Process each message fragment
        while len(MsgFractions):

            if len(MsgFractions) == 0: # Skip empty messages
                continue

            iMsg = iMsg + 1 # Increment message count

            RequestType = MsgFractions.pop(0).decode('ascii') # Decode and retrieve request type

            if RequestType == 'Name?':  # Server requests the player's name
                s.send(('Name ' + queryPlayerName(POKER_CLIENT_NAME) + "\n").encode())

            elif RequestType == 'Chips':  # Server informs about the player's chip count
                name = MsgFractions.pop(0).decode('ascii')
                if name == POKER_CLIENT_NAME:
                    chips = MsgFractions.pop(0).decode('ascii')
                    infoAgent.Chips = int(chips)
                    # SMART start
                    infoPlayerChips(name, chips)
                    # SMART end
                else:
                    infoPlayerChips(name, MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Ante_Changed':  # Server updates the ante amount
                ante = MsgFractions.pop(0).decode('ascii')
                infoAgent.Ante = int(ante)
                infoAnteChanged(ante)

            elif RequestType == 'Forced_Bet':  # Server notifies a forced bet
                name = MsgFractions.pop(0).decode('ascii')
                if name == POKER_CLIENT_NAME:
                    print(SIGNAL_START)
                    infoAgent.playersCurrentBet = infoAgent.playersCurrentBet + int(MsgFractions.pop(0).decode('ascii'))
                else:
                    infoForcedBet(name, MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Open?': # Server requests the player's open action
                minimumPotAfterOpen = int(MsgFractions.pop(0).decode('ascii'))
                playersCurrentBet = int(MsgFractions.pop(0).decode('ascii'))
                playerRemainingChips = int(MsgFractions.pop(0).decode('ascii'))
                tmp = queryOpenAction(minimumPotAfterOpen, playersCurrentBet, playerRemainingChips)
                if isinstance(tmp, str):  # For check and All-in
                    s.send((tmp + "\n").encode())
                elif len(tmp) == 2:  # For open
                    s.send((tmp[0] + ' ' + str(tmp[1]) + " \n").encode())
                print(SIGNAL_ALIVE)
                print(POKER_CLIENT_NAME + 'Action>', tmp)

            elif RequestType == 'Call/Raise?': # Server requests the player's call/raise action
                maximumBet = int(MsgFractions.pop(0).decode('ascii'))
                minimumAmountToRaiseTo = int(MsgFractions.pop(0).decode('ascii'))
                playersCurrentBet = int(MsgFractions.pop(0).decode('ascii'))
                playersRemainingChips = int(MsgFractions.pop(0).decode('ascii'))
                tmp = queryCallRaiseAction(maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips)
                if isinstance(tmp, str):  # For fold, all-in, call
                    s.send((tmp + "\n").encode())
                elif len(tmp) == 2:  # For raise
                    s.send((tmp[0] + ' ' + str(tmp[1]) + " \n").encode())
                print(SIGNAL_ALIVE)
                print(POKER_CLIENT_NAME + 'Action>', tmp)

            elif RequestType == 'Cards':  # Server sends the player's cards
                infoAgent.CurrentHand = []
                for ielem in range(1, 6):  # 1 based indexing is required...
                    infoAgent.CurrentHand.append(MsgFractions.pop(0).decode('ascii'))
                infoPlayerHand(POKER_CLIENT_NAME, infoAgent.CurrentHand)

            elif RequestType == 'Draw?': # Server requests the player's discard action
                discardCards = queryCardsToThrow(infoAgent.CurrentHand)
                s.send(('Throws ' + discardCards + "\n").encode())
                print(POKER_CLIENT_NAME + ' Action>' + 'Throws ' + discardCards)

            elif RequestType == 'Round': # Server starts a new round
                infoNewRound(MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Game_Over': # Server signals the game has ended
                infoGameOver()
                GAME_ON = False

            elif RequestType == 'Player_Open': # Server informs about a player's open action
                infoPlayerOpen(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Check': # Server informs about a player's check action
                infoPlayerCheck(MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Raise': # Server informs about a player's raise action
                infoPlayerRise(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Call': # Server informs about a player's call action
                infoPlayerCall(MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Fold': # Server informs about a player's fold action
                infoPlayerFold(MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_All-in': # Server informs about a player's all-in action
                infoPlayerAllIn(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Draw': # Server informs about a player's card exchange
                infoPlayerDraw(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Round_Win_Undisputed': # Server informs about an undisputed round win
                print(SIGNAL_END)
                infoRoundUndisputedWin(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Round_result':  # Server provides round result details
                print(SIGNAL_END)
                infoRoundResult(MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'))

            elif RequestType == 'Player_Hand': # Server reveals a player's hand
                infoPlayerHand(MsgFractions.pop(0).decode('ascii'),
                               [MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'), MsgFractions.pop(0).decode('ascii'),
                                MsgFractions.pop(0).decode('ascii')])

    except socket.timeout:
        break

s.close()
