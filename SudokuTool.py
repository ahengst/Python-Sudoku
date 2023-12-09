# SudokuTool.py by Andy Hengst 2023-11-26

# NEXT - Look at README.md in git repository
# NEXT look at for loops that might be able to use map OR list comprehension
# NEXT places where set would work just as good as list
# learn Debugging

# Nomenclature and patterns used in this program:
# A sudoku grid is a square array (grid) made of smaller boxes.
# Rows and Columns. We identify array (list of lists) elements by list[row][col]
#   which may be backwards compared to graphs with X and Y coordinates.
#   typically [r] is a specific row index (0 start)
#             [rr] is a loop iterating row index (0 start)
#             row or {r+1} are human friendly row coordinates (1 start)
#             etc for cols
# You will see many loops of size GRID and many of size BOX, but context will
#   determine whether this means rows, columns, symbols (for GRID)
#   or rows/columns within a box, or Boxes (e.g. box origin coord + row offset coord)

""" these three constants get assigned in set_size() """
# BOX = 0  # Box size - the smaller count inside sudoku grid
# GRID = 0  # Grid size - the whole grid dimensions (rows=columns)
# SYMBOLS = []  # the correct group of symbols for player selected grid size

Sudoku = []  # the visible player grid ([rows][columns] )
candidates = []  # candidates grid - 2D array each cell containing all symbols


def set_size():
    # Called once to Set the grid size
    # for testing use 4x4, real soduku is 9x9, haxadoku is 16x16.
    global BOX, GRID, SYMBOLS, candidates  # assigned in here, used everywhere
    BOX = 0
    while not BOX:
        my_grid = input("Enter grid size (4/9/16): ")
        if my_grid == "4":
            BOX = 2
            GRID = 4
            SYMBOLS = list("1234")
        elif my_grid == "9":
            BOX = 3
            GRID = 9
            SYMBOLS = list("123456789")
        elif my_grid == "16":
            BOX = 4
            GRID = 16
            SYMBOLS = list("0123456789ABCDEF")

    print(f"set-size: Box size {BOX} and Grid size {GRID}")

    print(f"set-size: The symbols we will use are: {SYMBOLS}")

    candidates = [[SYMBOLS[:] for _ in range(GRID)] for _ in range(GRID)]
    # for the array to initialize with unique copies of SYMBOLS[] in each
    #   cell, the slice [:] is critical!


def fill_grid():
    # Called once for manual cells entry of puzzle symbols and spaces.
    for rr in range(GRID):
        prompt = f"fill: Type spaces or symbols for row #{rr+1}: "
        my_line = ""
        while len(my_line) != GRID:
            print(f"{' '*len(prompt)}{'.'*GRID}")
            my_line = input(prompt)
            if len(my_line) < GRID:
                print(f"Too few. Please enter {GRID} symbols or spaces for each row")
            if len(my_line) > GRID:
                print(f"Too many. Please enter {GRID} symbols or spaces for each row")
        Sudoku.append(list(my_line))


def display_grid():
    # frequently called - display current grid contents and candidates-remaining
    notsolved = 0  # keep track of squares NOT solved, also becomes False when done.
    ncand = 0  # keep track of total candidates

    horiz = f"{'--'*GRID}{'--'*BOX}-"  # construct a row divider of the correct length
    for rr in range(GRID):
        if rr % BOX == 0:
            print(f"{horiz}       {horiz}")  # print row dividers at each box boundary
        # display the play grid on the left
        for cc in range(GRID):
            if cc % BOX == 0:
                print("| ", end="")  # left edge and middle edges
            print(Sudoku[rr][cc], end=" ")
            notsolved += Sudoku[rr][cc] == " "
        print("|  ", end="")  # right edge of play grid

        # display a vertical legend for row numbers
        if rr + 1 <= 9:  # 9 being the last 1-digit number if counting to 16
            print(" ", end="")
        print(f"{rr+1}  ", end="")

        # display the remaining # candidates tallies on the right
        for cc in range(GRID):
            if cc % BOX == 0:
                print(" |", end="")  # left edge and middle edges
            lc = len(candidates[rr][cc])
            if lc <= 9:
                print(" ", end="")
            print(lc, end="")
            ncand += lc
        print(f" |  {rr+1}")  # right edge of tally grid

    print(f"{horiz}       {horiz}")  # draw the bottom border row divider

    horiz2 = " "
    for i in range(GRID):  # compose the column indexes row
        if i % BOX == 0 and i > 0:
            horiz2 += "  "
        if i + 1 < 10:
            horiz2 += " "  # &&& is there another way to pad leading spaces?
        horiz2 += str(i + 1)
    print(f"{horiz2}         {horiz2}")
    print(f"Not yet solved: {notsolved}                      Total candidates: {ncand}")

    return notsolved, ncand


