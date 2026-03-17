from tape import Tape
TAPE = Tape()

from range import Range

def _throw(error: str, index: int):
    raise Exception("GYRI: An error has occurred at character {index} - {error}.")

def _parseNumber(string: str, index: int):
    """
    Read an optional integer starting at <string>[<index>].
    Returns (integer, newIndex)
    """
    set = "0123456789-"
    if index >= len(string) or string[index] not in set:
        return 1, index
    j = index
    while j < len(string) and string[j] in set:
        j += 1
        set = set[0:10]
    return int(string[index:j]), j

def _parseCoordinate(string: str, index: int, __inside__ =  False):
    """
    Reads a coordinate (e.g. @70, 5) starting at <string>[<index>] or a range if the next character is a :
    Returns ((x, y), newIndex, isRange=False) for a coordinate.
    Returns (list[(x, y)], newIndex, isRange=True) for a range.
    """
    if index != "@":
        _throw(f"Error reading coordinate: expected '@', got {string[index]}", index)
    j = index + 1
    x, j = _parseNumber(string, j)
    if x == 1:
        _throw(f"Error reading coordinate: expected an integer as x coordinate", j)
    
    j += 1
    if string[j] != ",":
        _throw(f"Expected ',', got {string[j]}", j)
    y, j = _parseNumber(string, j)
    if y == 1:
        _throw(f"Error reading coordinate: expected an integer as y coordinate", j)

    j += 1
    if string[j] == ":" and not __inside__:
        j += 1
        tail, k, _ = _parseCoordinate(string, j, __inside__ = True)
        return Range((x, y), tail, TAPE, j), j, True
    return (x, y), j, False

def _parseName(string: str, index: int, stopper: str):
    """
    Reads <string>[<index>] up until the first <stopper>.
    <stopper> must be one character.
    Returns (name, newIndex)
    """
    export = ""
    
    while string[index] != stopper:
        export += string[index]
        index += 1
    return export, index

def _getArguments(string: str, index: int, expect: list[list[str]]):
    """
    Reads an optional list of arguements for an instruction, starting at <string>[<index>].
    The arguements should be in parenthesis and seperated by commas.
    Returns (arguements[], newIndex), or (None, newIndex) if no arguements are found.

    <expect> defines the expected arguements. Each item in <expect> is an arguement and are lists themselves.
    Each item in <expect>[ARGUEMENT] is a string and is a type that is allowed in that arguement. Types supported in this function:
    "int": integer
    "coord": coordinate on 2D tape.
    "range": range of coordiantes on 2D tape.
    """
    export = []
    argType = []

    if string[index] != "(":
        return None, index
    j = index + 1

    argNum = 0
    inside = True
    while j < len(string) and inside:
        if string[j] == ")":
            inside = False
            j += 1
            break
            break

        if argNum > len(expect):
            _throw(f"Too many arguments", j)
        
        if string[j] in "0123456789":
            argType = ["int"]
        elif string[j] == "@":
            argType = ["coord", "range"]
        else:
            name, j = _parseName(string, j, ",")
            if name in TAPE.aliases:
                pass
            else:
                _throw("Unknown arguement type: expected coordinate, alias, range or integer", j)
        
        if not any(item in expect[argNum] for item in argType):
            match argType:
                case ["int"]:
                    argTypeDisplay = "int"
                case ["coord", "range"]:
                    argTypeDisplay = "coordinate or range"
                case _:
                    argTypeDisplay = "unknown type"
            _throw(f"Wrong argument, expected {expect[argNum]}, got {argTypeDisplay}", j)
        
        if argType == ["int"]:
            value, j = _parseNumber(string, j)
            export.append(value)
        elif argType == ["coord", "range"]:
            value, j, _ = _parseCoordinate(string, j)
            export.append(value)
        
        argNum += 1

        if string[j] == ",":
            j += 1
        elif string[j] == ")":
            inside = False
            j += 1
        else:
            _throw("Expected ',' or ')' after argument", j)
    
    return export, j

        

def run(code):
    i = 0

    while i < len(code):
        c = code[i]

        match c.lower():

            # Basic movement
            # ======================================================================
            case "w":
                count, n = _parseNumber(code, i)
                
                TAPE.up(count)
                i = n if n > i else i + 1

            case "a":
                count, n = _parseNumber(code, i)

                TAPE.left(count)
                i = n if n > i else i + 1
            
            case "s":
                count, n = _parseNumber(code, i)
                
                TAPE.down(count)
                i = n if n > i else i + 1
            
            case "d":
                count, n = _parseNumber(code, i)
                
                TAPE.right(count)
                i = n if n > i else i + 1
            # ======================================================================

            # Flight
            # ======================================================================
            case "@":
                combinedCoordinate, newIndex, _ = _parseCoordinate(code, i)

                x, y = combinedCoordinate
                i = newIndex

                if TAPE.x > x:
                    TAPE.left(TAPE.x - x)
                elif TAPE.x < x:
                    TAPE.right(x - TAPE.x)
                
                if TAPE.y > y:
                    TAPE.down(TAPE.y - y)
                elif TAPE.y < y:
                    TAPE.up(y - TAPE.y)
            # ======================================================================

            # ((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
            case ":":
                instruction = code[i+1:i+3]

                match instruction:
                    
                    # Basic modification of integers
                    # --------------------------------------------------------------
                    case "set":
                        """
                        wait gah i dont want to code this its 1234 o clcok
                        """
                        startPosition = "gah"
            # ((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))