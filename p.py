#!/usr/bin/python

"""
http://www.openbookproject.net/books/bpp4awd/ch08.html
"""

"""
# here is an example user game play
$ clear;clear;python ./p.py
(base) kali@kali:~/Projects/python/solitaire-py$ python p.py
Welcome to the Tournament shell. Type help or ? to list commands.

tournament> mg
Welcome to the Game shell. Type help or ? to list commands.

game> ng
nE
nE
nE
nE
:AS AD 2S 6C 5D KH 5S KS 2H 9C 9H QS 7C AC 3S QC 6D 2D 8S 7S 2C 6S 9D KD   dc=:::
nE nE nE nE nE nE nE
QH JS 4C 5H QD 1S 8H
.. 7H 3D JH JC 3H JD
.. .. AH 1C 5C 8D KC
.. .. .. 1H 7D 4S 6H
.. .. .. .. 8C 9S 4H
.. .. .. .. .. 4D 3C
.. .. .. .. .. .. 1D
Start playing the game. Type help or ? to list commands.

play> m
AHnE:1::S3:3:P3:0:v=300|us:0:su:0:False|ud:0:du:0:False|False:False:0:0
7H8C:2::S2:2:S5:5:v=800|us:0:su:0:False|ud:0:du:0:False|False:False:0:0
play> p
doing move: AHnE:1::S3:3:P3:0:v=300|us:0:su:0:False|ud:0:du:0:False|False:False:0:0
nE
nE
nE AH
nE
:AS AD 2S 6C 5D KH 5S KS 2H 9C 9H QS 7C AC 3S QC 6D 2D 8S 7S 2C 6S 9D KD   dc=:::
nE nE nE nE nE nE nE
QH JS 4C 5H QD 1S 8H
.. 7H 3D JH JC 3H JD
.. .. .. 1C 5C 8D KC
.. .. .. 1H 7D 4S 6H
.. .. .. .. 8C 9S 4H
.. .. .. .. .. 4D 3C
.. .. .. .. .. .. 1D
play> exit
We played 1 moves.
game> exit
tournament> exit
(base) kali@kali:~/Projects/python/solitaire-py$
"""

"""
Autoplay lots of game:
$ ./p.py <<EOF | grep "Game #"
ag
EOF
"""

"""
# use shell to display only every 100th game won/loss message:

(base) kali@kali:~/Projects/python/solitaire-py$ python --version
Python 3.9.7
(base) kali@kali:~/Projects/python/solitaire-py$ python p.py <<EOF | grep "Game #" | awk '!(NR%100)'
ag
EOF
"""

"""
# output of runs as of 13-dec-21
                                       Game #8000 Won 1762 22.025%
                                       Game #8100 Won 1786 22.049382716049383%
                                       Game #8200 Won 1804 22.0%
                                       Game #8300 Won 1822 21.951807228915662%
                                       Game #8400 Won 1841 21.916666666666668%
                                       Game #8500 Won 1863 21.91764705882353%
                                       Game #8600 Won 1889 21.96511627906977%
                                       Game #8700 Won 1903 21.873563218390803%
                                       Game #8800 Won 1930 21.931818181818183%
                                       Game #8900 Won 1949 21.898876404494384%
                                       Game #9000 Won 1969 21.877777777777776%
                                       Game #9100 Won 1987 21.835164835164836%
                                       Game #9200 Won 2011 21.858695652173914%
                                       Game #9300 Won 2034 21.870967741935484%
                                       Game #9400 Won 2055 21.861702127659573%
                                       Game #9500 Won 2079 21.88421052631579%
                                       Game #9600 Won 2099 21.864583333333336%
                                       Game #9700 Won 2113 21.783505154639172%

"""

"""
# card display description
nE = means no card here
nS = normal card where n is the numeric value of the card (A,2,3,4,5,6,7,8,9,1,J,Q,K) and
     S is the suit (H,S,C,D)
"""

"""
#  discription board layout
(base) kali@kali:~/Projects/python/solitaire-py$ python p.py
Welcome to the Tournament shell. Type help or ? to list commands.

tournament> mg
Welcome to the Game shell. Type help or ? to list commands.

game> ng

play> db <--- command line
nE  <--- suit pile
nE  <--- suit pile
nE  <--- suit pile
nE  <--- suit pile

+--- deck of cards
|
| +--- bottom of deck (card on top of deck is placed here when deal deck dd command)
| |
| |                                               original top of deck card ---+
| |                                                 this is end of game card   |
| |                                                                            |
| |             top card on deck (only visible/playable deck card) ---+        |
| |                                                                   |        |
V V                                                                   V        V
:3D 9C 1D 9D 6H 8C 1C KD 2D 3S 4H 3H JS 4S 7S 5S 6D 2C AC KH QD 6C AS 7D   dc=:9C::
nE nE nE nE nE nE nE

+--- card stacks
|
| only the cards on the diagonal are visible/playable
| the cards not on the diagonal are not visible (unless cheating?)
V
QH 4D JD 1H JH 6S 8H
.. AD 5C JC 4C QC 7C
.. .. QS 2S 5H 1S 3C
.. .. .. AH 9H 9S 7H
.. .. .. .. KC KS 8S
.. .. .. .. .. 5D 8D
.. .. .. .. .. .. 2H
play>  <--- command line

"""

# import color  # for ansi color codes
from color import colors  # for ansi color codes

#from treelib import *

# from copy import deepcopy # to copy objects
# from copy import *
import copy

# from pickle import dump, load # for object file i/o
import pickle

# from cmd import cmd, Cmd # for interactive command loop
# from cmd import *
import cmd

# from sys import exc_info, exit # for system calls
import sys

# global variables
VERSION_STRING = "1.1"  # for about command
TOURNAMENT_COMMAND_QUEUE = ""  # auto-commanding when needed
GAME_COMMAND_QUEUE = ""  # auto-commanding when needed
PLAY_COMMAND_QUEUE = ""  # auto-commanding when needed
GAMES_WON_COUNT = 0  # count how many games won this tournament


# print("Hello Python!")

# foundational playing card class
class Card(object):
    """Playing Card class that defines a single playing card"""
    SUITS = ('Clubs', 'Diamonds', 'Hearts', 'Spades', 'Empty')
    RANKS = ('narf', 'Ace', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'Jack', 'Queen', 'King')

    def __init__(self,
                 suit=4,  # 4 == empty suit (no suit yet)
                 rank=0,  # 0 == no rank yet
                 visible=False,  # can't see me yet
                 hand=None,  # this card not in any Hand(Deck) yet
                 position=0):  # no position yet

        # what this card is
        self.suit = suit  # this card's suit
        self.rank = rank  # this card's number
        self.visible = visible  # is this card visible or covered on the board?
        # form unique card name from rank and suit 2H JC KS
        self.name = Card.RANKS[self.rank][0] + Card.SUITS[self.suit][0]

        # where this card is
        self.hand = hand  # which hand is this card in
        self.position = position  # which position in the hand this card is in

    @staticmethod
    def is_card_movable(sourcecard, destinationcard):
        """" determine if source card can be moved to desitnation card
             return a value of the move and if can be moved """

        if False:  # True:
            print("sourcecard      " + sourcecard.name + \
                  " suit " + str(sourcecard.suit) + \
                  " rank " + str(sourcecard.rank) + \
                  " hand " + sourcecard.hand.name + \
                  " pos  " + str(sourcecard.position) + \
                  " vis  " + str(sourcecard.visible))

            print("destinationcard      " + destinationcard.name + \
                  " suit " + str(destinationcard.suit) + \
                  " rank " + str(destinationcard.rank) + \
                  " hand " + destinationcard.hand.name + \
                  " pos  " + str(destinationcard.position) + \
                  " vis  " + str(destinationcard.visible))

        # set initial value to low priority move (for False returns)
        value = 2001  # higher value is lower priority

        # set source card not in normal solved position
        normalposition = False  # not normal position

        # check if deck destination
        if destinationcard.hand.name == "Deck":
            return value, False  # should never happen!

        # check if destination is within the stacks or piles
        isstackdestination = False
        ispiledestination = False
        if destinationcard.hand.name == "S1" or \
                destinationcard.hand.name == "S2" or \
                destinationcard.hand.name == "S3" or \
                destinationcard.hand.name == "S4" or \
                destinationcard.hand.name == "S5" or \
                destinationcard.hand.name == "S6" or \
                destinationcard.hand.name == "S7":
            isstackdestination = True
        else:
            ispiledestination = True

        # print isstackdestination
        # print ispiledestination

        # check for pile to pile move (not allowed!)
        if ispiledestination and \
                sourcecard.hand.suit != 4:  # pile to pile (pile.suit == 4)
            return value, False  # pile to pile not allowed

        # check for a possible move but not needed because
        # already in position

        #   do this only for stack destinations
        #   allow moves to piles to happen even if in normal order on stack
        if (not ispiledestination) and \
                (not sourcecard.position == 0):  # not at top of stack because
            # no upcard when at top of stack
            thiscard = sourcecard

            # get card just covered by this card
            upcard = sourcecard.hand.cards[thiscard.position - 1]

            # check for source card in normal solved position on stack
            # low prio move if cards in source stack are already in
            # normal position
            #  meaning opposite suit + stack rank order + upcard is visible
            #  This is checking if the source card and the card it is on
            #  is already in solved order. This would make moving this
            #  source card to another destination a very low priority move.
            #  However- this is exactly the type of move needed when in
            #  the special game condition of walking up the ladder.
            #  Therefore we don't want to reject this move completely but
            #  set its prio so low that it is made only as last resort
            #  which is what walking up the ladder it.
            if ((((((thiscard.suit == 0) or (thiscard.suit == 3)) and
                   ((upcard.suit == 1) or (upcard.suit == 2))) or \
                  (((thiscard.suit == 1) or (thiscard.suit == 2)) and \
                   ((upcard.suit == 0) or (upcard.suit == 3)))) and \
                 (thiscard.rank == (upcard.rank - 1))) and \
                    (upcard.visible == True)):

                # indicate normal position for use in determining
                # move value
                normalposition = True  # is normal position
                # keep checking for a move
            else:

                normalposition = False  # not normal position
                # keep checking for a move

        # print normalposition

        # check for moves within the stacks (not piles)
        #    check for a stack destination (not pile)
        #    skip a stack destination that is an ace (==1) or a duece (==2)
        if (isstackdestination) and \
                (not destinationcard.rank == 1) and \
                (not destinationcard.rank == 2):

            # if here then it is a possible legit destination within the stacks

            # check for opposite suite and one lower rank
            if (((((sourcecard.suit == 0) or (sourcecard.suit == 3)) and \
                  ((destinationcard.suit == 1) or (destinationcard.suit == 2))) or \
                 (((sourcecard.suit == 1) or (sourcecard.suit == 2)) and \
                  ((destinationcard.suit == 0) or (destinationcard.suit == 3)))) and \
                    (sourcecard.rank == (destinationcard.rank - 1))):

                # if source is from a pile then low prio move
                if sourcecard.hand.suit != 4: # source is from a pile
                                              # low priority move
                    value = 900

                else:

                    # when here:
                    #   we found a stack to stack move
                    #   but if it is an in normal position set
                    #   the prio lower
                    if not normalposition:
                        value = 800  # source is into stack
                                     # (stack.suit == 4) so
                                     # higher value is lower priority
                    else:
                        value = 1000 # this is a move but from
                                     # a normal position so low prio

                return value, True

            else:

                # check for king (==13) onto empty stack (==0) and
                # not an empty pile (pile was check for and excluded above)
                if sourcecard.rank == 13 and \
                        destinationcard.rank == 0:

                    # check for a deck king move (always allowed)
                    if sourcecard.hand.name == "Deck":

                        # this source king is on top of deck
                        # so mark it as a move

                        value = 600  # higher value is lower priority
                        return value, True  # this is a worthwhile
                        # movable king

                    # check for king already at top of stack with
                    # stack having an empty (rank=0) card on top
                    # remember: stacks always have an empty card in
                    #           position [0] so a top of stack king
                    #           is in position [1]
                    elif not sourcecard.hand.cards[1].rank == 13:

                        # this source king is not at top of a stack
                        # so mark it as a move

                        value = 700  # higher value is lower priority
                        return value, True  # this is a worthwhile
                                            # movable king
                    else:

                        # this source king card is already at the
                        # top of a stack so not worth moving it

                        return value, False # this is a not worth
                                            # it movable king

                else:
                    return value, False  # if here then not an
                                         # available move

        else:  # check for moves within the piles
            # check for ace onto empty its own suit pile
            if sourcecard.rank == 1 and \
                    destinationcard.hand.suit == sourcecard.suit and \
                    destinationcard.rank == 0:
                value = 300  # higher value is lower priority
                return value, True
            else:
                # check for normal card onto its own suit pile
                # and only if last card on source stack
                # because if not last card on stack then there
                # is a downcard that cannot be moved to the pile
                #   check if last source card from stack
                #   (hand.suit == 4) and source card == hand.last card [-1]
                if (((sourcecard.suit == destinationcard.hand.suit) and \
                     (sourcecard.rank == (destinationcard.rank + 1))) and \
                        ((sourcecard.hand.suit == 4) and \
                         (sourcecard == sourcecard.hand.cards[-1]))):

                    value = 400  # higher value is lower priority
                    return value, True

                else:

                    return value, False  # if here then not an
                                         # available move onto a pile

    def __str__(self):
        """

          > >> print(Card(2, 12))
          Queen of Hearts
        """

        fgc = colors.fg.pink
        bgc = colors.reset + colors.bold if (self.visible) \
            else colors.bg.blue

        color = colors.text.green if \
            ((Card.SUITS[self.suit] == 'Clubs') or
             (Card.SUITS[self.suit] == 'Spades')) else \
            colors.text.red

        return '' + fgc + bgc + color + '{0}{1}'.format(
            Card.RANKS[self.rank][0],
            Card.SUITS[self.suit][0] + colors.reset) + ''