def add_one_rc(call_mode="play"):
    if call_mode != "play":
        call_mode = "setup"
    # During play, player may add symbol to only an empty cell
    # row and col are human-friendly indices, r and c are pythonic indices
    row = int(input(f"{call_mode}: Changing row: "))  # &&& CRASH if not a digit
    if row < 1 or row > GRID:
        print("\nEntered row is out of bounds.")
        return -1, -1
    col = int(input(f"{call_mode}: Changing col: "))
    if col < 1 or col > GRID:
        print("\nEntered col is out of bounds.")
        return -1, -1

    r = row - 1
    c = col - 1
    if Sudoku[r][c] != " ":
        if call_mode == "play":
            print(
                "\nThat square is not empty. During play only empty cells can be modified."
            )
            return -1, -1
        else:
            print(f"The symbol in square {row},{col} is '{Sudoku[r][c]}'")
    my_sel = input("Type the symbol to add, or Enter to leave unchanged. ")
    if my_sel in SYMBOLS:  # symbol is in our list of digits
        Sudoku[r][c] = my_sel
        return r, c
    elif call_mode == "setup" and my_sel == " ":
        Sudoku[r][c] = my_sel
        return r, c
    elif my_sel == "":
        # <enter> is OK, do nothing
        return -1, -1
    else:
        print(f"Invalid symbol. Typed '{my_sel}' Expecting {SYMBOLS}")
        return -1, -1


def inspect_cand_rc():
    # During play, player may inspect remaining candidates
    # row and col are human-friendly indices, r and c are pythonic indices
    row = int(input("add: Inspecting row: "))  # &&& CRASH if not a digit
    if row < 1 or row > GRID:
        print("\nEntered row is out of bounds.")
    col = int(input("add: Inspecting col: "))
    if col < 1 or col > GRID:
        print("\nEntered col is out of bounds.")

    r = row - 1
    c = col - 1
    if Sudoku[r][c] != " ":
        print("\nThat square is not empty.")
    print(f"Candidates remaining at {row},{col}: {candidates[r][c]}")


def digest_new_cell(rr, cc):
    # call any time a new cell appears. Transmits presence of new symbol to nearby cells.
    # Does nothing with blank cells
    # rr/cc parameters are indexes 0... of cell having the effect in row/col/box
    # task is to "pop" all other cells in same column, same row, same box
    this_symbol = Sudoku[rr][cc]
    if this_symbol == " ":
        print(f"digest: found blank cell at {rr+1},{cc+1}. No change.")
        return

    # pop all symbols from this cell, because now it's occupied
    # now that we have a symbol, cell can't be anything else
    candidates[rr][cc].clear()

    # pop symb from each cell in col cc
    for r in range(GRID):
        pop_a_cell(this_symbol, r, cc)

    # pop symb from each cell in row rr
    for c in range(GRID):
        pop_a_cell(this_symbol, rr, c)

    # Do remaining Box rows/cols (do all box cells even though some already got done)
    # find top left corner (idx crow,ccol) of box
    # e.g. in 4x4 grid, lower-left-box top-left-corner would be crow=2, ccol=0.
    # always multiples of box where box = 2/3/4
    # loop through box rows and box cols offseting from that top left corner
    crow = rr - rr % BOX
    ccol = cc - cc % BOX
    # print(f"digest thinks top corner of box for this cell is at {crow}{ccol}")
    for r in range(crow, crow + BOX):
        for c in range(ccol, ccol + BOX):
            pop_a_cell(this_symbol, r, c)


