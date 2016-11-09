from random import random


class Card(object):
    suit_names = ["club", "Diamond", "Spade", "Heart"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=int(random(4)), value=int(random(13))):
        self.suit = suit % 4
        self.rank = value % 13 + 1

    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank], Card.suit_names[self.suit])

    def __cmp__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)
