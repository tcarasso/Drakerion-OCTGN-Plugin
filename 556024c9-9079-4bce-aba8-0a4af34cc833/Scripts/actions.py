import re

###################
#### CONSTANTS ####
###################

otherPlayer = []

## Change these strings to whatever you choose to name your piles from the XML

deck = "Deck"
discard = "Discard"

## Change this HEX string value to customize the highlight color
highlight = "#ff0000"
AttackHilight = "#ae0603"

# Change this positive integer value to customize the default Draw Many count
drawManyDefault = 6

# Change this tuple if you want to create a specific default marker (not recommended)
StandardMarker = ("Marker", "d9851c6f-2ed7-4ca9-82d2-f22e4e12114c")

banners = dict(
	BannerOfTheExiled =			("2dd354ad-e5a9-4943-9117-7da05630daf0", 4, 1, "def9e961-67a3-4e06-90e8-885c5b976954", 1, "39d4acac-d2a8-4e09-b56c-2ca297f2c9f4", 1, "b81717a3-9624-4713-a7d0-0fc60335fc7f", 1, "c097c91c-f132-412a-a9ce-1a8c62afa33e"),
	BannerOfTheFirstLegion =	("1d26a19f-48a8-4393-a31f-825942e9da20", 3, 1, "750baf90-04ca-4438-8a7b-01973fcee0c4", 1, "90f5878d-88e1-4144-a92c-e9bcc7413b45", 1, "4bce5988-8512-4a40-ba58-08ae9f96bbc4"),
	BannerOfTheTwilight =		("9fe3af48-2fa0-922c-9146-5ef6422a66b5", 4, 1, "8ea7a1bb-7235-c18b-a5fc-aed62eca6032", 1, "c4474517-3d9b-e581-a6e2-e95273f2058e", 1, "0664fca6-b457-e2a5-8316-e87f3664828e", 1, "c13a752b-e81b-6773-9193-e174db4a4105"),
	AllianceOfTheAncientFolk =	("c37dc675-4c88-91b4-84e5-a56533694a99", 3, 1, "e3655f98-2d0c-b4e7-a639-87ab12218e35", 1, "6d3bd3fe-d8a7-2a9d-9181-674f0a980b5f", 1, "5659372f-41cb-4cdf-97ee-8d96cbd2caed"))

cityCommitRequiredToPlay = dict(
	ProtectedByTheWalls =	("4a7e4c45-6361-4d40-a9a5-35de9e91a968", 1),
	GalvanSTactic =			("4654dc36-d1f8-454f-b5c9-92a87adf3ee1", 1),
	FromShameToGrude =		("1d41c12a-4d33-8992-b651-d76e481c7862", 1),
	WaterIsLife =			("3494510e-b677-d6b6-9431-cc56fa7d52e8", 1))

bannerCommitRequiredToPlay = dict(
	DancingWithDeath =			("4931d2ae-3ed7-7cd6-9562-913a83f7064b", 1),
	GatheringBones =			("83eefd6c-f43a-05a2-8468-54c566d6ba6e", 1),
	FaceYourOwnDeath =			("98913402-688c-1615-a895-ec96b214be5a", 1),
	StrikeWhileTheIronIsHot =	("b3356b27-c9c4-198a-992e-6c271bd4680a", 1),
	MountainDoesntFlinch =		("f1c1efaa-33fa-d224-85e4-bc1cc329197e", 1))

def getotherplayer(player):
	global otherplayer
	otherplayer = player

######################
#### PILE ACTIONS ####
######################

def shuffle(group, x = 0, y = 0):
	mute()
	group.shuffle()
	notify("{} shuffles their {}.".format(me, group.name))

def draw(group, x = 0, y = 0):
	mute()
	if len(group) < 1:
		return
	card = group.top()
	card.moveTo(card.owner.hand)
	notify("{} draws a card from {}.".format(me, group.name))

def drawMany(group, x = 0, y = 0):
	if len(group) < 1:
		return
	mute()
	global drawManyDefault
	count = askInteger("Draw how many cards?", drawManyDefault)
	if count == None or count == 0:
		return
	drawManyDefault = count
	for card in group.top(count):
		card.moveTo(card.owner.hand)
	notify("{} draws {} cards from their {}'s.".format(me, count, group.name))

def discardMany(group, x = 0, y = 0):
	if len(group) < 1:
		return
	mute()
	count = askInteger("Discard how many cards?", 1)
	if count == None or count == 0:
		return
	for card in group.top(count):
		card.moveTo(card.owner.piles[discard])
	notify("{} discards {} cards from their {}'s.".format(me, count, group.name))

