import random as random
class Player:
    
    # Initial player settings.
    # All players start the game with 2 coins, and a number assigned to them.
    # All players start the game with two influencers, which are assigned at random at the start of each game.
    # Players have access to the current game instance so that they may refer to the deck and grave (will be viewable at a later point)
    def __init__(self,n,i,j,g):
        self.coins = 2
        self.number = n
        self.influence = [i,j]
        self.game = g
    
    # Does the player have any influence left?
    def isAlive(self):
        return len(self.influence) > 0
    
    # Take 1 coin from the Bank.
    # Cannot be cancelled or challenged.
    def Income(self):
        print("Player " + str(self.number) + " has claimed income.")
        self.coins += 1
    
    # Take 2 coins from the Bank.
    # Can be cancelled by the Duke (Which can be challenged by the player who is taking their turn.) (Not yet implemented)
    # The cancel can be challenged by the player who is currently taking their turn (Not yet implemented)
    def foreignAid(self):
        challenged = False
        print("Player " + str(self.number) + " has claimed foreign aid.")
        self.coins += 2

    # Pay 3 coins to eliminate any other player. 
    # Can be challenged and can be cancelled if the target claims to have a contessa card. (Not yet implemented)
    # The player who is taking their turn can challenge the contessa claim (Not yet implemented)
    def Assassinate(self, player):
        if self.coins >=3: 
            challenged = False
            print("Player " + str(self.number) + " has killed one of Player " + str(player.number) + "'s influences.") 
            self.coins -= 3
            player.influence.pop(0)
        else:
            print("Player " + str(self.number) + " tried to perform an assassination but failed.")
   
   # Take 3 coins from the Bank.
   # Can be challenged by any other player.
    def Duketax(self):
        print("Player " + str(self.number) + " wants to claim Duke Tax.")
        challenged = self.game.callDukeBS(self)
        if not challenged:
            print("Player " + str(self.number) + " has successfully claimed Duke Tax and received 3 coins!")
            self.coins += 3
    
    # Take 2 cards from the deck (1 if the deck only has 1 card) and swap cards into the deck as needed.
    # Can be challenged by any other player.
    def Ambassador(self):
        print("Player " + str(self.number) + " has claimed Ambassador and wishes to draw 2 cards and place 2 cards back into the deck.")
        challenged = self.game.callDukeBS(self)
        if not challenged:
            self.AmbassadorAct()
            print("Player " + str(self.number) + " has drawn 2 cards and placed 2 cards into the deck.")

    # Helper function to engage in the actual card review and replacement into the deck. Deck shuffled after.
    def AmbassadorAct(self):
        draws = 2
        curr = len(self.influence)
        while draws > 0 and len(self.game.deck) > 0:
            self.influence.append(self.game.deck.pop(0))
            draws -= 1
        influencers = "Your current influences are: "
        while curr != len(self.influence):
            for i in self.influence:
                influencers += str(self.influence.index(i)) + ") " + i + ", "
            print(influencers + "please choose " + str(len(self.influence)-curr) + " to return to the deck")
            while True:
                result = raw_input()
                if (result != "1" and result != "0" and result != "2" and result != "3"):
                    print("This does not appear to be a valid response. Please try again")
                    continue
                else:
                    if result == "0":
                        self.game.deck.append(self.influence.pop(0))
                        break
                    elif result == "1":
                        self.game.deck.append(self.influence.pop(1))
                        break
                    elif result == "2":
                        if len(self.influence) < 3:
                            print("You do not have enough cards for this choice!")
                            continue
                        else:
                            self.game.deck.append(self.influence.pop(2))
                            break
                    else:
                        if len(self.influence) < 4:
                            print("You do not have enough cards for this choice!")
                            continue
                        else:
                            self.game.deck.append(self.influence.pop(3))
                            break
        self.game.shuffle()

    # Take two coins from any other player. Can be challenged by any other player.
    # Can be cancelled by a player that claims to have another captain or an ambassador card.
    # The cancellation can also be challenged by the player currently taking their turn.
    def Captain(self,player):
        if player.coins >= 2:
            print("Player " + str(self.number) + " has stolen 2 coins from Player " + str(player.number) + ".")
            challenged = self.game.callCaptainBS(self)
            if not challenged:
                if not player.isAlive:
                    self.coins += 2
                    player.coins -= 2
                    return
                if not self.game.blockCaptain(self,player):
                    return
                else:
                    self.coins += 2
                    player.coins -= 2
        else:
            print("Player " + str(self.number) + " tried to steal coins from Player " + str(player.number) + ", but there were not enough coins.")

    # Pay 7 coins to eliminate the influence of any particular player.
    # This cannot be challenged or cancelled.
    # Players must choose the coup option if they have 10 or more coins at the start of their turn.(Not yet implemented)
    def Coup(self, player):
        if self.coins >= 7:
            print("Player " + str(self.number) + " has staged a coup against one of player " + str(player.number) + "'s influences.")
            self.coins -= 7
            player.influence.pop(player.influence.index(random.choice(player.influence)))
        else:
            print("Player " + str(self.number) + "tried to stage a coup but did not have enough coins.")