class Deck(object):
    """ foundational deck of play cards class """

    def __init__(self):
        self.cards = []  # start empty
        self.name = "Deck"  # give a name to this deck
        self.suit = 4  # indicate this is a no suit
        # hand (just like stack but
        # not pile)
        self.deathcard = ""  # virtual death card

        for suit in range(4):  # populate cards in box order
            for rank in range(1, 14):
                self.cards.append(Card(suit=suit,
                                       rank=rank,
                                       visible=False,
                                       hand=self,
                                       position=((suit * 13) + (rank - 1))))

        # display fresh unshuffled deck
        # for card in self.cards:
        #    print "create card:" + card.name + " " + str(card.position)

    def __str__(self):
        _str = ""
        for i in range(len(self.cards)):
            # _str += " " * i + str(self.cards[i]) + "\n"
            _str += str(self.cards[i]) + "\n"
        return _str

    def __len__(self):  # return how many cards in this deck
        return len(self.cards)

    def display_deck(self):
        """ Display deck of cards """

        _str = ""
        for i in range(len(self.cards)):
            # _str += " " * i + str(self.cards[i]) + "\n"
            _str += str(self.cards[i]) + " "

        if self.name[0] != 'P':  # suppress on piles (no deathcard on piles)
            _str += "  dc=:" + self.deathcard + ":"

        return _str

    def shuffle(self):
        """ shuffle the deck of cards """

        import random

        num_cards = len(self.cards)

        # print "shuffle " + str(num_cards) + " cards:"

        for i in range(num_cards):
            j = random.randrange(i, num_cards)

            # print "i=" + str(i) + " j=" + str(j)
            # print self.cards[i].name + " " + str(self.cards[i].position)
            # print self.cards[j].name + " " + str(self.cards[j].position)

            # swap the i'th and j'th card
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

            # temp = self.cards[i]
            # self.cards[i] =  self.cards[j]  # move card
            # self.cards[j] =  temp           # move card

            # swap the card's position too
            self.cards[i].postion, self.cards[j].position = j, i

        # renumber the cards for some reason the above does not???
        for i in range(num_cards):
            self.cards[i].position = i

        # display shuffled deck
        # for card in self.cards:
        #    print "create card:" + card.name + " " + str(card.position)

    def rotate(self, game):
        """ wrap popped card to front and make hidden;
            make new exposed card visible
            Deal deck to make new deck card visible"""

        if len(self.cards) == 0:
            # put an empty card of death onto deck
            self.cards.insert(0, Card(suit=4,
                                      rank=0,
                                      visible=False,
                                      hand=game.board.deck,
                                      position=0))

            return False

        # increment game moves here because a 'dd' does not call do_move()
        # and adding a death card is not really a user move
        game.movescount += 1  # so count the upcomming move

        # save a deck deal move to the game
        #   this creates a deck-to-deck move object and adds it to
        #   the game
        try:
            undodupcard = \
                copy.deepcopy(self.cards[-2])
        except IndexError:
            undodupcard = \
                copy.deepcopy(self.cards[-1])

        game.gamemoves.append(
            Move(
                sourcecard=copy.deepcopy(self.cards[-1]),  # move this card
                destinationcard=copy.deepcopy(self.cards[0]),  # to this card
                movenumber=1,  # n/a move number
                movevalue=0,  # n/a prio
                # where the card ended up
                #   this will become the source card for undo
                undosourcecard= \
                    copy.deepcopy(self.cards[0]),
                # where the card came from
                #   this will become the destination card for undo
                undodestinationcard= \
                    copy.deepcopy(self.cards[-1]),
                # the upcard from where the card came from
                #   this will help reset the top card to the premove state
                undodupcard=undodupcard,
                moveid=game.movescount,  # create unique move id
                gamemove=game.movescount,  # which game move number
                # this move is
                gamestate=None))  # game saved after this move

        # pop top card   this was the visible card on the deck
        oldcard = self.cards.pop()  # get card on top of deck
        oldcard.visible = False  # can't see it any more

        # add a virtual death card if not already set
        if self.deathcard == "":
            self.deathcard = oldcard.name

        # add a death card before popped card if not already one in deck
        nocard = True
        for card in self.cards:  # look for death card in deck
            if card.rank == 0:  # found one! rank == 0 == empty card
                nocard = False  # not no card found
                break

        if nocard and \
                oldcard.rank != 0:  # add if no empty card found

            # put an empty card of death onto deck
            # self.cards.insert(0, Card(4, 0, False, hand=game.board.deck))

            # indicate this rotate put a ne card on deck
            #   use this indicator to remove that ne card upon undoing
            game.gamemoves[-1].movevalue = -1  # coop value for indicator

        # put popped card onto bottom of deck
        # do this after a death card has been added
        # (if not a death card already)
        self.cards.insert(0, oldcard)  # put onto bottom of deck

        # make new top card visible
        self.cards[-1].visible = True  # can now see new deck card

        num_cards = len(self.cards)
        for i in range(num_cards):  # reposition cards after rotate
            self.cards[i].position = i

        # print self

        # when here:
        # 1. the deck was rotated by 1
        # 2. the gamemoves had been updated to be able to undo this
        #    rotate

        # display move for debug
        if False:
            print("did move: " + str(game.movescount) + " " + \
                  str(game.gamemoves[-1]))

        # return False if reached a death card meaning
        # already looped through deck without a move
        print(self.cards[-1].name)
        print(self.deathcard)
        if self.cards[-1].name == self.deathcard:
            playablecardfound = False  # hit the death card upon this rotation
        else:
            playablecardfound = True

        # this is old code for when the death card was a real card
        # it is all pass now
        # retained for historical purposes
        if self.cards[-1].rank == 0:  # found a death card

            # make top deck death card invisible so it does not
            # try to get played
            # self.cards[-1].visible = False

            # playablecardfound = False # hit the death card upon this rotation
            pass

        else:

            # playablecardfound = True
            pass

        # update the gamemove with this game
        # game.gamemoves[-1].gamestate = copy.deepcopy(game)
        # game.gamemoves[-1].gamestate.board.deck = copy.deepcopy(self)
        # game.gamemoves[-1].gamestate.gamemoves = []  # null out saved game
        #                                     # moves else many games get saved
        # save only the part of the game that is needed for move compare
        # get a new game
        game.gamemoves[-1].gamestate = CardGame(board=SBoard(), deck=Deck())
        # store current game
        game.gamemoves[-1].gamestate.board = copy.deepcopy(game.board)
        game.gamemoves[-1].gamestate.deck = []  # don't need this either
        game.gamemoves[-1].gamestate.moveid = game.gamemoves[-1].moveid  # save
        # this move's id
        game.gamemoves[-1].gamestate.movescount = game.gamemoves[-1].gamemove
        # save this
        # move's count

        # when here:
        # 1. game updated to most recent deck rotation move
        # 2. gamemoves updated to contain this deck rotation move

        # return state of deck's top card playable or not
        return playablecardfound

    def remove_death_card(self):
        """ remove deck death card after a move
            (give deck another chance through)"""

        # remove all death cards from deck after a move
        for card in self.cards:

            # print card.name + "   " + str(card.rank)

            if card.rank == 0:  # empty card has rank of zero

                self.cards.remove(card)  # take it out of deck

                # reposition cards after removal
                num_cards = len(self.cards)
                for i in range(num_cards):
                    self.cards[i].position = i

        # always make the deck card visible
        # (case where death card popped else deck card
        # should be visible anyway
        if len(self.cards) > 0:
            self.cards[-1].visible = True

        # reset virtual death card
        self.deathcard = ""  # no more death card

        return

    def remove(self, card):
        """ remove a particular card from a deck """

        # print("removing " + card.name + " " + \
        #      card.hand.name + " " + str(card.position) + \
        #      " from self." + self.name)

        if card in self.cards:
            self.cards.remove(card)
            # print "found to remove"
            # if card in self.cards:
            #    print "but still found?"
            # else:
            #    print "not found!"
            #
            # print self

            num_cards = len(self.cards)
            for i in range(num_cards):  # reposition cards after remove
                self.cards[i].position = i

            return True
        else:
            return False

    def pop(self):
        """ return the card on the end of the deck """
        return self.cards.pop()

    def is_empty(self):
        """ return True if deck does not contain any cards """
        return len(self.cards) == 0

    def deal(self, hands, num_cards=999):
        """ deal cards evenly into each hand until no more cards """
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():  # break if out of cards
                break
            card = self.pop()  # take the top card
            hand = hands[i % num_hands]  # whose turn is next?
            hand.add(card)  # add the card to the hand


class Hand(Deck):
    """ foundational hand of play cards class """

    def __init__(self, name="", suit=-1):
        super(Hand, self).__init__()
        self.cards = []  # hands contain a list of card
        self.name = name  # each hand has a name
        self.suit = suit  # each hand has an optional suit
                        # (for example: allow only cards of this
                        # suit in this hand)
        self.deathcard = ""

        return

    def add(self, card):
        """add card to self hand """
        card.hand = self  # add this hand into card so card knows
        # which hand it is in

        card.position = len(self.cards)  # add position of card
        # in hand into the card
        # so card knows where it is
        self.cards.append(card)

        return

    def __str__(self):
        """Do not prefix with hand name"""
        _str = ""  # prefix with empty string
        if self.is_empty():
            _str = ".."  # empty card string

        # return _str + Deck.__str__(self)  # __str__ appends newline
        return _str + Deck.display_deck(self)  # no newline

    def display_hand(self):
        """Prefix with hand name"""
        _str = "Hand " + self.name  # prefix with hand name
        if self.is_empty():
            _str = _str + " is empty\n"
        else:
            _str = _str + " contains\n"

        return _str + Deck.display_deck(self)

    def display_card(self, card=0):
        """ display card (by index) if in hand else blanks """

        if card < len(self.cards):
            return str(self.cards[card])
        else:
            return ".."


class Board(object):
    """ foundational board of a game class """

    def __init__(self):
        pass