def discardManyFromBottom(group, x = 0, y = 0):
	if len(group) < 1:
		return
	mute()
	count = askInteger("Discard how many cards?", 1)
	if count == None or count == 0:
		return
	for card in group.bottom(count):
		card.moveTo(card.owner.piles[discard])
	notify("{} discards {} cards from the bottom of their {}'s.".format(me, count, group.name))

def allToDeck(group, x = 0, y = 0):
	mute()
	for card in group:
		card.moveTo(card.owner.piles[deck])
	notify("{} moves all cards from their {}'s to their {}.".format(me, group.name, me.piles[deck].name))

def	toDeck(card, x = 0, y = 0):
	mute()
	shouldReveal = confirm("Do you want to reveal choosen cards to all your opponents?")
	if shouldReveal is None:
		shouldReveal = False
	if shouldReveal is True:
		card.moveTo(card.owner.piles[deck])
		card.isFaceUp = True
		notify("{} moves {} from their {} to their {}".format(me, card, card.group.name, me.piles[deck].name))
		card.isFaceUp = False
	else:
		notify("{} moves a card from their {} to their {}.".format(me, card.group.name, me.piles[deck].name))
		card.moveTo(card.owner.piles[deck])

def allToBottom(group, x = 0, y = 0):
	mute()
	for card in group:
		card.moveToBottom(card.owner.piles[deck])
	notify("{} moves all cards from their {}'s to the bottom of their {}'s.".format(me, group.name, me.piles[deck].name))

def toDeckBottom(card, x = 0, y = 0):
	mute()
	shouldReveal = confirm("Do you want to reveal choosen cards to all your opponents?")
	if shouldReveal is None:
		shouldReveal = False
	if shouldReveal is True:
		card.moveToBottom(card.owner.piles[deck])
		card.isFaceUp = True
		notify("{} moves {} from their {} to bottom of their {}".format(me, card, card.group.name, me.piles[deck].name))
		card.isFaceUp = False
	else:
		notify("{} moves a card from their {} to the bottom of their {}.".format(me, card.group.name, me.piles[deck].name))
		card.moveToBottom(card.owner.piles[deck])
 
def allToDiscard(group, x = 0, y = 0):
	mute()
	for card in group:
		card.moveTo(card.owner.piles[discard])
	notify("{} moves all cards from {} to {}.".format(me, group.name, me.piles[discard].name))

def viewGroup(group, x = 0, y = 0):
	group.lookAt(-1)

######################
#### HAND ACTIONS ####
######################

def randomDiscard(group, x = 0, y = 0):
	mute()
	card = group.random()
	if card == None:
		return
	card.moveTo(me.piles[discard])
	notify("{} randomly discards {} from {}.".format(me, card, group.name))

def randomPick(group, x = 0, y = 0):
	mute()
	card = group.random()
	if card == None:
		return
	if confirm("Reveal randomly-picked {}?".format(card.Name)):
		index = card.index
		card.moveTo(me.piles[discard])
		notify("{} randomly picks {} from their {}.".format(me, card, group.name))
		card.moveTo(me.hand, index)
	else:
		notify("{} randomly picks {} (hidden) from their {}.".format(me, card, group.name))
	card.select()
	card.target(True)

def mulligan(group, x = 0, y = 0):
	mute()
	dlg = cardDlg(list=[], bottomList=me.Hand)
	dlg.title = "Select cards to mulligan"
	dlg.label = "To bottom of deck"
	dlg.bottomLabel = "Hand"
	dlg.text = "Select cards to mulligan, they'll be moved to the bottom of your deck and you'll draw that many new cards."
	if dlg.show() is None:
		notify("{} cancelled mulligan.".format(me))
		return
	for c in dlg.list:
		c.moveToBottom(me.Deck)
	notify("{} mulligans {} cards.".format(me, len(dlg.list)))
	for i in range(len(dlg.list)):
		draw(me.Deck)
	shuffle(me.Deck)