class Game:

    # The initial game settings.
    # Deck consists of 3 of each: Assassin, Captain, Duke, Ambassador, and Contessa
    # Potential actions are as follows: Income, Assassinate, Foreign Aid, Duke Tax, Coup, Captain, or Ambassador.
    # Read above for more details on each specific action 
    def __init__(self):
        self.deck = ["Assassin", "Assassin", "Assassin", "Captain", "Captain", "Captain",
        "Duke","Duke","Duke","Ambassador","Ambassador","Ambassador",
        "Contessa","Contessa","Contessa"]
        self.players = []
        self.grave = []
        self.remainingpPlayersstr = []
        self.remainingPlayers = []
        self.Actions = ["Income", "Assassinate", "Foreign Aid", "DukeTax","Coup","Captain", "Ambassador"]

    # Shuffles the deck with an easy call.
    def shuffle(self):
        random.shuffle(self.deck)

    # Offers the opportunity for anyone to challenge the claim of captain. If no challenges, procceed with claim.
    # If challenged, reveal whether or not you have the captain card.
    def callCaptainBS(self,p1):
        self.remainingPlayersstr = []
        self.remainingPlayers = []
        print("Does any player wish to call their bluff? Please input your number below.")
        for i in self.players:
            if i is not p1:
                self.remainingPlayersstr.append(str(i.number))
                self.remainingPlayers.append(i)
                print("Player " + str(i.number))
        print("or 'None'")
        challenged = True
        while True:
            result = raw_input("Your Choice: ")
            if result != "None" and result not in self.remainingPlayersstr:
                print(result + "does not appear to be a valid input. Please try again.")
                continue
            else:
                if result == "None":
                    challenged = False
                    return challenged
                break
        return self.reveal(p1,self.remainingPlayers[self.remainingPlayersstr.index(str(result))],"Captain")
    
    # Provides the player being targeted by the captain to cancel their action by claiming possession of an ambassador or captain card.
    # If the player does not opt to cancel the action, the captain proceeds as intended.
    # If chosen to cancel the action, the captain may then challenge the claim as below.
    def blockCaptain(self,p1,p2):
        print("Does Player " + str(p2.number) + " have either an ambassador or a captain card to block the captain")
        blocked = True
        while True:
            result = raw_input()
            if (result != "y" and result != "yes" and result != "no" and result != "n"):
                print("This does not appear to be a valid response. Please try again")
                continue
            else:
                if result == "n" or result == "no":
                    blocked = False
                    return blocked
                break
        return self.callCaptainBlockBS(p1,p2)

    # The player has claimed to have a Captain or Ambassador. This can be challenged or accepted.
    # If accepted, the captain's original action is nullified.
    # If challenged, the targeted player (p2) must reveal if they have either card, as shown below.
    def callCaptainBlockBS(self, p1,p2):
        print("Player "+ str(p2.number) + " claims to have a Captain or Ambassador, do you wish to call their bluff?")
        while True:
            result = raw_input()
            blocked = True
            if (result != "y" and result != "yes" and result != "no" and result != "n"):
                print("This does not appear to be a valid response. Please try again")
                continue
            else:
                if result == "n" or result == "no":
                    blocked = False
                    return blocked
                break
        return self.revealCaptainCounter(p1,p2)
    
    # The targeted player (p2) must reveal if they have either the Captain or Ambassador card
    # If they do, they then return it to the deck, draw a new card, and the Captain's action is cancelled.
    # If they do not, they lose influence and the captain proceeds with the original action.
    # Because there are two acceptable counters, a separate function was required to ensure that--
    # --influence was not prematurely removed before checking for the other card
    # This probably could've been made more modular by making the original reveal(p1,p2,card) check through a-- 
    # --list of card names instead of just one card, with the majority being a list of length 1
    def revealCaptainCounter(self,p1,p2):
        contains = False
        for card in p2.influence:
            if card == "Captain" or card == "Ambassador":
                correct = card
                contains = True
        if contains:
            self.grave.append(p2.influence.pop(p2.influence.index(random.choice(p2.influence))))
            if len(p2.influence) == 0:
                self.players.pop(self.players.index(p2))
            self.deck.append(p1.influence.pop(p1.influence.index(correct)))
            self.shuffle()
            p1.influence.append(self.deck.pop(0))
            print("Player " + str(p1.number) + " has revealed that they indeed have the " + card +". They have shuffled, and drawn a new card from the deck while Player " + str(p2.number) + " must lose an influencer.")
            return False
        else:
            self.grave.append(p1.influence.pop(p1.influence.index(random.choice(p1.influence))))
            if len(p1.influence) == 0:
                self.players.pop(self.players.index(p1))
            print("Player " + str(p1.number) + " was caught in a lie, and has lost an influencer.")
            return True

    # Players may decide whether or not they want to challenge the Duke's action.
    # If players decide to challenge, the self-proclaimed Duke must go through the regular reveal process.
    # If not challenged, the Duke proceeds.
    def callDukeBS(self,p1):
        self.remainingPlayersstr = []
        self.remainingPlayers = []
        print("Does any player wish to call their bluff? Please input your number below.")
        for i in self.players:
            if i is not p1:
                self.remainingPlayersstr.append(str(i.number))
                self.remainingPlayers.append(i)
                print("Player " + str(i.number))
        print("or 'None'")
        challenged = True
        while True:
            result = raw_input("Your Choice: ")
            if result != "None" and result not in self.remainingPlayersstr:
                print(result + "does not appear to be a valid input. Please try again.")
                continue
            else:
                if result == "None":
                    challenged = False
                    return challenged
                break
        return self.reveal(p1,self.remainingPlayers[self.remainingPlayersstr.index(str(result))],"Duke")

    # Players may decide whether or not they want to challenge the Ambassador's action.
    # If players decide to challenge, the self-proclaimed Duke must go through the regular reveal process.
    # If not challenged, the Ambassador proceeds.
    def callAmbassadorBS(self,p1):
        self.remainingPlayersstr = []
        self.remainingPlayers = []
        print("Does any player wish to call their bluff? Please input your number below.")
        for i in self.players:
            if i is not p1:
                self.remainingPlayersstr.append(str(i.number))
                self.remainingPlayers.append(i)
                print("Player " + str(i.number))
        print("or 'None'")
        challenged = True
        while True:
            result = raw_input("Your Choice: ")
            if result != "None" and result not in self.remainingPlayersstr:
                print(result + "does not appear to be a valid input. Please try again.")
                continue
            else:
                if result == "None":
                    challenged = False
                    return challenged
                break
        return self.reveal(p1,self.remainingPlayers[self.remainingPlayersstr.index(str(result))],"Ambassador")
   
   # The process by which a player reveals whether or not they have the card they're being challenged on.
   # If the player has the card, they must put it in the deck, shuffle, and redraw. The challenging player will lose influence (automated randomly as of now).
   # If the player does not have the card, they must choose an influencer to lose (automated randomly as of now).
    def reveal(self, p1, p2,card):
        if card in p1.influence:
            self.grave.append(p2.influence.pop(p2.influence.index(random.choice(p2.influence))))
            if len(p2.influence) == 0:
                self.players.pop(self.players.index(p2))
            self.deck.append(p1.influence.pop(p1.influence.index(card)))
            self.shuffle()
            p1.influence.append(self.deck.pop(0))
            print("Player " + str(p1.number) + " has revealed that they indeed have the " + card +". They have shuffled, and drawn a new card from the deck while Player " + str(p2.number) + " must lose an influencer.")
            return False
        else:
            self.grave.append(p1.influence.pop(p1.influence.index(random.choice(p1.influence))))
            if len(p1.influence) == 0:
                self.players.pop(self.players.index(p1))
            print("Player " + str(p1.number) + " was caught in a lie, and has lost an influencer.")
            return True

    # Start the game!
    def play(self):
        turn = 0
        self.shuffle()
        p = 3
        for i in range(p):
            x = Player(i,self.deck.pop(), self.deck.pop(),self)
            self.players.append(x)
        while len(self.players) > 1:
            myturn = self.players[turn%len(self.players)]
            if not myturn.isAlive():
                self.players.pop(turn%len(self.players))
                turn += 1
            else:
                choice = random.choice(self.Actions)
                if choice == "Income":
                    myturn.Income()
                elif choice == "Foreign Aid":
                    myturn.foreignAid()
                elif choice == "Assassinate":
                    myturn.Assassinate(self.players[(turn+1)%len(self.players)])
                elif choice == "Coup":
                    myturn.Coup(self.players[(turn+1)%len(self.players)])
                elif choice == "Captain":
                    myturn.Captain(self.players[(turn+1)%len(self.players)])
                elif choice == "Ambassador":
                    myturn.Ambassador()
                else:
                    myturn.Duketax()
                turn += 1
        print("Player " + str(self.players[0].number)+ " has risen victorious!")
        # Reset the game state for future playthroughs
        self.deck = ["Assassin", "Assassin", "Assassin", "Captain", "Captain", "Captain",
        "Duke","Duke","Duke","Ambassador","Ambassador","Ambassador",
        "Contessa","Contessa","Contessa"]
        self.players = []
        self.grave = []
        self.Actions = ["Income", "Assassinate", "Foreign Aid", "DukeTax","Coup","Captain","Ambassador"]
        return