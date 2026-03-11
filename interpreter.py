from tape import Tape

def parseNumber(string, index):
    """
    Read an optional integer starting at <string>[<index>].
    Returns (integer, newIndex)
    """
    if index >= len(string) or string[index] not in "0123456789":
        return 1, index
    j = index
    while j < len(string) and string[j] in "0123456789":
        j += 1
    return int(string[i:j]), j

def run(code):
    TAPE = Tape()
    i = 0

    while i < len(code):
        c = code[i]

        match c.lower():
            case "w":
                count, n = parseNumber(code, i)
                
                TAPE.up(count)
                i = n

            case "a":
                count, n = parseNumber(code, i)

                TAPE.left(count)
                i = n
            
            case "s":
                count, n = parseNumber(code, i)
                
                TAPE.down(count)
                i = n
            
            case "d":
                count, n = parseNumber(code, i)
                
                TAPE.right(count)
                i = n