def play(card, x = 0, y = 0):
	mute()
	if card.named == "Yes" :
		for c in table :
			if c.properties['Name'] == card.properties['Name'] and c.controller == me:
				choiceList = ['+1 Melee Attack', '+1 Ranged Attack', '+1 Riposte', '+1 Health Point']
				colorList = ['#FF0000', '#FF0000', '#FF0000', '#FF0000']
				choice = askChoice("Choose a bonus to apply to your character", choiceList, colorList)
				if choice < 1 :
					whisper("Cancelled playing duplicate.")
					return
				else :
					if choice == 1 :
						notify("{} plays {} duplicate to get +1 Melee Attack.".format(me, card))
						card.moveTo(me.piles[discard])
						return
					if choice == 2 :
						notify("{} plays {} duplicate to get +1 Ranged Attack.".format(me, card))
						card.moveTo(me.piles[discard])
						return
					if choice == 3 :
						notify("{} plays {} duplicate to get +1 Riposte.".format(me, card))
						card.moveTo(me.piles[discard])
						return
					if choice == 4 :
						notify("{} plays {} duplicate to get +1 Health Point.".format(me, card))
						card.moveTo(me.piles[discard])
						return
	cost=int(card.Cost)
	if me.counters['Gold(s)'].value < cost :
		whisper("You don't have enough golds to pay for {}.".format(card.name))
		return
	for d in cityCommitRequiredToPlay :
		if card.model == cityCommitRequiredToPlay[d][0] :
			if card.model == "3494510e-b677-d6b6-9431-cc56fa7d52e8" :
				choiceList = ['Commit your city to play this card', 'Pay 1 gold to play this card']
				colorList = ['#FF0000', '#FF0000']
				choice = askChoice("Choose an option to play this card", choiceList, colorList)
				if choice < 1 :
					whisper("Cancelled playing {}.".format(card))
					return
				else :
					if choice == 2 :
						if me.counters['Gold(s)'].value < 1 :
							whisper("You don't have enough golds to pay for {}.".format(card.name))
							return
						else :
							notify("{} chooses to pay 1 gold to play {}.".format(me, card))
							me.counters['Gold(s)'].value -= 1
							if me.isInverted :
								card.moveToTable(0, -288)
							else :
								card.moveToTable(0, 200)
							return
			for c in table :
				if c.properties['Type'] == "City" and c.controller == me :
					if c.orientation != 0 :
						whisper("You cannot play {}, you're city is already commited.".format(card))
						return
					else :
						whisper("Please, commit your city to play this card.")
	for d in bannerCommitRequiredToPlay :
		if card.model == bannerCommitRequiredToPlay[d][0] :
			for c in table :
				if c.properties['Type'] == "Banner" and c.controller == me :
					if c.orientation != 0 :
						whisper("You cannot play {}, you're banner is already commited.".format(card))
						return
					else :
						whisper("Please, commit your banner to play this card.")
	if card.type == "Attachment" :
		list = []
		for c in table:
			if c.properties['Type'] == "Character" and c.controller == me and c.properties['Keyword(s)'] != "No attachments":
				list.append(c)
		if len(list) <= 0 :
			return
		dlg = cardDlg(list)
		dlg.title = "Characters you control"
		dlg.text = "Choose a character to attach {} to.".format(card.name)
		dlg.min = 1
		dlg.max = 1
		c = dlg.show()
		if c == None:
			notify("Please attach {} to a character mannually (shift click to target character, then CRTL+X on {}).".format(card.name, card.name))
		else:
			c[0].target(True)
			attach(card, 0, 0)
			notify("{} plays {} for {} gold(s).".format(me, card, cost))
			me.counters['Gold(s)'].value -= cost
			return
	if me.isInverted :
		card.moveToTable(0, -288)
	else :
		card.moveToTable(0, 200)
	notify("{} plays {} for {} gold(s).".format(me, card, cost))
	me.counters['Gold(s)'].value -= cost

#######################
#### TABLE ACTIONS ####
#######################

def flipCoin(group, x = 0, y = 0):
	mute()
	n = rnd(1, 2)
	if n == 1:
		notify("{} flips heads.".format(me))
	else :
		notify("{} flips tails.".format(me))

def interrupt(group, x = 0, y = 0):
	notify('{} interrupts the game.'.format(me))

def passTurn(group, x = 0, y = 0):
	notify('{} passes.'.format(me))

def addAnyMarker(cards, x = 0, y = 0):
	mute()
	marker, quantity = askMarker()
	if quantity == 0: return
	for card in cards:
		card.markers[marker] += quantity
		notify("{} adds {} {} marker(s) to {}.".format(me, quantity, marker[0], card))

def addMarker(cards, x = 0, y = 0):
	mute()
	for card in cards:
		card.markers[StandardMarker] += 1
		notify("{} adds a marker to {}.".format(me, card))