def digest_a_slice_h(symb, r, ccc):
    # when a candidate has been narrowed down to one h-slice (in a row+box)
    #   this function will pop {symb} from other cells in this row or box
    # parameter ccc will be box origin
    # parameters indicate start of a slice (leftmost cell in h direction)
    # print(f"digesting h-slice for '{symb}' near {r+1},{ccc+1}")
    for cc in range(GRID):
        inslice = 0 <= (cc - ccc) < BOX
        # or, is cc within low and high bound of 'whichever slice it is in' ?
        # are we in the candidate's slice of this row?
        # print(f"{inslice}", end=" ")
        if inslice:  # pop cells directly "above/below" inside this box
            rrr = r - (r % BOX)  # rrr is box origin row
            for poprow in range(rrr, rrr + BOX):
                if poprow != r:  # leaving candidate's slice alone
                    pop_a_cell(symb, poprow, cc)
                # we are in row rr which could be 1st mid or last row in b
        else:  # pop cells in this row if outside box
            pop_a_cell(symb, r, cc)
    # print("end digesting slice -h")


def digest_a_slice_v(symb, rrr, c):
    # when a candidate has been narrowed down to one v-slice (in a col+box)
    #   this function will pop {symb} from other cells in this col or box
    # parameter rrr will be box origin
    # parameters indicate start of a slice (topmost cell in v direction)
    # print(f"digesting v-slice for '{symb}' near {rrr+1},{c+1}")
    for rr in range(GRID):
        inslice = 0 <= (rr - rrr) < BOX
        # or, is rr within low and high bound of 'whichever slice it is in' ?
        # are we in the candidate's slice of this col?
        # print(f"{inslice}", end=" ")
        if inslice:  # pop cells directly "left/right" inside this box
            ccc = c - (c % BOX)  # ccc is box origin row
            for popcol in range(ccc, ccc + BOX):
                if popcol != c:  # leaving candidate's slice alone
                    pop_a_cell(symb, rr, popcol)
                # we are in col cc which could be 1st mid or last col in b
        else:  # pop cells in this col if outside box
            pop_a_cell(symb, rr, c)
    # print("end digesting slice -v")


def pop_a_cell(symb, r, c):
    # called multiple times during digest_new_cell() or analyze_slicy
    # remove candidate symbol 'symb' from THIS nearby cell of row, col, box.
    # just condensing repeated code.
    if symb in candidates[r][c]:  # test to avoid getting ValueError at .remove
        candidates[r][c].remove(symb)


def autofill_ones():
    # any time only one candidate remains, assign that cell.
    r = None  # using r to see if there were any 1-candidate cells at all
    for rr in range(GRID):
        for cc in range(GRID):
            if len(candidates[rr][cc]) == 1:
                r = rr
                print(f"Auto assigning '{candidates[r][cc][0]}' to cell {r+1},{cc+1}")
                Sudoku[r][cc] = candidates[r][cc][0]
                digest_new_cell(r, cc)
    if r == None:
        print("NO 1-candidate cells found.")


def analyze_grid():
    # look for candidates that fit in only one cell of a row or column or box
    # this will do one pass, may need to call multiple times

    # Let's look for only-one-possible-position, BY ROW
    for rr in range(GRID):
        r, c, symb = cand_in_row(rr)  # may return ONE matching symbol, not all.
        if symb != " ":
            print(f"agr: Auto assigning '{symb}' in row at {r+1},{c+1}")
            Sudoku[r][c] = symb
            digest_new_cell(r, c)

    # again for every COL
    for cc in range(GRID):
        r, c, symb = cand_in_col(cc)  # may return ONE matching symbol, not all.
        if symb != " ":
            print(f"agc: Auto assigning '{symb}' in col at {r+1},{c+1}")
            Sudoku[r][c] = symb
            digest_new_cell(r, c)

    # again for all BOXes
    for rr in range(0, GRID, BOX):
        for cc in range(0, GRID, BOX):
            r, c, symb = cand_in_box(rr, cc)  # returns r,c position on grid
            if symb != " ":
                print(f"agb: Auto assigning '{symb}' in box at {r+1},{c+1}")
                Sudoku[r][c] = symb
                digest_new_cell(r, c)