class SBoard(Board):
    """ specialized board of a solataire game class """

    def __init__(self):
        """ initialize the card structures that exist on the board """

        # initialize suit piles
        self.p1 = Hand("P1", 0)  # one of four suit discard pile fix suit
        self.p2 = Hand("P2", 1)  # one of four suit discard pile
        self.p3 = Hand("P3", 2)  # one of four suit discard pile
        self.p4 = Hand("P4", 3)  # one of four suit discard pile

        # put non-existing card on suit piles
        self.p1.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.p1,  # this card Hand(Deck)
                         position=0))  # no position yet
        self.p2.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.p2,  # this card Hand(Deck)
                         position=0))  # no position yet
        self.p3.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.p3,  # this card Hand(Deck)
                         position=0))  # no position yet
        self.p4.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.p4,  # this card Hand(Deck)
                         position=0))  # no position yet

        # initialize stacks
        self.s1 = Hand("S1", 4)  # one of seven card stacks no suit
        self.s2 = Hand("S2", 4)  # one of seven card stacks
        self.s3 = Hand("S3", 4)  # one of seven card stacks
        self.s4 = Hand("S4", 4)  # one of seven card stacks
        self.s5 = Hand("S5", 4)  # one of seven card stacks
        self.s6 = Hand("S6", 4)  # one of seven card stacks
        self.s7 = Hand("S7", 4)  # one of seven card stacks

        self.deck = []        # there is the deck on the board
                              # but is included as part of the game

        # helper lists for iterations of board structures
        #    seven stacks of cards on board
        self.stacks = [self.s1, self.s2, self.s3, self.s4,
                       self.s5, self.s6, self.s7]
        #    four put up piles of cards on board
        self.piles = [self.p1, self.p2, self.p3, self.p4]

        return

    @classmethod
    def check_board_lowlow_condition(self, game):
        """Check board for all suits lowlow conditon"""

        # clubs (black suit)
        clublow1card, \
        clublow2card, \
        clublowlow = game.board.check_suit_lowlow_condition(game=game,
                                                            suit=0)

        # diamonds (red suit)
        diamondlow1card, \
        diamondlow2card, \
        diamondlowlow = game.board.check_suit_lowlow_condition(game=game,
                                                               suit=1)

        # hearts (red suit)
        heartlow1card, \
        heartlow2card, \
        heartlowlow = game.board.check_suit_lowlow_condition(game=game,
                                                             suit=2)

        # spades (black suit)
        spadelow1card, \
        spadelow2card, \
        spadelowlow = game.board.check_suit_lowlow_condition(game=game,
                                                             suit=3)

        # get number of suits in lowlow condition
        blacks = reds = 0  # start with none in lowlow condition

        # check each suit then increment count if in lowlow
        if clublowlow:
            blacks += 1  # increment suits in lowlow condition

        if diamondlowlow:
            reds += 1  # increment suits in lowlow condition

        if heartlowlow:
            reds += 1  # increment suits in lowlow condition

        if spadelowlow:
            blacks += 1  # increment suits in lowlow condition

        return blacks, reds  # return number of suits on board in lowlow

    @classmethod
    def check_suit_lowlow_condition(self, game, suit):
        """Check suit for two lowest cards visible"""

        low1card = low2card = ".."  # start with no low cards found
        low1bool = low2bool = False  # start with no low cards found

        if 0 <= suit < 4:

            cardlist = game.board.list_suits()  # get all cards box order

            for rank in range(0, 13):  # loop each card low to high

                # look for lowest visible card
                if cardlist[(suit * 13) + rank].visible:  # lowest card visible

                    # found lowest visible card
                    low1card = str(cardlist[(suit * 13) + rank])
                    low1bool = True

                    if rank < 12:  # don't check for next lowest if a king

                        # look for next lowest card is visible
                        if cardlist[(suit * 13) + (rank + 1)].visible:

                            # found next lowest visible card
                            low2card = str(cardlist[(suit * 13) + (rank + 1)])
                            low2bool = True

                        else:

                            low2card = ".."  # not next lowest found
                            low2bool = False
                    else:

                        # handle when first low card is a king
                        low2card = "ne"  # empty card next lowest after king
                        low2bool = True  # if king visible then
                        # lowlow is true

                    break  # got the low cards

                else:

                    continue  # keep looking for lowest visible

            # when here:
            # lowxcard contains the low card or .. or ne
            # lowxbool contains true if a low card or false if no low card

        else:
            pass  # suit not in range therefore suit not lowlow

        # return the low cards and true if lowlow and false if not lowlow
        return low1card, low2card, (low1bool and low2bool)

    def check_board_won(self, game):  # check to see if a winning game
        """Check if board has been won"""

        # check win criteria
        #  using the deck short circuits the win determination
        #  but leaves the game in an uncompleted state
        #  using the piles leaves the game in a completed state
        # usedeck = True # use empty deck as criteria for a win
        usedeck = False  # use full piles as criteria for a win

        if usedeck:

            # this does not work because there could be the
            # non-death empty card on the deck
            # and would need to look for that here because
            # that means len==1 and is empty but is_empty()
            # return false
            if not game.board.deck.is_empty():
                return False  # deck not empty means game not won

        else:
            # check piles
            for pile in self.piles:  # check each pile for a king on top
                if pile.cards[-1].rank == 13:  # look for kings on top of piles
                    pass  # found a king look for more
                else:
                    return False  # if not a king then not a won game

        # when here:
        # 1. the game is won

        global GAMES_WON_COUNT  # count how many games won this tournament
        GAMES_WON_COUNT += 1  # count how many games won this tournament

        return True  # if here then the game has been won

    def compare_games(self, currentgame, originalmovegame):
        """ make sure current board matches saved board  """

        miscomparelist = ""  # initialize miscompared cards list

        ogame = originalmovegame.gamestate  # short name

        # compare in piles
        for cpile in currentgame.board.piles:  # compare cards in piles

            for opile in ogame.board.piles:  # compare cards in piles

                # compare in matching piles
                if cpile.name == opile.name:  # found matching pile to compare

                    # get each current card to compare with orginal card
                    for iccard, ccard in enumerate(cpile.cards):

                        iocard = iccard  # same position number

                        # get equivalent original card if any
                        try:
                            ocard = opile.cards[iocard]
                        except IndexError:

                            # make special orginal card if there is none
                            ocard = Card(suit=4,  # 4 == empty suit (no suit yet)
                                         rank=0,  # 0 == no rank yet
                                         visible=False,  # can't see me now
                                         # no known hand yet
                                         hand=Hand(name="pilenotevencloseinorginalgame"),
                                         position=iocard)  # no position yet

                        # when here:
                        # should have a current card and ocard to compare

                        # compare card attributes for match or not
                        if (ccard.suit != ocard.suit) or \
                                (ccard.rank != ocard.rank) or \
                                (ccard.position != ocard.position) or \
                                (ccard.visible != ocard.visible):
                            # found miscompare
                            miscomparestring = \
                                ":" + \
                                str(currentgame.movescount) + "?" + \
                                str(ogame.movescount) + "+" + \
                                cpile.name + "?" + opile.name + "|" + \
                                str(ccard.suit) + "?" + str(ocard.suit) + "|" + \
                                str(ccard.rank) + "?" + str(ocard.rank) + "|" + \
                                str(ccard.position) + "?" + str(ocard.position) + "|" + \
                                str(ccard.visible) + "?" + str(ocard.visible) + "|" + \
                                ":"

                            # save into big string
                            miscomparelist += miscomparestring

        # compare in stacks
        for cstack in currentgame.board.stacks:  # compare cards in stacks

            for ostack in ogame.board.stacks:  # compare cards in stacks

                # compare in matching stacks
                if cstack.name == ostack.name:  # found matching stack to compare

                    # get each current card to compare with orginal card
                    for iccard, ccard in enumerate(cstack.cards):

                        iocard = iccard  # same position number

                        # get equivalent original card if any
                        try:
                            ocard = ostack.cards[iocard]
                        except IndexError:

                            # make special orginal card if there is none
                            ocard = Card(suit=4,  # 4 == empty suit (no suit yet)
                                         rank=0,  # 0 == no rank yet
                                         visible=False,  # can't see me now
                                         # no known hand yet
                                         hand=Hand(name="stacknotevencloseinorginalgme"),
                                         position=iocard)  # no position yet

                        # when here:
                        # should have a current card and ocard to compare

                        # compare card attributes for match or not
                        if (ccard.suit != ocard.suit) or \
                                (ccard.rank != ocard.rank) or \
                                (ccard.position != ocard.position) or \
                                (ccard.visible != ocard.visible):
                            # found miscompare
                            miscomparestring = \
                                ":" + \
                                str(currentgame.movescount) + "?" + \
                                str(ogame.movescount) + "+" + \
                                cstack.name + "?" + ostack.name + "|" + \
                                str(ccard.suit) + "?" + str(ocard.suit) + "|" + \
                                str(ccard.rank) + "?" + str(ocard.rank) + "|" + \
                                str(ccard.position) + "?" + str(ocard.position) + "|" + \
                                str(ccard.visible) + "?" + str(ocard.visible) + "|" + \
                                ":"

                            # save into big string
                            miscomparelist += miscomparestring

        # compare in deck
        for icdeck in range(1):  # keep loop indent structure

            # get current deck
            cdeck = currentgame.board.deck  # compare cards in decks

            # get orginal deck
            for iodeck in range(1):  # keep loop indent structure

                odeck = ogame.board.deck  # compare cards in decks

                # compare in matching decks
                if cdeck.name == odeck.name:  # found matching deck to compare

                    # get each current card to compare with orginal card
                    for iccard, ccard in enumerate(cdeck.cards):

                        iocard = iccard  # same position number
                        # get equivalent original card if any

                        try:
                            ocard = odeck.cards[iocard]
                        except IndexError:

                            # make special orginal card if there is none
                            ocard = Card(suit=4,  # 4 == empty suit (no suit yet)
                                         rank=0,  # 0 == no rank yet
                                         visible=False,  # can't see me now
                                         # no known hand yet
                                         hand=Hand(name="decknotevencloseinorginalgame"),
                                         position=iocard)  # no position yet

                        # when here:
                        # should have a current card and ocard to compare

                        # compare card attributes for match or not
                        if (ccard.suit != ocard.suit) or \
                                (ccard.rank != ocard.rank) or \
                                (ccard.position != ocard.position) or \
                                (ccard.visible != ocard.visible):

                            if False:  # True:
                                # display deck
                                print("original deck:")
                                print(':' + ogame.board.deck.display_deck() + ':')
                                print("current deck:")
                                print(':' + currentgame.board.deck.display_deck() + ':')

                            # found miscompare
                            miscomparestring = \
                                ":" + \
                                str(currentgame.movescount) + "?" + \
                                str(ogame.movescount) + "+" + \
                                cdeck.name + "?" + odeck.name + "|" + \
                                str(ccard.suit) + "?" + str(ocard.suit) + "|" + \
                                str(ccard.rank) + "?" + str(ocard.rank) + "|" + \
                                str(ccard.position) + "?" + str(ocard.position) + "|" + \
                                str(ccard.visible) + "?" + str(ocard.visible) + "|" + \
                                ":"

                            # save into big string # move 0 is not playable
                            miscomparelist += miscomparestring

        if len(miscomparelist) != 0:
            print("miscompare list = *" + miscomparelist + "*")
            print("vvvvvvvvvvvv original game vvvvvvvvvvvv")
            ogame.board.display_board(ogame)  # pass in game to get access
            print("^^^^^^^^^^^^ original game ^^^^^^^^^^^^")
            raw_input("pause")

        return True  # if here the board passed checks

    def check_board_integrity(self, game):
        """ make sure board is sane (no out of position cards) """

        # start out hopeful
        boardpassed = True  # t = board has integrity

        # check for 52 cards
        numcards = 0

        # count in piles
        for pile in self.piles:  # count cards in piles
            for card in pile.cards:
                if card.rank != 0:  # don't count empty cards
                    numcards += 1

        # print "pile count = " + str(numcards)
        # count in stacks
        for stack in self.stacks:  # count cards in stack
            for card in stack.cards:
                if card.rank != 0:  # don't count empty cards
                    numcards += 1
        # print "stack count = " + str(numcards)

        # count in deck
        for card in self.deck.cards:  # count cards in deck
            if card.rank != 0:  # don't count empty cards
                numcards += 1

        # print "deck count = " + str(numcards)
        if numcards != 52:
            print("Expected 52 cards. Counted " + str(numcards))
            boardpassed = False  # board has card count problem

        # when here we know there are 52 card on the board

        # check integrity of board
        # check piles
        for pile in self.piles:  # check each pile for normality
            for icard, card in enumerate(pile.cards):  # check each card in pile

                # check for internally consistent card position
                if card.position != icard:  # card has wrong position?
                    print("pile " + pile.name + " " + card.name + " " + \
                          "expected position " + str(icard) + " " + \
                          "but card position is " + str(card.position))

                    boardpassed = False  # board has pile position problem

                # check right suit in right pile
                if card.rank == 0:
                    continue  # skip empty cards
                else:
                    if card.suit != pile.suit:  # mismatch pile
                        print("pile " + " " + pile.name + " " + \
                              str(pile.suit) + "  card " + card.name + \
                              " " + str(card.suit) + " " + str(card.rank))

                        boardpassed = False  # board has piles problem
                        # raise mismatchinpile

        # check stacks
        for stack in self.stacks:  # check each stack for normality
            for icard, card in enumerate(stack.cards):  # check cards in stack

                # check for internally consistent card position
                if card.position != icard:  # card has wrong position?
                    print("stack " + stack.name + " " + card.name + " " + \
                          "expected position " + str(icard) + " " + \
                          "but card position is " + str(card.position))

                    boardpassed = False  # board has stack position problem

                # check right suit in right pile
                if card.rank == 0:
                    continue  # skip empty cards
                else:
                    pass  # do some check here for stack integrity

        # check deck
        for icard, card in enumerate(self.deck.cards):  # count cards in deck

            # check for internally consistent card position
            if card.position != icard:  # card has wrong position?
                print("deck " + card.name + " " + \
                      "expected position " + str(icard) + " " + \
                      "but card position is " + str(card.position))

        return boardpassed  # f = board has problems

    def display_board(self, game):
        """ visual display of structures on the board """

        # display discard piles
        print('{0}'.format(game.board.p1))  # use __str__ for no prefix strings
        print('{0}'.format(game.board.p2))
        print('{0}'.format(game.board.p3))
        print('{0}'.format(game.board.p4))

        # display deck
        print(':' + game.board.deck.display_deck() + ':')

        # display stacks
        for i in range(0, game.board.max_stack_size(), 1):
            print("{0} {1} {2} {3} {4} {5} {6}".format(
                game.board.s1.display_card(i),
                game.board.s2.display_card(i),
                game.board.s3.display_card(i),
                game.board.s4.display_card(i),
                game.board.s5.display_card(i),
                game.board.s6.display_card(i),
                game.board.s7.display_card(i)))
        # print("end board")

        return

    def max_stack_size(self):
        """ return max number of cards in any stack """

        maxcount = len(self.s1)  # start with max quess
        for stack in self.stacks:  # loop for each stack
            if maxcount < len(stack):  # capture if this stack has
                # more cards
                maxcount = len(stack)

        return maxcount

    def find_card(self,
                  suit,  # suit of card to look for
                  rank,  # rank or card to look for
                  handname=None):  # match this hand.name if any
        """Find card with suit and rank on the board"""

        # print "Looking for card suit= " + str(suit) + \
        #      " rank= " + str(rank) + " hand= " + str(handname)

        # init card to empty card
        cardnotfound = Card(suit=4,  # 4 == empty suit (no suit yet)
                            rank=0,  # 0 == no rank yet
                            visible=False,  # can't see me now
                            hand=Hand(name="notfound"),  # no known hand yet
                            position=0)  # no position yet

        # loop for no more than max number of card
        for i in range(1):  # 52):  # len(game.originaldeck)):

            # look for card on each board stack, pile, deck
            # return card as soon as found

            for stack in self.stacks:  # loop for each stack
                for card in stack.cards:  # loop for each card

                    # print "1looking at card " + card.name

                    # look for either suit,rank or suit,rank,hand
                    if handname is None:  # match only suit and rank

                        # look only for suit,rank with hand don't care
                        if card.suit == suit and \
                                card.rank == rank:

                            # print "1Found card suit= " + str(card.suit) + \
                            #      " rank= " + str(card.rank) + \
                            #      " hand= " + card.hand.name

                            # found suit,rank
                            return card  # return suit and rank card

                        else:

                            # didn't find suit,rank with hand don't care
                            continue  # keep looking

                    # look for suit,rank and hand
                    elif handname == card.hand.name and \
                            card.suit == suit and \
                            card.rank == rank:

                        # print "2Found card suit= " + str(card.suit) + \
                        #      " rank= " + str(card.rank) + \
                        #      " hand= " + card.hand.name

                        # found suit,rank,hand
                        return card  # return suit, rank, hand card

                    else:

                        # didn't find suit,rank, or hand
                        continue  # keep looking

            for pile in self.piles:  # loop for each suit pile
                for card in pile.cards:  # loop for each card

                    # print "2looking at card " + card.name

                    # look for either suit,rank or suit,rank,hand
                    if handname is None:  # match only suit and rank

                        # look only for suit,rank with hand don't care
                        if card.suit == suit and \
                                card.rank == rank:

                            # print "3Found card suit= " + str(card.suit) + \
                            #      " rank= " + str(card.rank) + \
                            #      " hand= " + card.hand.name

                            # found suit,rank
                            return card  # return suit and rank card

                        else:

                            # didn't find suit,rank with hand don't care
                            continue  # keep looking

                    # look for suit,rank and hand
                    elif handname == card.hand.name and \
                            card.suit == suit and \
                            card.rank == rank:

                        # print "4Found card suit= " + str(card.suit) + \
                        #      " rank= " + str(card.rank) + \
                        #      " hand= " + card.hand.name

                        # found suit,rank,hand
                        return card  # return suit, rank, hand card

                    else:

                        # didn't find suit,rank, or hand
                        continue  # keep looking

            for card in self.deck.cards:  # loop for each card

                # print "3looking at card " + card.name

                # look for either suit,rank or suit,rank,hand
                if handname is None:  # match only suit and rank

                    # look only for suit,rank with hand don't care
                    if card.suit == suit and \
                            card.rank == rank:

                        # print "5Found card suit= " + str(card.suit) + \
                        #      " rank= " + str(card.rank) + \
                        #      " hand= " + card.hand.name

                        # found suit,rank
                        return card  # return suit and rank card

                    else:

                        # didn't find suit,rank with hand don't care
                        continue  # keep looking

                # look for suit,rank and hand
                elif handname == card.hand.name and \
                        card.suit == suit and \
                        card.rank == rank:

                    # print "6Found card suit= " + str(card.suit) + \
                    #      " rank= " + str(card.rank) + \
                    #      " hand= " + card.hand.name

                    # found suit,rank,hand
                    return card  # return suit, rank, hand card

                else:

                    # didn't find suit,rank, or hand
                    continue  # keep looking

        return cardnotfound  # if here then didn't find card

    def list_suits(self):
        """List each card in each suit in box order"""

        suitcardlist = []  # start empty

        # loop for each suit
        #   suits are emnumerated 0..3 (4 suits + blank)
        for suit in range(0, 4):

            # loop for each rank
            for rank in range(1, 14):  # rank is emnumerated 1..14 (13 cards)

                # put into total card list
                suitcardlist.append(self.find_card(suit, rank))

        return suitcardlist  # return list of 52 cards in suit rank order

    def list_visible_cards(self):
        """ return list of all visible cards """

        visiblecardlist = []  # start empty

        for stack in self.stacks:  # loop for each stack
            for card in stack.cards:  # loop for each card
                if card.visible:  # listing only visibles
                    visiblecardlist.append(card)

        for pile in self.piles:  # loop for each suit pile
            for card in pile.cards:  # loop for each card
                if card.visible:  # listing only visibles
                    visiblecardlist.append(card)

        for card in self.deck.cards:  # loop for each card
            if card.visible:  # listing only visibles
                visiblecardlist.append(card)

        return visiblecardlist

    def list_source_cards(self):
        """ list all cards that are movable on the board """
        return self.list_visible_cards()  # same list

    def list_destination_cards(self):
        """ list all cards that are possible desinations on the board """
        destinationcardlist = []  # start empty

        # look for visibles at end of each stack
        for stack in self.stacks:  # look for cards at end of stacks
            if (len(stack) > 0) and \
                    stack.cards[-1].visible:  # listing visibles at end of stack
                destinationcardlist.append(stack.cards[-1])

        # look for destinations in suit piles
        for pile in self.piles:  # look for cards in piles or empty
            if (len(pile) > 0) and \
                    pile.cards[-1].visible:  # listing visibles at end of stack
                destinationcardlist.append(pile.cards[-1])

        return destinationcardlist

    @staticmethod
    def list_moves(sourcecards, destinationcards, moveset):
        """ find and list all moves (source maps to destinations) """

        move = 0  # count each move
        movelist = []  # start empty
        movevalue = 1002  # get move's value from is_card_movable
        # movetree = Tree() # start the tree of moves
        # movetree.create_node("Root", "root", data=Move())
        for source in sourcecards:  # loop checking each source card

            # print source.name

            for dest in destinationcards:  # loop checking each dest card

                # print "   " + dest.name

                movevalue, ismovable = \
                    source.is_card_movable(sourcecard=source,
                                           destinationcard=dest)

                if ismovable:

                    # print source.name + dest.name + \
                    #        " value=" + str(movevalue)

                    # check if already did this move
                    setmove = Move(source, dest, 0, 0)
                    # print "Looking for move in moveset:"
                    # print setmove
                    # print "set contains: "
                    # for i, m in enumerate(moveset):
                    #    print str(i)
                    #    print m
                    if setmove in moveset:
                        # print "already did this move!!"
                        pass
                    else:
                        # print "didnt do that move"
                        move = move + 1  # count this move

                        # movetree.create_node(tag=s.name+dest.name,
                        # identifier=str(move), parent='root',
                        # data=Move(source,dest))

                        # add move to accumulated possible moves
                        movelist.append(Move(source, dest, move, \
                                             movevalue))

        # sort and renumber move list so that
        # higher prio moves (lower value numbers) are listed first
        from operator import itemgetter, attrgetter, methodcaller
        movelist = sorted(movelist, key=attrgetter('movevalue'))  # sort
        for i, move in enumerate(movelist):
            move.movenumber = i + 1  # renumber moves

        # return movetree
        return movelist