def removeMarker(cards, x = 0, y = 0):
	mute()
	for card in cards:
		if card.markers[StandardMarker] < 1:
			return
		card.markers[StandardMarker] -= 1
		notify("{} removes a marker from {}.".format(me, card))

def rotate(cards, x = 0, y = 0):
	mute()
	for card in cards:
		card.orientation ^= Rot90
		if card.orientation & Rot90 == Rot90:
			notify('{} commits {}'.format(me, card))
		else:
			notify('{} readies {}'.format(me, card))

def standAll(group, x = 0, y = 0):
    mute()
    for card in table:
        if card.controller == me:
            if card.orientation != Rot0:
                card.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def flip(cards, x = 0, y = 0):
	mute()
	for card in cards:
		if card.isFaceUp == True:
			notify("{} flips {} face down.".format(me, card))
			card.isFaceUp = False
		else:
			card.isFaceUp = True
			notify("{} flips {} face up.".format(me, card))

def highlightCard(cards, x = 0, y = 0):
	mute()
	for card in cards:
		if card.highlight != None :
			card.highlight = None
			notify('{} removes highlight from {}'.format(me, card))
		else:
			card.highlight = highlight
			notify('{} highlights {}'.format(me, card))

def discardCard(card, x = 0, y = 0):
	mute()
	card.moveTo(card.owner.piles["Discard"])
	notify("{} discards {}.".format(me, card))

def chooseFromDeckTopXShuffleRest(_group = None, _x = None, _y = None, count = None):
	"""Allows a player to take card(s) from the top X cards of their Deck and shuffles the rest to the bottom.
	The taken cards are put into player's hand and can be automatically revealed to opponents, if desired."""
	mute()
	if count == None:
		count = askInteger("Choose from how many top cards ?", 5)
	if count == None or count == 0:
		return
	dlg = cardDlg(list=[], bottomList=me.Deck.top(count))
	dlg.title = "Choose card(s) from top {}, shuffle rest to bottom".format(count)
	dlg.label = "To hand"
	dlg.bottomLabel = "To the bottom of Deck in a random order"
	dlg.text = "Select card(s) to put into your hand. The rest will shuffled and put to the bottom of your Deck." \
				"You'll be asked if you want to reveal selected cards."
	if dlg.show() is None:
		notify("{} has cancelled choosing cards from top {} of their Deck.".format(me, count))
		return
	if len(dlg.list) > 0:
		shouldReveal = confirm("Do you want to reveal choosen cards to all your opponents?")
	else:
		shouldReveal = False
	if shouldReveal is None:
		shouldReveal = False
	if shouldReveal:
		for c in dlg.list:
			me.Deck[c.index].isFaceUp = True ## c.isFaceUp doesn't work for cards in piles.
		cardInfo = ', '.join("{}".format(c) for c in dlg.list)
	else:
		cardInfo = "{} card(s)".format(len(dlg.list))
	notify("{} puts {} from top {} of their Deck to hand and the rest was shuffled and put to the bottom of their Deck".format(me, cardInfo, count))
	for c in dlg.list:
		c.moveTo(me.Hand)
	DeckBottomAllShuffle(cards=dlg.bottomList, verbose=False)

def DeckBottomAllShuffle(cards, x = 0, y = 0, verbose = True):
	mute()
	count = len(cards)
	rng = Random()
	for i in range(count - 1, 0, -1):
		j = rng.Next(0, i + 1)
		cards[i], cards[j] = cards[j], cards[i]
	for card in cards:
		card.moveToBottom(card.owner.piles['Deck'])
	if verbose:
		notify("{} shuffles {} selected cards to the bottom of their Deck.".format(me, count))

def scry(group = me.Deck, x = 0, y = 0, count = None):
	mute()
	if count == None:
		count = askInteger("Scry how many cards?", 1)
	if count == None or count == 0:
		return
	topCards = []
	for c in group.top(count):
		topCards.append(c)
	dlg = cardDlg(topCards, [])
	dlg.max = count
	dlg.title = "Scry"
	dlg.label = "Top of Deck"
	dlg.bottomLabel = "Bottom of Deck"
	dlg.text = "Reorder scryed cards to the top or bottom.\n\n(Close window to cancel scry.)"
	if dlg.show() == None:
		notify("{} has scryed for {}, {} on top 0 on bottom.".format(me, count, count))
		return
	for c in reversed(dlg.list):
		c.moveTo(group)
	for c in dlg.bottomList:
		c.moveToBottom(group)
	notify("{} scryed for {}, {} on top, {} on bottom.".format(me, count, len(dlg.list), len(dlg.bottomList)))
	group.visibility = "none"