def cand_in_row(rr):
    # look for candidates that fit in only one cell of a row
    # returns first match, ignores others.
    list_g = []  # to collect all candidates
    for cc in range(GRID):
        list_g.extend(candidates[rr][cc][:])
    for sym in SYMBOLS:
        if list_g.count(sym) == 1:  # we found a single! locate it...
            # print(
            #    f"checkrow: we .count({sym}) appearing only once in Row{rr+1}..",
            #    end="",
            # )
            for cc in range(GRID):
                if candidates[rr][cc].count(sym) == 1:
                    # print(f".at column {cc+1}")
                    return rr, cc, sym
            # print(
            #    f"checkrow: by now we should have found {sym}'s spot in row{rr+1} but DID NOT."
            # )
    # print(f"checkrow: nothing interesting in row {rr+1}")
    return -1, -1, " "


def cand_in_col(cc):
    # look for candidates that fit in only one cell of a column
    # returns first match, ignores others.
    list_g = []  # to collect all candidates
    for rr in range(GRID):
        list_g.extend(candidates[rr][cc][:])
    # print(f"leftover candidates row{rr+1}: {list_g}")
    for sym in SYMBOLS:
        if list_g.count(sym) == 1:  # we found a single! locate it...
            # print(
            #    f"checkcol: we .count({sym}) appearing only once in Col{cc+1}..",
            #    end="",
            # )
            for rr in range(GRID):
                if candidates[rr][cc].count(sym) == 1:
                    # print(f".at row {rr+1}")
                    return rr, cc, sym
            # print(
            #    f"checkrow ERROR: by now we should have found {sym}'s spot in col{cc+1} but DID NOT."
            # )
    # print(f"checkcol: nothing interesting in col {cc+1}")
    return -1, -1, " "


def cand_in_box(br, bc):
    # look for candidates that fit in only one cell of a box at 'root'
    # returns first match, ignores others.
    list_g = []  # to collect all candidates

    for rr in range(BOX):
        for cc in range(BOX):
            list_g.extend(candidates[br + rr][bc + cc][:])
    # print(f"leftover candidates in box at idx{br},{bc}: {list_g}")
    for sym in SYMBOLS:
        if list_g.count(sym) == 1:  # we found a single! locate it...
            # print(f"checkbox: we .count({sym}) appearing only once in box at idx{br},{bc}..",end="")
            for rr in range(BOX):
                for cc in range(BOX):
                    if candidates[br + rr][bc + cc].count(sym) == 1:
                        # print(f".at cell {br+rr+1},{bc+cc+1}")
                        return br + rr, bc + cc, sym
            # print(f"checkbox: by now we should have found {sym}'s spot in box at idx{br},{bc} but DID NOT.")
    # print(f"checkbox: nothing interesting in box at idx{br},{bc}")
    return -1, -1, " "