class Move(object):
    """ this is an object that contains a single possible move on
        the board """

    def __init__(self,

                 # these are for the current move on the board
                 sourcecard=Card(),  # move this card
                 destinationcard=Card(),  # to this card
                 movenumber=-1,  # move number
                 # (helps the user select
                 # this move)
                 movevalue=2000,  # the lower the value the
                 # higher the prio of this move

                 # these are for undoing this move, if this move is made
                 # where the card ended up
                 #   this will become the source card for undo
                 undosourcecard= \
                         Card(4, 0, False, hand=Hand(name="us")),
                 # the upcard from where the card went to
                 #   this will help reset the top card from where
                 #   the undo source card came from to the premove state
                 undosupcard= \
                         Card(4, 0, False, hand=Hand(name="su")),
                 # where the card came from
                 #   this will become the destination card for undo
                 undodestinationcard= \
                         Card(4, 0, False, hand=Hand(name="ud")),
                 # the upcard from where the card came from
                 #   this will help reset the new destination top card
                 #   to the premove state
                 #   this will help reset the top card to where
                 #   the undo source card went to to the premove state
                 undodupcard= \
                         Card(4, 0, False, hand=Hand(name="du")),

                 # move types needed when undoing
                 wasundone=False,  # t == move was prevously undone by undo
                 # f == move may be normal undo

                 isundo=False,  # t == this is an undo and not available
                 #      to undo again
                 # f == move is normal

                 moveid=0,  # move unique id

                 gamemove=0,  # which game move number
                 # this move is
                 gamestate=None):  # save of game as result of this move

        # this are attributes of a move
        #   this move's source card
        self.sourcecard = sourcecard

        #   this move's destination card
        self.destinationcard = destinationcard

        #   this move's name
        self.name = sourcecard.name + destinationcard.name

        #   a move number for this set of moves
        self.movenumber = movenumber

        #   this move's priority value
        self.movevalue = movevalue

        #   for undo this move
        self.undosourcecard = undosourcecard

        #   for undo this move
        self.undosupcard = undosupcard

        #   for undo this move
        self.undodestinationcard = undodestinationcard

        #   for undo this move
        self.undodupcard = undodupcard

        #   set to true if and when this move is undone by undo
        self.wasundone = wasundone

        #   set to true when this move is an undo move
        self.isundo = isundo

        #   set unique id for this move
        self.moveid = gamemove

        #   which game move number this move was
        self.gamemove = gamemove

        #   save of game as the result of this move (saved after every
        #   card movement move)
        self.gamestate = gamestate

        return

    def __str__(self):
        """ return the string version of a move object """

        movestring = ""

        # print "str"
        # print id(self)
        # print dir(self)
        # print "dir"
        # print self.__dict__

        # create move string for this move to return to caller
        try:
            movestring = \
                self.name + ":" + \
                str(self.movenumber) + ":" + ":" + \
                self.sourcecard.hand.name + ":" + \
                str(self.sourcecard.position) + ":" + \
                self.destinationcard.hand.name + ":" + \
                str(self.destinationcard.position) + \
                ":v=" + str(self.movevalue) + "|" + \
                self.undosourcecard.hand.name + ":" + \
                str(self.undosourcecard.position) + ":" + \
                self.undosupcard.hand.name + ":" + \
                str(self.undosupcard.position) + ":" + \
                str(self.undosupcard.visible) + "|" + \
                self.undodestinationcard.hand.name + ":" + \
                str(self.undodestinationcard.position) + ":" + \
                self.undodupcard.hand.name + ":" + \
                str(self.undodupcard.position) + ":" + \
                str(self.undodupcard.visible) + "|" + \
                str(self.wasundone) + ":" + \
                str(self.isundo) + ":" + \
                str(self.moveid) + ":" + \
                str(self.gamemove)

        except Exception as argument:
            print("Bad move string because " + str(argument))

        return movestring