def setUp(c, x = 0, y = 0):
	mute()
	a, b = c.position
	if (c.type != "Banner") :
		return
	for d in banners :
		k = banners[d][1]
		j = 2
		if c.model == banners[d][0] :
			if me.isInverted :
				x -= 400
				y -= 100
				if a < 0 :
					x += 800
			else :
				x += 400
				if a > 0 :
					x -= 800
			while k > 0 :
				i = banners[d][j]
				while i > 0 :
					card = me.Deck.top()
					if card.model == banners[d][j + 1] :
						card.moveToTable(x, y)
						if me.isInverted :
							x -= 10
							y-= 10
						else :
							x += 10
							y += 10
						notify("{} put {} on the table from their deck for set up.".format(me, card))
						i -= 1
					else :
						card.moveToBottom(me.Deck)
				if (j + 2) < len(banners[d]) :
					j += 2
				k -= 1
	shuffle(me.Deck)
	j = 0
	k = 0
	for k in players :
		j += 1
	if j > 1 :
		remoteCall(players[1], "getotherplayer", me)
	notify("{} finished their set up.".format(me))

def declareAttack(c, x = 0, y = 0):
	mute()
	if (c.type != "Character") :
		whisper("You can only declare an attack with a character.")
		return
	if c.controller == me and c.orientation == 0 :
		list = []
		for card in table:
			if card.type == "Character" and card.controller != me :
				list.append(card)
		if len(list) <= 0 :
			return
		c.orientation = 1
		c.highlight = AttackHilight
		notify("{} declares {} as an attacker.".format(me, c))
		dlg = cardDlg(list)
		dlg.title = "Characters controlled by {}".format(otherplayer)
		dlg.text = "Select a character to declare as a defender (remember you can only attack characters in range, 1 row if it's a melee attack, 2 rows if it's a ranged attack)."
		dlg.min = 1
		dlg.max = 1
		card = dlg.show()
		if card == None:
			notify("{} has cancelled their attack.".format(me))
			c.orientation = 0
			c.highlight = None
			return
		c.arrow(card[0])
	else :
		whisper("You can only declare an attack with a standing character you control.")

def addPrestige(group, x = 0, y = 0):
	mute()
	me.counters['Prestige'].value += 1
	notify("{} gains 1 Prestige.".format(me))

def removePrestige(group, x = 0, y = 0):
	mute()
	me.counters['Prestige'].value -= 1
	notify("{} loses 1 Prestige.".format(me))

def addGold(group, x = 0, y = 0):
	mute()
	me.counters['Gold(s)'].value += 1
	notify("{} gains 1 gold.".format(me))

def removeGold(group, x = 0, y = 0):
	mute()
	me.counters['Gold(s)'].value -= 1
	notify("{} loses 1 gold.".format(me))

def collect(card, x = 0, y = 0):
	mute()
	if card.controller == me and card.properties['Type'] == "Maneuver":
		southRevealed = confirm("Did your opponent revealed 'The South is shut' maneuver and you didn't revealed 'Gathering information' ?")
		if southRevealed is None:
			southRevealed = False
		if southRevealed:
			notify("{} collected their resources from {} minus 'The South is shut' maneuver effect.".format(me, card))
			me.counters['Gold(s)'].value += int(card.properties['Gold Value']) - 2
			count = 1
			while count < int(card.properties['Draw Value']):
				draw(me.Deck)
				count += 1
			return
		else:
			notify("{} collected their resources from {}.".format(me, card))
			me.counters['Gold(s)'].value += int(card.properties['Gold Value'])
			count = 0
			while count < int(card.properties['Draw Value']):
				draw(me.Deck)
				count += 1
			return
	else:
		whisper("You can only collect resources from a maneuver you control.")

