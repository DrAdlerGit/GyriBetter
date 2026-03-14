from tape import Tape
from interpreter import _throw

class Range:
    def __init__(self, head: tuple, tail: tuple, tape: Tape, interpreterIndex: int):
        """
        Creates a custom type called the 'Range'. A range is a 1D or 2D ordered group of cell values. It is defined by the <head> and <tail> coordinates.
        Internally, a range is a list of the values of the cells inside the head-tail pair. It is ordered X first, and 2D ranges either go up (Y+) or down (Y-)
        based off if the head is lower or higher than the tail respectively. Ranges cannot be easily stored in a integer/cellvalue and are temporary.
        """
        self.head = head
        self.tail = tail

        self.direction = ""
        self.twoDimensional: bool

        if self.head == self.tail:
            _throw("Error creating range: head coordinate cannot be the same as tail", interpreterIndex) 
        
        if head[0] == tail[0] and head[1] != tail[1]:
            self.twoDimensional = False

            if head[1] > tail[1]:
                self.direction = "down"
            else:
                self.direction = "up"
        
        elif head[0] != tail[0] and head[1] == tail[1]:
            self.twoDimensional = False

            if head[0] > tail[0]:
                self.direction = "left"
            else:
                self.direction = "right"
        
        else:
            self.twoDimensional = True

            if head[1] > tail[1]:
                self.direction = "down"
            else:
                self.direction = "up"
        
        self.values = []

                