class CardGame(object):
    """ foundational class of a game containing a board and a deck
        of playing cards """

    def __init__(self,  # this game
                 board=SBoard(),  # type of board
                 deck=Deck(),  # type of deck
                 gamemoves=[],  # list of moves made during this game
                 movescount=0,  # how many moves this game
                 savedgame=False):  # True if this game is savedgame

        # here are the attibutes of a game
        self.board = board  # the game has a board
        # (specialized per card game)
        self.deck = deck  # game has a deck
        self.board.deck = deck  # put the deck onto the board too
        self.gamemoves = gamemoves  # list of which moves played this game
        self.movescount = movescount  # how many moves played this game
        self.moveset = {}  # sanitized moved made during
        # this card game
        self.moveset = set()  # turn it into a set datatype
        self.originaldeck = deck  # either a fresh deck or a saved deck
        self.savedgame = savedgame  # don't deal if already known game
        self.winnable = self.board.check_board_won(self)  # pass in game

        # load savedgame deck else do random deck
        if (not self.savedgame) and \
                (not self.winnable):  # new game from scratch

            self.deck.shuffle()  # random shuffle deck

            # save this shuffled deck in case this game is a winnder
            self.originaldeck = copy.deepcopy(self.deck)

        # if game is saved and is a winner start it fresh
        if self.winnable:  # if a saved winnable then clean the game

            # get original shuffled deck of this saved winning game
            self.deck = copy.deepcopy(self.originaldeck)  # start from saved deck
            self.board.deck = self.deck  # put the deck onto the board too

            # initialize suit piles
            self.board.p1.cards = []  # clear the saved game's pile
            self.board.p2.cards = []  # clear the saved game's pile
            self.board.p3.cards = []  # clear the saved game's pile
            self.board.p4.cards = []  # clear the saved game's pile

            # put non-existing card on suit piles
            #   add a visible empty card to pile
            self.board.p1.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                                   rank=0,  # 0 == no rank yet
                                   visible=True,  # can see me now
                                   hand=self.board.p1,  # this card Hand
                                   position=0))  # no position yet
            self.board.p2.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                                   rank=0,  # 0 == no rank yet
                                   visible=True,  # can see me now
                                   hand=self.board.p2,  # this card Hand
                                   position=0))  # no position yet
            self.board.p3.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                                   rank=0,  # 0 == no rank yet
                                   visible=True,  # can see me now
                                   hand=self.board.p3,  # this card Hand
                                   position=0))  # no position yet
            self.board.p4.add(Card(suit=4,  # 4 == empty suit (no suit yet)
                                   rank=0,  # 0 == no rank yet
                                   visible=True,  # can see me now
                                   hand=self.board.p4,  # this card Hand
                                   position=0))  # no position yet

        # deal only in a new game or cleaned winnable game
        if (not self.savedgame) or self.winnable:
            # deal into the seven stacks(tried to put this into the board())
            #  use custom stack list each time because game deals
            #  one less stack each deal pass
            dpass = [self.board.s1, self.board.s2, self.board.s3,
                     self.board.s4, self.board.s5, self.board.s6, self.board.s7]
            for stack in dpass:
                # clear any residual empty cards from saved game stack
                stack.cards = []  # clear any residual empty cards from saved
                # game stack

                # add an empty card to each stack
                stack.cards.insert(0,
                                   Card(suit=4,  # 4 == empty suit (no suit yet)
                                        rank=0,  # 0 == no rank yet
                                        visible=False,  # can't see me now
                                        hand=stack,  # this card Hand
                                        position=0))  # position at bottom of stack

            # deal into the stacks per the rules of the game
            self.deck.deal(dpass, 7 - 0)  # deal first row of stack card,
            # all stacks

            dpass = [self.board.s2, self.board.s3, self.board.s4,
                     self.board.s5, self.board.s6, self.board.s7]

            self.deck.deal(dpass, 7 - 1)  # deal next row of stack card,
            # but not 1st stack

            dpass = [self.board.s3, self.board.s4,
                     self.board.s5, self.board.s6, self.board.s7]

            self.deck.deal(dpass, 7 - 2)  # deal next row of stack card,
            # but not 1st and 2nd stack

            dpass = [self.board.s4,
                     self.board.s5, self.board.s6, self.board.s7]

            self.deck.deal(dpass, 7 - 3)  # deal next row of stack card

            dpass = [
                self.board.s5, self.board.s6, self.board.s7]
            self.deck.deal(dpass, 7 - 4)  # deal next row of stack card

            dpass = [
                self.board.s6, self.board.s7]
            self.deck.deal(dpass, 7 - 5)  # deal next row of stack card

            dpass = [
                self.board.s7]

            self.deck.deal(dpass, 7 - 6)  # deal next row of stack card,
            # only the last stack

            # make last card in stacks visible
            self.board.s1.cards[-1].visible = True
            self.board.s2.cards[-1].visible = True
            self.board.s3.cards[-1].visible = True
            self.board.s4.cards[-1].visible = True
            self.board.s5.cards[-1].visible = True
            self.board.s6.cards[-1].visible = True
            self.board.s7.cards[-1].visible = True
            if len(self.deck) > 0:
                self.deck.cards[-1].visible = True  # deck card visible

            # when here:
            # 1. should have a freshly dealt board
            #

            # this is an example of how to stack the board
            # to create a card situation to allow debug
            #   realize this can/will break board integrity
            if False:  # True:

                # put a king onto the deck
                self.board.deck.cards[-1] = \
                    Card(suit=0,  # 4 == empty suit (no suit yet)
                         rank=13,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.board.deck,  # this card Hand
                         position=3)  # no position yet

                # put a king onto a stack
                self.board.s2.add(
                    Card(suit=0,  # 4 == empty suit (no suit yet)
                         rank=13,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=self.board.s2,  # this card Hand
                         position=3))  # no position yet

                # clear a stack to allow king moves
                self.board.s1.remove(self.board.s1.cards[-1])
                self.board.s1.cards[-1].visible = True

            return

    def do_unmove(self, move, game):
        """Do a single requested undo move of card(s)"""

        # define user exceptions
        class Error(Exception):
            """Base class for other exceptions"""
            pass

        # define user exceptions
        class Movinganemptystackorpilecard(Error):
            """Raised when moving an empty card (should not happen)"""
            pass

        # define user exceptions
        class Decktostackpileundoshouldneverhappen(Error):
            """Raised when moving an deck card (should not happen)"""
            pass

        # define user exceptions
        class Movinganemptystackcard(Error):
            """Raised when moving an deck card (should not happen)"""
            pass

        # print "doing undo of move: " + str(move)

        # obtain the real card that is on the game.board using
        # the suit and rank of the source card stored into the
        # undo portion of the orginal move
        sourcecard = game.board.find_card(suit=move.undosourcecard.suit,
                                          rank=move.undosourcecard.rank,
                                          handname= \
                                              move.undosourcecard.hand.name)
        scardhand = sourcecard.hand  # save for deleting old card

        destinationcard = game.board.find_card(suit=move.undodupcard.suit,
                                               rank=move.undodupcard.rank,
                                               handname=move.undodupcard.hand.name)

        if False:  # True:
            print("sourcecard " + ":" + \
                  str(sourcecard) + ":" + \
                  sourcecard.hand.name + ":" + \
                  str(sourcecard.position))

            print("destinationcard " + ":" + \
                  str(destinationcard) + ":" + \
                  destinationcard.hand.name + ":" + \
                  str(destinationcard.position))

            print("undosourcecard " + ":" + \
                  str(move.undosourcecard) + ":" + \
                  move.undosourcecard.hand.name + ":" + \
                  str(move.undosourcecard.position) + ":" + \
                  str(move.undosourcecard.suit) + ":" + \
                  str(move.undosourcecard.rank))

            print("undodestinationcard " + ":" + \
                  str(move.undodestinationcard) + ":" + \
                  move.undodestinationcard.hand.name + ":" + \
                  str(move.undodestinationcard.position) + ":" + \
                  str(move.undodestinationcard.suit) + ":" + \
                  str(move.undodestinationcard.rank))

            print("undosupcard " + ":" + \
                  str(move.undosupcard) + ":" + \
                  move.undosupcard.hand.name + ":" + \
                  str(move.undosupcard.position) + ":" + \
                  str(move.undosupcard.visible))

            print("undodupcard " + ":" + \
                  str(move.undodupcard) + ":" + \
                  move.undodupcard.hand.name + ":" + \
                  str(move.undodupcard.position) + ":" + \
                  str(move.undodupcard.visible))

        # undo stack->[stack|pile] moves differently than the other moves
        if (not sourcecard.hand.name == "Deck") and \
                (not destinationcard.hand.name == "Deck"):

            # do a stack->[stack|pile] move
            # print "do a stack->[stack|pile] move"

            if sourcecard.rank == 0:
                raise Movinganemptystackcard

            # turn just uncovered source up card to visiblity it was
            # before the normal move
            sourcecard.hand.cards[move.undosupcard.position].visible = \
                move.undosupcard.visible

            # turn just covered dest up card to visiblity it was
            # before the normal move
            destinationcard.hand.cards[move.undodupcard.position].visible \
                = move.undodupcard.visible

            #     move a substack from sourcecard to end of source hand
            #     to destination hand via slicing
            destinationcard.hand.cards.extend \
                (sourcecard.hand.cards[sourcecard.position:])

            # clear the moved sourcecards from the old source deck
            #    bit bucket (even needed?)
            sourcecard.hand.cards[sourcecard.position:] = []

            # self.reposition the new cards in the destination deck
            for i, card in enumerate(destinationcard.hand.cards):
                # all cards now in destination hand
                card.hand = destinationcard.hand

                # all cards now with position in hand
                card.position = i

        # undo deck to [stack|pile] moves differently than the other
        # board moves
        elif (sourcecard.hand.name == "Deck") and \
                (destinationcard.hand.name != "Deck"):

            # do a deck->[stack|pile] move
            # print "deck to [stack|pile]"

            raise Decktostackpileundoshouldneverhappen

        # undo [stack|pile] to deck moves differently than the other
        # board moves
        elif (sourcecard.hand.name != "Deck") and \
                (destinationcard.hand.name == "Deck"):

            # do a [stack|pile] -> deck move
            # print "[stack|pile] to deck"

            if sourcecard.rank == 0:
                raise Movinganemptystackorpilecard

            # make now top card not visible again as it was before move
            game.deck.cards[-1].visible = False

            # put the original top card (which is now on stack|pile)
            # onto the top again using single card
            game.deck.cards.extend(sourcecard.hand.cards[-1:])

            # make new (original) top card visible again
            # game.deck.cards[-1].visible = True # needed?

            # fixup original card now back on deck
            game.deck.cards[-1].hand = destinationcard.hand
            game.deck.cards[-1].position = move.undodestinationcard.position

            # delete any empty card on bottom of deck because
            # this empty card was added when the original move cause
            # the deck to go empty. This added empty card must
            # be removed now because, once the first card is readded
            # to the deck during unmove this "was empty" added empty
            # card is not longer valid (deck is not empty anymore)
            if (game.deck.cards[0].suit == 4) and \
                    (game.deck.cards[0].rank == 0):
                game.deck.remove(game.deck.cards[0])

            # delete the now old bottom card
            move.undosupcard.hand = scardhand
            move.undosupcard.hand.cards[-1:] = []

            # handle newly uncovered source card's visiblity
            move.undosupcard.hand.cards[-1].visible = move.undosupcard.visible
            # when here:
            # 1. the board is restored to the pre move state

        # undo deck to deck moves differently than the other
        # board moves
        else:

            # do a deck->deck move
            # print "do a deck->deck move"

            # make now top card not visible again as it was before move
            game.deck.cards[-1].visible = False

            # put the original top card (which is now on bottom)
            # onto the top again using slice from pos 0 count of 1
            game.deck.cards.extend(game.deck.cards[0: 1])

            # make new (original) top card visible again
            game.deck.cards[-1].visible = True

            # delete the now old bottom card
            game.deck.cards[0: 1] = []

            # handle any death card added by the orginal dd move
            if move.movevalue < 0:  # this means the death card was added

                # delete the added death card
                # game.deck.remove_death_card() # remove death card if any
                pass

            # reposition the cards in the deck because they shifted
            for i, card in enumerate(game.deck.cards):
                # all cards now with position in hand
                card.position = i

            # when here:
            # 1. the deck is restored to the pre dd state

        # set the move's undone flag
        move.wasundone = True  # set the orginal move to was undone
        # so it is not undoable any more

        # increment game move count
        game.movescount += 1

        # create a new move that will represent the undo move just
        # peformed
        umove = copy.deepcopy(move)  # start with same move
        umove.sourcecard = sourcecard
        umove.destinationcard = destinationcard
        umove.wasundone = False  # an undo move can never be undone
        umove.isundo = True

        # append game move count to move
        umove.gamemove = game.movescount

        # save this new game to the gamemoves (do this before saving this move!)
        # umove.gamestate = copy.deepcopy(game) # copy of state of game right now
        # umove.gamestate.gamemoves = []        # null out saved game moves else
        # many games get saved
        # save only the part of the game that is needed for unmove compare
        umove.gamestate = CardGame(board=SBoard(), deck=Deck(),
                                   gamemoves=[])  # get a new game
        umove.gamestate.board = copy.deepcopy(game.board)  # store current game
        umove.gamestate.deck = []  # don't need this either
        umove.gamestate.movescount = game.movescount

        # append umove to game moves
        game.gamemoves.append(umove)  # list of moves played

        # print "did umove: " + str(game.movescount) + " " + str(umove)

        # When here:
        # 1. the game and board updated back to before the orignal move
        # 2. the game's move count has been incremented due to unmove
        # 3. the game's moves have been adjusted to reflect the undo

        return True  # from do_unmove

    def do_move(self, move, game):
        """Do a single requested source to destination move of card(s)"""

        """Note: there are only three(3) places that move a card:
                 1. do_move()
                 2. do_unmove()
                 3. rotate
        """

        print("doing move: " + str(move))

        # save original cards values (for move.sourcecard restoration)
        #  1 of 2: save source card
        #   what the card is
        savedsourcecard = copy.deepcopy(move.sourcecard)

        ssuit = move.sourcecard.suit  # this card's suit
        srank = move.sourcecard.rank  # this card's number
        svisible = move.sourcecard.visible  # is this card visible or
        # covered on the board?
        sname = move.sourcecard.name  # card's name
        #   where this card is
        shand = move.sourcecard.hand  # which hand is this card in
        sposition = move.sourcecard.position  # which position in the
        # hand this card is in

        #  2 of 2: save destination card
        #   what the card is
        saveddestinationcard = copy.deepcopy(move.destinationcard)

        dsuit = move.destinationcard.suit  # this card's suit
        drank = move.destinationcard.rank  # this card's number
        dvisible = move.destinationcard.visible  # is this card visible or
        # covered on the board?
        dname = move.destinationcard.name  # card's name
        #   where this card is
        dhand = move.destinationcard.hand  # which hand is this
        # card in
        dposition = move.destinationcard.position  # which position in the
        # hand this card is in

        # move the sourcecards to the destination deck
        #     move a substack from sourcecard to end of source hand
        #     to destination hand via slicing
        move.destinationcard.hand.cards.extend \
            (move.sourcecard.hand.cards[move.sourcecard.position:])

        # clear the moved sourcecards from the old source deck
        #    bit bucket (even needed?)
        move.sourcecard.hand.cards[move.sourcecard.position:] = []

        # handle newly uncovered sourcecard in the sourcecard's hand
        #    did hand just get emptied?
        if not move.sourcecard.hand.is_empty():

            # when here we have an stack up card (in orginal condition)
            # save this up card into the move's undo position
            # for later use during the undo move
            move.undodupcard = copy.deepcopy(move.sourcecard.hand.cards[-1])

            # no, source hand not empty yet; just uncover new last card
            #    end of stack is visible
            move.sourcecard.hand.cards[-1].visible = True

        else:  # yes, source hand just got emptied

            # handle sourcecard's hand being emptied by move
            #    added empty to stack or pile
            if move.sourcecard.hand.name != "Deck":

                # add an empty card and make visible
                move.sourcecard.hand.add(
                    Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=move.sourcecard.hand,  # this card Hand
                         position=0))  # no position yet

                # when here we have a new empty stack up card
                # save this up card into the move's undo position
                # for later use during the undo move
                move.undodupcard = \
                    copy.deepcopy(move.sourcecard.hand.cards[-1])

            else:  # added empty to deck (this will act as a death card too)

                # add an empty death card to deck
                # delme move.sourcecard.hand.cards.append(Card(4, 0, False))
                # add an empty death card and make invisible
                move.sourcecard.hand.cards.append(
                    Card(suit=4,  # 4 == empty suit (no suit yet)
                         rank=0,  # 0 == no rank yet
                         visible=True,  # can see me now
                         hand=move.sourcecard.hand,  # this card Hand
                         position=0))  # no position yet

                # when here we have a new empty deck up card
                # save this up card into the move's undo position
                # for later use during the undo move
                move.undodupcard = \
                    copy.deepcopy(move.sourcecard.hand.cards[-1])

        # self.reposition the new cards in the destination deck
        #   note: this action will literally change the .hand and .position
        #         value in each of the sourcecards moved. This renders the
        #         existing move object invalid because the sourcecard in
        #         the move object now has the destination deck and the
        #         original sourcecard.hand and .position values
        #         have been overwitten and lost!
        #         The orginal move object is fixed up later using
        #         the saved values from above.
        for i, card in enumerate(move.destinationcard.hand.cards):
            # all cards now in destination hand
            card.hand = move.destinationcard.hand

            # all cards now with position in hand
            card.position = i

        # save the orginal destination up card into the move's
        # undo source position for later use during the undo move
        move.undosupcard = \
            copy.deepcopy(move.destinationcard.hand.cards[move.sourcecard.position - 1])

        # make any empty card destination not visible once it gets
        # covered else it will look avaialble
        if move.destinationcard.rank == 0:  # this would be a empty card
            # that the sourcecards got
            # moved onto

            # make if invisble because it really does not exist and
            # cannot be played as visible
            move.destinationcard.visible = False

        # make newly covered pile card invisible
        if move.destinationcard.hand.suit != 4:  # suit of 4 means a pile
            move.destinationcard.hand.cards[-2].visible = False

        # when here we did a card move
        # therefore the deck is now fresh again for possible moves
        # so remove the death card and give the deck another chance
        # but don't remove death card/empty card if it is the only
        # card in the deck because a zero length hand/deck list
        # is not a good thing for how this program is designed.
        if (self.deck.cards[0].suit != 4) and (self.deck.cards[0].rank != 0):
            self.deck.remove_death_card()  # give deck another loop through
            # after any move

        # add sanitized move to move set
        setmove = copy.deepcopy(move)
        setmove.movenumber = 0
        setmove.movevalue = 0
        self.moveset.add(setmove)
        # print "adding into set move:"
        # print setmove
        # print self.moveset

        # print originalsourcehand
        # print(move).destinationcard.hand
        # raw_input("moved??")

        # when here the move object now has enough info to complete
        # the undo sourcecard portion of the move
        # the undo source card is where the orig sourcecard ended up
        # on the board
        move.undosourcecard = copy.deepcopy(saveddestinationcard)
        move.undosourcecard.position += 1  # move the card now one more
        # position down the stack

        # when here the undo source card's suit and rank are from
        # the move's destination card. this does not help when doing
        # an undo move therefore change back to orginal source card's id
        move.undosourcecard.suit = ssuit  # restore source card's suit
        move.undosourcecard.rank = srank  # restore source card's rank

        # restore the move's original cards (after the move already made)
        # 1 of 2: restore original sourcecard values (from save above)
        move.sourcecard = savedsourcecard  # replace with orginal card
        #   where this card is
        move.sourcecard.hand = shand  # which hand is this card in
        move.sourcecard.position = sposition  # which position in the hand
        # this card is in

        # 2 of 2: restore original destinationcard values (from save above)
        move.destinationcard = saveddestinationcard  # replace with orginal
        # card
        #   where this card was
        move.destinationcard.hand = dhand  # which hand is this
        # card in
        move.destinationcard.position = dposition  # which position in the
        # hand this card is in

        # the undo destination card is where the orig card came from
        move.undodestinationcard = savedsourcecard

        # set this as a normal move
        move.wasundone = False  # this move not undone by undo yet
        move.isundo = False  # this move is not an undo move

        # increment game move count
        game.movescount += 1

        # create a unique move id
        move.moveid = game.movescount

        # append game move count to move
        move.gamemove = game.movescount

        # save this new game to the gamemoves (do this before saving this move!)
        # move.gamestate = copy.deepcopy(game) # copy of state of game right now
        # move.gamestate.gamemoves = []        # null out saved game moves else
        #                                     # many games get saved
        # save only the part of the game that is needed for move compare
        move.gamestate = CardGame(board=SBoard(), deck=Deck(),  # get a new game
                                  gamemoves=[])  # get a new game
        move.gamestate.board = copy.deepcopy(game.board)  # store current game
        move.gamestate.deck = []  # don't need this either
        move.gamestate.moveid = move.moveid  # save this move's id
        move.gamestate.movescount = game.movescount  # save this move's count

        # save this move into the game's list of moves
        game.gamemoves.append(move)  # list of moves played

        # print "did move: " + str(game.movescount) + " " + str(move)

        # When here:
        # 1. the game and board updated with the orignal move
        # 2. the move object has been restored to orignal move
        # 3. the move object contains enough info to accomplish an
        #    undo move

        return True  # from do_move

    @classmethod
    def play(self, game, command=""):
        # type: (object, object) -> object
        """ this is the primary way to start playing a game. """

        # print("playing")
        # while not self.deck.is_empty():
        #    self.board.p1.add (self.deck.cards[0])
        #    self.deck.remove(self.deck.cards[0])

        # this is the tournament -> game -> PLAY command loop
        class Playshell(cmd.Cmd):
            """Game playing command processor."""
            intro = \
                'Start playing the game. Type help or ? to list commands.\n'
            prompt = 'play> '

            def preloop(self):
                """Do this when cmdloop() starts."""

                # handle any auto-commands for this cmdloop run

                #  handle any auto-commands set by the game (ag)
                global PLAY_COMMAND_QUEUE  # auto-commanding when needed
                self.cmdqueue = PLAY_COMMAND_QUEUE  # do any auto-comments

                #  set any auto-command we want the nex cmploop to run
                pass

                # Print board 1st time into playing loop
                self.display_board(game)

                return False  # continue command loop

            @classmethod
            def do_pass(self, arg):
                """Do nothing command"""
                print("Doing nothing!")
                return False  # continue command loop

            @classmethod
            def do_ci(self, arg):
                """Check integrity of board (program debug)"""
                'ci: CHECK INTEGRITY'
                if not game.board.check_board_integrity(self):  # pass in game
                    print("Board did not pass!")
                else:
                    print("Board passed!")
                return False  # continue command loop

            @classmethod
            def do_lm(self, arg):
                """List how many moves made in this game"""
                'lm: LIST NUMBER OF MOVES MADE'

                print("We made " + str(game.movescount) + " moves.")

                return False  # continue command loop

            @classmethod
            def do_llow(self, arg):
                """List low cards in each suit"""
                'llow: LIST LOW CARDS IN SUITS'

                # clubs (black suit)
                clublow1card, \
                clublow2card, \
                clublowlow = game.board.check_suit_lowlow_condition(
                    game=game, suit=0)

                # diamonds (red suit)
                diamondlow1card, \
                diamondlow2card, \
                diamondlowlow = game.board.check_suit_lowlow_condition(
                    game=game, suit=1)

                # hearts (red suit)
                heartlow1card, \
                heartlow2card, \
                heartlowlow = game.board.check_suit_lowlow_condition(
                    game=game, suit=2)

                # spades (black suit)
                spadelow1card, \
                spadelow2card, \
                spadelowlow = game.board.check_suit_lowlow_condition(
                    game=game, suit=3)

                # print in color order
                print(clublow1card + clublow2card)
                print(spadelow1card + spadelow2card)
                print(diamondlow1card + diamondlow2card)
                print(heartlow1card + heartlow2card)

            @classmethod
            def do_lsuits(self, arg):
                """List cards in each suit"""
                'lsuits: LIST CARD IN SUITs'

                cardlist = game.board.list_suits()

                line = ""
                suit = 0
                for rank in range(0, 13):
                    line += str(cardlist[(suit * 13) + rank])
                clubs = line

                line = ""
                suit += 1
                for rank in range(0, 13):
                    line += str(cardlist[(suit * 13) + rank])
                diamonds = line

                line = ""
                suit += 1
                for rank in range(0, 13):
                    line += str(cardlist[(suit * 13) + rank])
                hearts = line

                line = ""
                suit += 1
                for rank in range(0, 13):
                    line += str(cardlist[(suit * 13) + rank])
                spades = line

                # print in color order
                print(clubs)
                print(spades)
                print(diamonds)
                print(hearts)

            @classmethod
            def do_ld(self, arg):
                """List destination cards on the board (program debug)"""
                'lv: LIST DESTINATION CARDS'
                print(','.join(card.name
                               for card in game.board.list_destination_cards()))
                return False  # continue command loop

            @classmethod
            def do_lv(self, arg):
                """List visible cards on the board (program debug)"""
                'lv: LIST VISIBLE CARDS'
                print(','.join(card.name
                               for card in game.board.list_visible_cards()))
                return False  # continue command loop

            @classmethod
            def do_ls(self, arg):
                """List source cards (program debug)"""
                'ls: LIST SOURCE CARDS'
                print(','.join(card.name
                               for card in game.board.list_source_cards()))
                return False  # continue command loop

            def do_exit(self, arg):
                """Exit playing"""
                'exit:   EXIT'
                # print("Thanks for playing!")
                self.close()
                return True  # exit command loop

            @classmethod
            def close(self):
                """ close """
                pass

            @classmethod
            def postloop(self):
                """Print playing command loop goodbye"""
                # print "exiting playing command loop"
                print("We played " + str(game.movescount) + " moves.")
                if game.movescount < 300:
                    for i, move in enumerate(game.gamemoves):
                        # print i, "  ", move
                        pass
                return True  # exit play command loop

            @classmethod
            def postcmd(self, stop, line):
                """Display board after each command"""

                skip = ['?', 'ci', 'db', 'exit',
                        'help', 'ld', 'lgm', 'llow',
                        'lm', 'ls', 'lsuits', 'lv', 'm', 'mm',
                        'pass']
                if "help" in line:  # condition help command line
                    line = "help"

                # display board after some commends
                if ((not stop) and  # no display on exit
                        (line not in skip)):  # not a helper command
                    self.display_board(game)  # then display board

                return stop  # may continue or may be an exit command

            @classmethod
            def do_lgm(self, arg):
                """List game moves (moves made)"""
                'lgm: LIST MOVES MADE'

                print("We played " + str(game.movescount) + " moves.")
                for i, move in enumerate(game.gamemoves):
                    print((i), "  ", move)
                return False  # continue command loop

            @classmethod
            def do_db(self, arg):
                """Display board"""
                'db: DISPLAY BOARD'
                game.board.display_board(game)  # pass in game to get access
                # to the deck
                return False  # continue command loop

            @classmethod
            def do_dd(self, arg):
                """Deal card from deck"""
                'dd: DEAL FROM DECK'

                # get a new playing card from deck
                if not game.deck.rotate(game):
                    # When here:
                    # deck rotation returned a death card meaning
                    # all the deck cards have been checked for moves
                    #
                    # This means special techniques are needed to
                    # determine if game is winnable.
                    # For example: walking up the ladder

                    print("Uh oh End of Game?")

                    # try some special techniques here

                    # check to see if walking up the ladder is possible
                    # by checking if board is in a lowlow condition
                    blacks, \
                    reds = game.board.check_board_lowlow_condition(game)

                    # display how many suits in lowlow
                    # this might help determine if walking up ladder
                    # is possible
                    print(str(blacks) + " black  " + \
                          str(reds) + " red suits in lowlow")

                return False  # continue command loop

            @classmethod
            def do_u(self, arg):
                """Undo moves"""
                'u: UNDO MOVES'

                # travel game moves until an undoable move found
                candidatemove = None
                for candidatemove in reversed(game.gamemoves):

                    # check an undoable move
                    if (not candidatemove.wasundone) and \
                            (not candidatemove.isundo) and \
                            (candidatemove.moveid != 0):  # move 0 is not playable
                        # we found the next move to undo
                        break
                    else:
                        # this candidatemove is not undoable because
                        # it is was either already undone or
                        # is an undo move itself or
                        # it is the 0th move which is not a real
                        #   move- it just contains the original game
                        candidatemove = None  # mark this move ineligable

                # go do the undo move if found one
                # else display no undo available message and return
                if candidatemove is not None:

                    # print "candidatemove = " + str(candidatemove)

                    # find game of previous move because this is the
                    # game to compare after undoing candidate move
                    #  think about it!

                    # travel up from candidatemove to find previous move
                    premove = game.gamemoves[0]  # defaulf to original game
                    for ipremove in range((candidatemove.gamemove - 1),
                                          -1, -1):

                        if False:  # True:
                            print("undbg" + str(ipremove) + " " + \
                                  str(game.gamemoves[ipremove]))

                            if game.gamemoves[ipremove].wasundone:
                                print("was undone")

                            if game.gamemoves[ipremove].isundo:
                                print("is undo")

                            if game.gamemoves[ipremove].moveid == 0:
                                print("is original game")

                        # skip over undoable moves
                        if (game.gamemoves[ipremove].wasundone) or \
                                (game.gamemoves[ipremove].isundo) or \
                                (game.gamemoves[ipremove].moveid == 0):

                            # this premove is undoable anyway
                            continue  # keep looking for a doable premove

                        else:

                            # we found the previous move
                            #  this is the next one up from the candidatemove
                            premove = game.gamemoves[ipremove]
                            break  # leave ipremove loop because we found it

                    if False:  # True:
                        print("vvvvvvvvvvvvvvvvv board before undo")

                        print("pre move = " + str(premove))
                        print("un  move = " + str(candidatemove))

                        self.do_db(arg="")
                        game.board.check_board_integrity(game)  # pass in game
                        print("^^^^^^^^^^^^^^^^^ board before undo")

                    # perform the unmove
                    game.do_unmove(move=candidatemove,  # peform move
                                   game=game)  # need game board

                    # check for integrity after an undo
                    # print "vvvvvvvvvvvvvvvvvvvvv board after undo"
                    # self.do_db(arg="")
                    if not game.board.check_board_integrity(game):
                        return True  # True means board failed integrity check

                    # check this new game (just unmoved) against the game
                    # saved after the orginal move
                    if not game.board.compare_games(game,  # this game right now
                                                    premove):  # original game
                        return True  # True means board failed compare check
                    # print "^^^^^^^^^^^^^^^^^^^^^ board after undo"

                else:
                    print("No undo moves available")

                return False  # continue command loop

            @classmethod
            def do_ua(self, arg):
                """Undo all moves"""
                'ua: UNDO ALL MOVES'

                # travel all current game moves until all undone
                for candidatemove in reversed(game.gamemoves):

                    # this will select the next undoable move
                    # and undo it
                    if self.do_u(arg=""):
                        return True  # exit command loop

                return False  # continue command loop

            @classmethod
            def do_m(self, arg):
                """Show priority moves on board"""
                'm: SHOW MOVES'

                # get available moves on board
                branches, moves = self.get_moves(game)

                # display moves
                if len(moves) > 0:  # we have some moves to display

                    movedisplayed = False  # display help message or not

                    for move in moves:
                        if move.movevalue < 1000:
                            print(move)
                            movedisplayed = True  # no help needed

                    if not movedisplayed:
                        print("No useful moves. Try dd or mm.")

                else:  # no moves show hint

                    print("No moves. Try dd.")

                return False  # continue command loop

            @classmethod
            def do_mm(self, arg):
                """Show all moves on board"""
                'mm: SHOW ALL MOVES'

                # get available moves on board
                branches, moves = self.get_moves(game)

                # display moves
                if len(moves) > 0:  # we have some moves to display

                    for move in moves:
                        if True:  # match structure of do_m above
                            print(move)

                else:  # no moves show hint

                    print("No moves. Try dd.")

                return False  # continue command loop

            @classmethod
            def do_p(self, arg):
                """Play a move: p n where n is from m command"""
                'p n: PLAY MOVE N'

                """This command is written to assume that the user
                   does a 'm' to see the available moves then does
                   a 'p n' to play one of those moves.
                   However this routine gets a whole new move list.
                   This means that the user can only do a single
                   'p n' because this routine gets a new move list
                   and that makes the moves displayed by the 'm'
                   command obsolete.
                   I know a user that would like to do a 'p 1' and
                   then a 'p 2' but doing that probably will not
                   execute the 'm''s move #2 because the 'p 2' re-gens
                   the move list.
                """

                # allow command line 'p' to mean 'p [1|a]' shortcut
                if len(arg) == len(""):  # no n on command line
                    movenumber = 1  # a single p command is move #1

                # check for p's command line argument
                else:  # if there is an n arg try to convert to move number

                    # try to convert to integer command number
                    try:
                        # allow character shortcuts due to phone
                        # terminal alpha to numeric switching
                        if arg[0] == 'a':
                            movenumber = 1
                        elif arg[0] == 'b':
                            movenumber = 2
                        elif arg[0] == 'c':
                            movenumber = 3
                        elif arg[0] == 'd':
                            movenumber = 4
                        elif arg[0] == 'e':
                            movenumber = 5
                        elif arg[0] == 'f':
                            movenumber = 6
                        elif arg[0] == 'g':
                            movenumber = 7
                        elif arg[0] == 'h':
                            movenumber = 8
                        elif arg[0] == 'i':
                            movenumber = 9
                        else:
                            movenumber = int(arg[0:])  # convert real n argument
                    except Exception:
                        print("need a move numnber  try m then p n")
                        return False  # keep command looping

                # when here:
                # movenumber should contain integer user selected move to do

                # get available moves on board
                branches, moves = self.get_moves(game)  # get new move list

                # play move n from list of moves
                for move in moves:
                    if movenumber == move.movenumber:  # play this selected move
                        game.do_move(move, game)  # perform move

                        # when here:
                        # 1. game updated to that move
                        # 2. the move just played, and the resulting game
                        #    have been saved to the list of gamemoves

                    continue  # loop until select move is played

                # when here:
                # if 'n' was found in the move list then
                # the move should have been made
                # else no move made

                # check for won game after this move
                if game.board.check_board_won(game):  # pass in game
                    print("Board won! " + str(game.movescount))
                    game.winnable = True

                return False  # continue command loop

            @classmethod
            def do_a(self, arg):
                """Autoplay a game"""
                'a: AUTOPLAY GAME'

                playing = True
                while playing:  # autoplay until board wins or gets stuck

                    # get available moves on board
                    branches, moves = self.get_moves(game)

                    movesmade = game.movescount  # how many moves made
                    # this round?

                    # select moves to play
                    # This loop causes the computer to play the highest
                    # prio move on the board.
                    #
                    # Moves are prioritized by a move value where
                    # the lowest values are the highest priority moves.
                    # As of now ;) the prio values are 100 <= value <= 1000
                    # where the 1000 prio's are really the special moves
                    # that need to be made during special processing like
                    # walking up the ladder.
                    # So this loop is limited to considering prios
                    # 100 <= value < 1000 meaning the 1000 prio moves
                    # will not be made by this loop.
                    #
                    # See the special processing code below that might
                    # exists ;) that could use the 1000 prio moves.
                    #
                    didmove = False  # loop until highest prio move made
                    #    loop low to high priority
                    for prio in range(100, (1000 - 100), 100):

                        # loop all available moves doing only one of prio
                        for move in moves:
                            # print(move)
                            if move.movevalue < (prio + 1):
                                game.do_move(move, game)  # perform move

                                didmove = True  # indicate a move made this
                                # prio
                                break  # break from for once a move is made

                        if didmove:  # if did move(s) at this prio
                            break  # break out; else loop at next
                            # lower prio

                    # if here then either:
                    # 1. a highest available prio move was made
                    #    (and inc move count)
                    # or
                    # 2. no move was made (no inc move count was made)

                    # deal from deck if no moves on board
                    if movesmade == game.movescount:  # deal from deck
                        # if no moves made
                        # just now

                        # get a new playing card from deck by rotating deck
                        playing = game.deck.rotate(game)

                        if not playing:  # out of moves?

                            print("Uh oh End of Game?")
                            playing = False

                            # try some special techniques here

                            # check to see if walking up the ladder
                            # is possible by checking if board is in
                            # a lowlow condition
                            blacks, \
                            reds = \
                                game.board.check_board_lowlow_condition(game)

                            # display how many suits in lowlow
                            # this might help determine if walking up
                            # ladder is possible
                            print(str(blacks) + " black  " + \
                                  str(reds) + " red suits in lowlow")

                            break  # exit autoplaying while loop

                        else:
                            # print "dealt from deck"
                            pass  # play again with new deck card visible

                    # terminate endless game  (darn sets!)
                    if game.movescount > 300:  # abandon this game
                        playing = False
                        break  # exit autoplaying while loop

                    game.board.display_board(game)  # pass in game to get
                    # access to the deck

                    print("^^^^^^^ " + str(game.movescount) + " ^^^^^^^")

                    # check for program logic error
                    #  this will fail if mutiple moves allowed before
                    #  recalculating moves
                    if not game.board.check_board_integrity(self):
                        # game.board.display_board(self) # pass in game
                        # to get access to
                        # the deck
                        print("Board did not pass!")
                        playing = False
                        break  # exit autoplaying while loop

                    # check for won game
                    if game.board.check_board_won(game):  # pass in game
                        # game.board.display_board(game) # pass in game to get
                        # access to the deck
                        print("Board won! " + str(game.movescount))
                        playing = False

                        # print "saving move" + str(game.gamemoves[0])
                        # save this winning game
                        game.winningmoves = game.gamemoves
                        game.savedgame = True
                        game.winnable = True

                        # save a winning game, or not
                        if False:  # True: # False:

                            # store game to file
                            filehandler = open("winner", 'w')

                            # serialize game to file
                            pickle.dump(game, filehandler)
                            filehandler.close()

                        # filehandler = open(filename, 'r')
                        # object = pickle.load(filehandler)
                        break  # exit autoplaying while loop

                    # when here:
                    # 1. a move or rotate deck move has been made
                    #    so go play to play another move
                    # 2. else we'd have broken out of the play loop
                    #    for some other reason

                # end of playing while loop

                # when here:
                # 1. the autoplay loop has finished for some reason
                #    a. game won
                #    b. endless game
                #    c. board integrity check failed

                return False  # continue command loop

            @classmethod
            def display_board(self, game):
                """Display board"""
                game.board.display_board(game)  # pass in game to get access
                # to the deck
                return False  # continue command loop

            @classmethod
            def get_moves(self, game):
                """Get list of available moves on board"""

                # get movable cards
                sourcecards = game.board.list_source_cards()
                # get possible destinations
                destinationcards = game.board.list_destination_cards()

                # find possible moves
                moves = \
                    game.board.list_moves(sourcecards=sourcecards,
                                          destinationcards=destinationcards,
                                          moveset=game.moveset)

                # determine the number of game trees represented by
                # this move set
                sourcecarddict = {}  # start empty with seen source cards
                for move in moves:

                    # for now only count trees in prio moves
                    if move.movevalue < 1000:

                        # tally if this sourcecard seen in moves already
                        try:

                            # increment source card count in dict if card
                            # already seen
                            sourcecarddict[move.sourcecard.name] += 1

                        except Exception:

                            # first time source card is seen
                            sourcecarddict[move.sourcecard.name] = 1

                # When here:
                # the dict should have each sourcecard as a key
                # and the count of how many times that source card
                # showed up in a move
                # print sourcecarddict
                numbranches = 0  # how many tree branches on the board now?
                for name, number in sourcecarddict.items():
                    # print('{0} seen {1} times'.format(name, number))
                    numbranches += number

                return numbranches, moves

            # save current game to file
            def do_sg(self, arg):
                """Save Current Game"""
                'SG: SAVE GAME'

                # get saved game file name from user
                filename = raw_input("file name> ")  # type: str

                # try to open the file
                try:
                   filehandler = open(filename, 'w')
                except IOError:
                    print \
                        ("Unable to open the file " + filename + ", try again")
                    return False  # keep command looping

                # try to save the game
                try:

                    # save this game
                    game.winningmoves = game.gamemoves
                    game.savedgame = True

                    # check for won game for proper .winnable setting
                    if game.board.check_board_won(game):  # pass in game
                        # needs to be true if won for reload playing
                        game.winnable = True
                    else:
                        game.winnable = False

                    # serialize game to file
                    pickle.dump(game, filehandler)

                    filehandler.close()

                except Exception:
                    print("Unable to save game, try again")
                    return False  # keep command looping

                else:
                    print("Saved game: " + filename)

        # when here:
        # the user selected the 'play' command from the 'game>' command
        # loop

        # allow user to play this game using 'play>' command loop
        Playshell().cmdloop()

        # when here:
        # 1. we have exited the 'play>' Playshell command loop
        #
        # we are done playing this game
        # return to outer game> command loop

        return True  # return from playing this game


