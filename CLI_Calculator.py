katiPoint = int(input("How much Point game: "))
noOfPlayers = int(input("Enter no of players: "))
playersName = []

playersMaal = []
totalMaal = 0

seenPlayers = []
unseenPlayers = []

for i in range(noOfPlayers):
    player = input(f"player {i+1} name : ")
    playersName.append(player)

print(playersName)

isRunning = True

while isRunning:
    print("seen status: Y/N")
    for p in playersName:
        seenStatus = input(f"{p}: ")
        if seenStatus == 'y' or seenStatus == 'Y':
            seenPlayers.append(p)
        elif seenStatus == 'n' or seenStatus == 'N':
            unseenPlayers.append(p)

    print("Enter Maal: ")
    for i in playersName:
        for j in seenPlayers:
            if i == j:
                maal = int(input(f"{i}: "))
                playersMaal.append(maal)
        for k in unseenPlayers:
            if i == k:
                maal = 0
                playersMaal.append(maal)

    player_maal_zip = zip(playersName, playersMaal)
    player_maal_dict = dict(player_maal_zip)
    print(player_maal_dict)

    totalMaal = sum(player_maal_dict.values())
    print(f"Total Maal: {totalMaal}")

    winner = input(f" Select winner : \n {playersName}")

    seenPlayerCount = len(seenPlayers)
    unseenPlayerCount = len(unseenPlayers)

    def handelWinner(winner):
        toPay = 0
        toReceive = 0
        GT = 0
        for player, maal in player_maal_dict.items():
            if player == winner:
                toReceive = noOfPlayers * maal
            toPay = toPay + maal
        GT = toReceive - toPay + (3 * (seenPlayerCount - 1)) + 10 * unseenPlayerCount
        print(f"{winner} = {GT}  --> {GT * katiPoint} ")

    handelWinner(winner)

    def handelSeenPlayers(seenPlayers, winner):
        toPay = 0
        toReceive = 0
        for player, maal in player_maal_dict.items():
            for s in seenPlayers:
                if player == s and player != winner:
                    toReceive = maal * noOfPlayers
                    toPay = (totalMaal + 3)
                    GT = toReceive - toPay
                    print(f"{player} = {GT}  --> {GT * katiPoint} ")

    handelSeenPlayers(seenPlayers, winner)

    def handelunseenPlayers(unseenPlayers):
        toPay = 0
        toReceive = 0
        for player in player_maal_dict.keys():
            for s in unseenPlayers:
                if player == s:
                    toReceive = 0
                    toPay = (totalMaal + 10)
                    GT = toReceive - toPay
                    print(f"{player} = {GT}  --> {GT * katiPoint} ")

    handelunseenPlayers(unseenPlayers)

    option = int(input("Exit (0) | Start Again (1) "))

    if option == 1:
        playersMaal = []
        totalMaal = 0
        seenPlayers = []
        unseenPlayers = []
    elif option == 0:
        isRunning = False
        
        