def help(group, x = 0, y = 0):
	mute()
	whisper("Shortcut brief help:")
	whisper("F1 - this help")
	whisper("F2 - Ready all your cards")
	whisper("F10 - Reset Screen Position")
	whisper("F11 - Full Screen")
	whisper("CTRL+shift+r - Flip a coin")
	whisper("tab - Pass")
	whisper("Double click on a card - Commit/Ready card")
	whisper("CTRL+M - Mulligan your hand")
	whisper("CTRL+D - Draw card")
	whisper("CTRL+Shift+D - Draw many cards")
	whisper("CTRL+S - Shuffle Deck")
	whisper("CTRL+C - Choose card(s) from top X of your Deck, shuffle the rest and put to the bottom of your Deck")
	whisper("CTRL+SHIFT+C - Scry x cards")
	whisper("CTRL+W - Add Prestige")
	whisper("CTRL+SHIFT+W - Remove Prestige")
	whisper("CTRL+G - Add Gold")
	whisper("CTRL+SHIFT+G - Remove Gold")
	whisper("While hovering on a card :")
	whisper("If Card is a banner : CTRL+SHIFT+U - Set up")
	whisper("If Card is a maneuver : CTRL+C - Collect resources")
	whisper("If Card is a character : CTRL+SHIFT+A - Declare attack")
	whisper("CTRL+X - Attach Card to Target")
	whisper("CTRL+F - Flip Up/Down Card")
	whisper("CTRL+A - Add/Remove Marker")
	whisper("Del - Discard card")
	whisper("CTRL+Q - Add random Marker")
	whisper("CTRL+W - Remove random Marker")
	whisper("CTRL+H - Move to Hand")
	whisper("CTRL+E - Move to Deck")
	whisper("ALT+CTRL+E - Move to Deck (bottom)")
	whisper("PgUp - Bring to Front")
	whisper("PgDn - Send to Back")

def	applyDamage(eventArgs):
	mute()
	card = eventArgs.card
	if card.highlight != None :
		card.highlight = None
	card.target(active = False)
	card.arrow(card, active = False)

playerside = None

def playerSide():  ## Initializes the player's top/bottom side of table variables
	mute()
	global playerside
	if playerside == None:  ## script skips this if playerside has already been determined
		if Table.isTwoSided():
			if me.isInverted:
				playerside = -1  # inverted (negative) side of the table
			else:
				playerside = 1
		else:  ## If two-sided table is disabled, assume the player is on the top side of the table
			playerside = 1
	return playerside

def alignAttachments(card, attachments = None):  ## Aligns all attachments on the card
	mute()
	side = playerSide()
	if attachments == None:
		return
	lastCard = card
	x, y = card.position
	count = 1
	if side*y < 0:  ## A position modifier that has to take into account the vertical orientation of the card
		yyy = -1
	else:
		yyy = 1
	for id in attachments:
		c = Card(id)
		attachY = y - 11 * yyy * side * count ## the equation to identify the y coordinate of the new card
		attachX = x - 11 * yyy * side * count ## the equation to identify the x coordinate of the new card
		c.moveToTable(attachX, attachY)
		c.index = lastCard.index
		lastCard = c
		count += 1

def getAttachments(card, attachdict):
	mute()
	return [k for k,v in attachdict.iteritems() if v == card._id]

def attach(card, x = 0, y = 0):
	mute()
	target = [c for c in table if c.targetedBy]
	if len(target) > 1:
		whisper("Invalid targets, select up to 1 target.")
	else:
		cattach = eval(getGlobalVariable('cattach'))
		if len(target) == 0 or card in target:
			## DETACH
			card.target(False)
			if card._id in cattach:  ## if this card's an attachment
				notify("{} detaches {} from {}.".format(me, card, Card(cattach[card._id])))
				del cattach[card._id]
				if card.owner != card.controller: ## return card to its owner
					if card.controller == me:
						card.controller = card.owner
			for id in getAttachments(card, cattach): ## if the card has attachments
				attachment = Card(id)
				del cattach[id]
				notify("{} detaches {} from {}.".format(me, attachment, card))
				if attachment.owner != attachment.controller:
					if attachment.controller == me:
						attachment.controller = attachment.owner
			setGlobalVariable('cattach', str(cattach))
		else:
			## ATTACH
			targetcard = target[0]
			cattach[card._id] = targetcard._id
			targetcard.target(False)
			setGlobalVariable('cattach', str(cattach))
			notify("{} attaches {} to {}.".format(me, card, targetcard))
			if targetcard.controller == me:
				alignAttachments(targetcard, getAttachments(targetcard, cattach))
			else:
				card.controller = targetcard.controller
				remoteCall(targetcard.controller, 'alignAttachments', [targetcard, getAttachments(targetcard, cattach)])

def moveCardEvent(args) :
	if args.player == me :
		cattach = eval(getGlobalVariable('cattach'))
		for card in args.cards :
			alignAttachments(card, getAttachments(card, cattach))