# this is the tournament -> GAME -> play command loop
class Gameshell(cmd.Cmd):
    """Game selector command processor."""
    intro = \
        'Welcome to the Game shell. Type help or ? to list commands.\n'

    prompt = 'game> '

    def preloop(self):
        """Do this when cmdloop() starts."""

        # handle any auto-commands for this cmdloop run

        #  handle any auto-commands set by the tournament (ag)
        global GAME_COMMAND_QUEUE  # auto-commanding when needed
        self.cmdqueue = GAME_COMMAND_QUEUE  # do any auto-comments

        return False  # continue command loop

    def do_pass(self, arg):
        """Do nothing command"""
        print("Doing nothing!")
        return False  # continue command loop

    def do_status(self, arg):
        """Display status of the game"""

        won = 'No game yet. Try ng...'  # type: str

        try:
            if self.game.winnable:
                won = 'Game Won!'
            else:
                won = 'Game not won yet...'  # type: str
        except:
            pass

        print(won)

        return False  # continue command loop

    def do_ng(self, arg):
        """Play new manual game"""
        self.game = CardGame(
            board=SBoard(),  # create game with specific board
            deck=Deck(),
            gamemoves=[]
            # use defaults for all other game attributes
        )  # create game with a deck

        # save game creation 'move' to the list of game moves
        self.game.gamemoves.append(
            Move(sourcecard=Card(hand=Hand(name="OriginalGame")),
                 destinationcard=Card(hand=Hand(name="OriginalGame")),
                 gamestate=copy.deepcopy(self.game)))

        self.game.play(self.game, command="")

        return False  # continue command loop

    def do_rg(self, arg):
        """Resume current game"""

        try:
            s = 'Resuming game play...'  # type: str
            print(s)  # print now because ...play() is a command loop
            self.game.play(self.game, command="")
        except:
            s = 'No game yet. Try ng...'  # type: str
            print(s)

        return False  # continue command loop

    def do_psg(self, arg):
        """Play saved game"""
        'PSG: PLAY SAVED GAME'

        class Openfile(cmd.Cmd):
            """Open saved game"""
            intro = \
                'Open and play a saved game. Type help or ? to list commands.\n'
            prompt = 'file> '

            def close(self):
                """ close """
                pass

            def do_exit(self, arg):
                """Exit saved game command loop"""
                'exit:   EXIT'
                self.close()
                return True  # exit command loop

            @staticmethod
            def do_dir(arg):
                """List contents of current directory"""
                import os
                print([os.path.join(os.getcwd(), f) \
                       for f in os.listdir(os.getcwd())])
                return False  # continue loop

            # get saved game file name from user
            def do_open(self, arg):
                """Enter saved game filename"""

                # get saved game file name from user
                filename = raw_input("file name> ")

                # try to open the file
                try:
                    filehandler = open(filename, 'r')
                except IOError:
                    print("The file does not exist, try again")
                    return False  # keep command looping

                # try to read the save(d game
                try:
                    self.savedgame = pickle.load(filehandler)
                except Exception:
                    print("Error reading the saved game, try again")
                    return False  # keep command looping
                else:
                    print("Loaded game from " + filename)
                    print("now try play")

                filehandler.close()

            # play saved game
            def do_play(self, arg):
                """Play saved game"""
                'play: PLAY SAVED GAME'

                # which deck to use for saved game?
                if self.savedgame.winnable:
                    # use orignal shuffled deck
                    thisdeck = self.savedgame.originaldeck

                else:
                    # use the saved deck (in process deck)
                    thisdeck = self.savedgame.deck

                # load the saved game
                try:
                    self.game = \
                        CardGame(board=self.savedgame.board,
                                 deck=thisdeck,
                                 gamemoves=self.savedgame.gamemoves,
                                 movescount=self.savedgame.movescount,
                                 savedgame=self.savedgame.savedgame)
                except Exception:
                    print("No game loaded. Try open first")
                    print("Unexpected error:", sys.exc_info()[0])
                    return False  # continue command loop

                # print "game.savedgame", str(self.game.savedgame)
                self.game.play(self.game, command="")

                return True  # exit saved game command loop

        # do saved game command loop
        Openfile().cmdloop()
        return False

    def do_exit(self, arg):
        """Exit game"""
        'exit:   EXIT'
        # print("Thanks for playing!")
        self.close()
        return True  # exit command loop

    def close(self):
        """ close """
        pass

    def postloop(self):
        # print "exiting game command loop"
        pass