def analyze_slicy():
    # Eliminates candidates, but cannot Auto assign any specific symbols to cells.
    # make multiple calls to test each row, col, box looking for symbols that
    # must be present in a slice but we don't know quite which cell yet.
    # e.g. in a 9x9 grid a slice would be a 3-cell group.
    # &&&(?really?) ADD: In this slice, the candidate MAY only fit in one spot. Assign it then.
    # this function does the same sort of thing for 3 geometries: row, column, box.

    # IDEA candidate living in a row-slice can be found by checking box or row
    # IDEA candidate living in a col-slice can be found by checking box or col
    # IDEA - both can be dealt with using exact same code. only_one_row_slice() only_one_col_slice()
    # maybe the loop should be from perspective of one slice, look in either direction.

    # &&&(?fixed?)should we move SYMBOLS to outside loop otherwise some combinations never get tested?

    # look for "warm areas" for symbols inside each row.
    for rr in range(GRID):  # one row at a time...
        slices_as = []  # will be a list of {BOX} lists
        cands_set = set()  # all candidates in this group
        for cc in range(BOX):  # traversing each slice...
            ccc = cc * BOX  # ccc is box origin column
            cands_list = []  # only candidates from this slice(cc) of this row(rr)
            for oo in range(BOX):  # offset
                cands_list.extend(candidates[rr][ccc + oo][:])  # &&& list is overkill
                cands_set = cands_set | {*candidates[rr][ccc + oo][:]}
            slices_as.append(cands_list[:])  # list of lists &&& -> of sets
        # print(f"analyzeslicy: row {rr+1} slics {cands_set}")

        for symb in cands_set:
            # could do all SYMBOLS but we only do candidates still in 'row'
            # print(f"\nanalyzeslicy: in row {rr+1} looking at '{symb}'")
            gotahit, whichsl = warmer(slices_as, symb)  # test this collection of slices
            if not gotahit:
                continue  # try again with next symbol

            # so, found something interesting
            # print(f"row {rr+1} expect '{symb}' at slice {whichsl+1}")
            # print(f"analyzeslicy: nulling '{symb}' in row {rr+1} for other cells...")
            digest_a_slice_h(symb, rr, whichsl * BOX)
            # print(" ")

    # Again, for the columns this time
    # look for "warm areas" for symbols inside each column.
    for cc in range(GRID):  # one column at a time...
        slices_as = []  # will be a list of {BOX} lists
        cands_set = set()  # all candidates in this group
        for rr in range(BOX):  # traversing each slice...
            rrr = rr * BOX  # rrr is box origin row
            cands_list = []  # only candidates from this slice(rr) of this column(cc)
            for oo in range(BOX):  # offset
                cands_list.extend(candidates[rrr + oo][cc][:])  # &&& list is overkill
                cands_set = cands_set | {*candidates[rrr + oo][cc][:]}
            slices_as.append(cands_list[:])  # list of lists &&& -> of sets
        # print(f"analyzeslicy: col {cc+1} slics {cands_set}")

        for symb in cands_set:
            # could do all SYMBOLS but we only do candidates still in 'col'
            # print(f"\nanalyzeslicy: in col {cc+1} looking at '{symb}'")
            gotahit, whichsl = warmer(slices_as, symb)  # test this collection of slices
            if not gotahit:
                continue  # try again with next symbol

            # so, found something interesting
            # print(f"col {cc+1} expect '{symb}' at slice {whichsl+1}")
            # print(f"analyzeslicy: nulling '{symb}' in col {cc+1} for other cells...")
            digest_a_slice_v(symb, whichsl * BOX, cc)
            # print(" ")

    # Again, for the boxes this time
    #   Let's try n-horizontal slices and n-vertical slices together!
    # look for "warm areas" for symbols inside each box.
    ##print("analyzeg: looking at boxes...")
    for brr in range(0, GRID, BOX):  # box origins by row
        for bcc in range(0, GRID, BOX):  # box origins by col
            slices_as_h = []  # will be a list of {BOX} lists - horiz.
            slices_as_v = []  # will be a list of {BOX} lists - vert.
            cands_set = set()  # all candidates in this group
            for slic in range(BOX):  # internal box offset for slices
                cands_list_h = []  # only candidates from this row-slice of box
                cands_list_v = []  # only candidates from this column-slice of box
                for cell in range(BOX):  # internal box/slice offset
                    cands_list_h.extend(candidates[brr + slic][bcc + cell][:])
                    # &&& ...list is overkill
                    cands_list_v.extend(candidates[brr + cell][bcc + slic][:])
                    # &&& ...list is overkill
                    cands_set = cands_set | {*candidates[brr + cell][bcc + slic][:]}
                slices_as_h.append(cands_list_h[:])  # list of lists &&& -> of sets
                slices_as_v.append(cands_list_v[:])  # list of lists &&& -> of sets
            # print(f"\nanalyzeslicy: box {brr+1},{bcc+1} slices h {slices_as_h}")
            # print(f"\nanalyzeslicy: box {brr+1},{bcc+1} slices v {slices_as_v}")
            # print(f"analyzeslicy: box {brr+1},{bcc+1} slics {cands_set}")

            # for box origin at brr,bcc look at its extracted slices...horizontally
            for symb in cands_set:
                # could do all SYMBOLS but we only do candidates still in 'box'
                gotahit, whichsl = warmer(
                    slices_as_h, symb
                )  # test this collection of slices
                if not gotahit:
                    continue  # try again with next symbol

                # so, found something interesting horizontally
                # print(f"box idx{brr},{bcc} expect '{symb}' at h-slice {whichsl+1}")
                # print(
                #    f"analyzeslicy: nulling '{symb}' in box idx{brr},{bcc} for other h-slices..."
                # )
                digest_a_slice_h(symb, brr + whichsl, bcc)
                # print(" ")

            # for box origin at brr,bcc look at its extracted slices...vertically
            for symb in cands_set:
                # could do all SYMBOLS but we only do candidates still in 'box'
                gotahit, whichsl = warmer(
                    slices_as_v, symb
                )  # test this collection of slices
                if not gotahit:
                    continue  # try again with next symbol

                # so, found something interesting vertically
                # print(f"box idx{brr},{bcc} expect '{symb}' at v-slice {whichsl+1}")
                # print(
                #    f"analyzeslicy: nulling '{symb}' in box idx{brr},{bcc} for other v-slices..."
                # )
                digest_a_slice_v(symb, brr, bcc + whichsl)
                # print(" ")

                # print(" ")


def warmer(slices, thiscand):  # expecting 2 or 3 or 4 slices as list-of-lists
    # By working out the different slicing directions in calling routine,
    #  we can code one logical test here
    # We are looking for the slice a symbol must be in even though it's
    #   not clear which cell it's in. Enough info to eliminate nearby candidates.
    # print(f"warmer: receives parameters {slices} {thiscand}")

    count_cand = 0
    whichslice = 0  # will contain 'idx' of slice where symbol exists
    # by the end of this cand loop, if only found once, this was where.
    for ss in range(BOX):  # once for each slice
        if thiscand in slices[ss][:]:  # is Symbol in this slice?
            whichslice = ss
            count_cand += 1
    if count_cand == 1:
        return True, whichslice  # all that's needed is to say "check this symbol"
    else:
        return False, 0
        # exhausted all symbols, rows, etc so return blanks


def main():
    global BOX, GRID, SYMBOLS, candidates, Sudoku
    # print("main: Begin main routine")
    set_size()  # initialize grid dimensions and candidates array

    fill_grid()  # manual entry of the puzzle, may contain errors

    # manual error correction, until player says Begin
    my_command = ""
    while my_command != "Q" and my_command != "B":
        display_grid()
        my_command = input("(m)odify  (B)egin play  (Q)uit :")
        if my_command == "m":
            add_one_rc("setup")
        elif my_command == "B":
            print("\nBEGIN PLAY. *no save or undo features - type carefully*\n")
        elif my_command != "Q":
            print("Invalid command")

    # player selected either B or Q
    if my_command == "Q":
        print("\nThank you for playing. Bye!\n")
        return

    # my_command must be "B" right now.
    # Loop over entire array and digest all cells with a symbol
    for rr in range(GRID):
        for cc in range(GRID):
            if Sudoku[rr][cc] != " ":
                digest_new_cell(rr, cc)

    # my_command must be "B" right now.
    while my_command != "Q":
        if my_command in ["1", "n", "a", "s"]:  # display if we changed grid
            ns, nc = display_grid()
            if ns == 0:
                print("\nThe puzzle grid is full, congratulations?")
                break
            if ns > 0 and nc == 0:
                print("\nNo candidates remain, but the puzzle is not solved!")
                print("Someone must have made a bad guess.")
                break

        my_command = input(
            "(m)odify   autofill (1) cell   (a)nalyze row-col-box   analyze (s)lices   (i)nspect   (Q)uit :"
        )
        if my_command == "m":
            r, c = add_one_rc()
            if r >= 0 and c >= 0:
                digest_new_cell(r, c)

        elif my_command == "1":
            autofill_ones()

        elif my_command == "a":
            analyze_grid()

        elif my_command == "s":
            analyze_slicy()

        elif my_command == "i":
            inspect_cand_rc()

        elif my_command != "Q":
            print("Invalid command")

    print("\nThank you for playing. Bye!\n")

    # next - analyze and stop to ..
    # next - .. display hint


main()