# this is the TOURNAMENT -> game -> play command loop
class Tournamentshell(cmd.Cmd):
    """Tournament selector command processor."""

    intro = \
        'Welcome to the Tournament shell. Type help or ? to list commands.\n'
    prompt = 'tournament> '

    def preloop(self):
        """Do this when cmdloop() starts."""

        # handle any auto-commands for this cmdloop run
        global TOURNAMENT_COMMAND_QUEUE  # auto-commanding when needed
        self.cmdqueue = TOURNAMENT_COMMAND_QUEUE  # do any auto-commanding
        return False  # continue command loop

    @staticmethod
    def do_pass(arg):
        """Do nothing command"""
        print("Doing nothing!")
        return False  # continue command loop

    @staticmethod
    def do_mg(arg):
        """Play a manual game"""
        'mg: PLAY MANUAL GAME'

        # set the command the game cmdloop() needs to do for manual game
        global GAME_COMMAND_QUEUE
        GAME_COMMAND_QUEUE = []  # no auto-commands needed for manual game

        global PLAY_COMMAND_QUEUE
        PLAY_COMMAND_QUEUE = []  # no auto-commands needed for manual game

        # play the game with auto-commands set (if any)
        Gameshell().cmdloop()  # enter game command loop

        return False  # continue command loop

    @staticmethod
    def do_ag(arg):
        """Play automated games"""
        'ag: PLAY AUTOMATED GAMES'

        """ This autoplaying works by taking advantange of the command
            loop's capability to run pre-queued command-line command
            upon entry into the command loop. The pre-queued commands
            are the same as the manual user would do to play a game
            but are just now executed automatically. """

        # loop for a lot of game
        for i in range(1, ((1000 * 500) + 1)):
            # set the command the game cmdloop() needs to do for auto-game
            global GAME_COMMAND_QUEUE
            GAME_COMMAND_QUEUE = ["? ng", "ng",  # do a new game
                                  # in game cmdloop
                                  "status",
                                  "? exit", "exit"]  # do these as part of
            # auto games

            global PLAY_COMMAND_QUEUE  # auto-commanding when needed
            PLAY_COMMAND_QUEUE = ["help a", "a",  # auto-play
                                  "help lm", "lm",
                                  "help llow", "llow",
                                  "help lsuits", "lsuits",
                                  "help ua", "ua",
                                  "help exit", "exit"]  # auto-game commands

            # play the game with auto-commands set
            #  use the game command queue to start a new game
            #  then use the play command queue to auto-play that game
            Gameshell().cmdloop()  # enter game command loop

            global GAMES_WON_COUNT
            winpercent = (GAMES_WON_COUNT / (i * 1.0)) * 100

            print("                                       Game #" + \
                  str(i) + " Won " + str(GAMES_WON_COUNT) + " " + \
                  str(winpercent) + "%")

        return False  # continue command loop

    def do_xpsg(self, arg):
        """Play saved game"""
        'PSG: PLAY SAVED GAME'

        class Openfile(cmd.Cmd):
            """Open saved game"""
            intro = \
                'Open and play a saved game. Type help or ? to list commands.\n'
            prompt = 'file> '

            def close(self):
                """ close """
                pass

            def do_exit(self, arg):
                """Exit saved game command loop"""
                'exit:   EXIT'
                self.close()
                return True  # exit command loop

            @staticmethod
            def do_dir(arg):
                """List contents of current directory"""
                import os
                print([os.path.join(os.getcwd(), f)
                       for f in os.listdir(os.getcwd())])
                return False  # continue loop

            # get saved game file name from user
            def do_open(self, arg):
                """Enter saved game filename"""

                # get saved game file name from user
                filename = raw_input("file name> ")

                # try to open the file
                try:
                    filehandler = open(filename, 'r')
                except IOError:
                    print("The file does not exist, try again")
                    return False  # keep command looping

                # try to read the saved game
                try:
                    self.savedgame = pickle.load(filehandler)
                except Exception:
                    print("Error reading the saved game, try again")
                    return False  # keep command looping
                else:
                    print("Loaded game from " + filename)
                    print("now try play")

                filehandler.close()

            # play saved game
            def do_play(self, arg):
                """Play saved game"""
                'play: PLAY SAVED GAME'

                # which deck to use for saved game?
                if self.savedgame.winnable:
                    # use orignal shuffled deck
                    thisdeck = self.savedgame.originaldeck

                else:
                    # use the saved deck (in process deck)
                    thisdeck = self.savedgame.deck

                # load the saved game
                try:
                    self.game = \
                        CardGame(board=self.savedgame.board,
                                 deck=thisdeck,
                                 gamemoves=self.savedgame.gamemoves,
                                 movescount=self.savedgame.movescount,
                                 savedgame=self.savedgame.savedgame)

                except Exception:

                    print("No game loaded. Try open first")
                    # print("Unexpected error:", sys.exc_info()[0])

                    return False  # continue command loop

                # print "game.savedgame", str(self.game.savedgame)
                self.game.play(self.game, command="")

                return True  # exit saved game command loop

        # do saved game command loop
        Openfile().cmdloop()
        return False

    def do_hint(self, arg):
        """Provide hint on how to play this game"""
        'hint:   HINT'
        print("To play a manual game:")
        print("tournament> mg")
        print("game> ng")
        print("play> m")
        print("play> p")
        print("")
        print("To play an automatic game:")
        print("tournament> mg")
        print("game> ng")
        print("play> a")

        return False

    def do_exit(self, arg):
        """Exit program"""
        'exit:   EXIT'
        print("Thanks for playing!")
        self.close()
        return True  # exit command loop

    def close(self):
        """ close """
        pass

    def postloop(self):
        """ do this after command loop exits """
        # print "exiting tournament command loop"
        pass

    def do_about(self, arg):
        """Provide version information"""
        'about:   ABOUT'
        global VERSION_STRING
        print("Version: " + VERSION_STRING)

        return False

    def do_exit(self, arg):
        """Exit program"""
        'exit:   EXIT'

        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod()

# run the outer most program's command loop
TOURNAMENT_COMMAND_QUEUE = []  # auto-commanding when needed
# TOURNAMENT_COMMAND_QUEUE = ["help ag", "ag", "exit"]
Tournamentshell().cmdloop()  # top level command loop
sys.exit()  # exit program
