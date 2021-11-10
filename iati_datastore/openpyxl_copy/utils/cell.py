# We want one function from openpyxl (MIT licensed)
# Rather than install the whole library, just have that function!
# It's from 3.0 branch:
# https://foss.heptapod.net/openpyxl/openpyxl/-/blob/0e772b1a30267d8d3580837622bd1fc68e9ec5b7/openpyxl/utils/cell.py
# If we ever do add openpyxl as a dependency,
#   we can just remove our local openpyxl package and change the package name we are calling.


def _get_column_letter(col_idx):
    """Convert a column number into a column letter (3 -> 'C')

    Right shift the column col_idx by 26 to find column letters in reverse
    order.  These numbers are 1-based, and can be converted to ASCII
    ordinals by adding 64.

    """
    # these indicies corrospond to A -> ZZZ and include all allowed
    # columns
    if not 1 <= col_idx <= 18278:
        raise ValueError("Invalid column index {0}".format(col_idx))
    letters = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx, 26)
        # check for exact division and borrow if needed
        if remainder == 0:
            remainder = 26
            col_idx -= 1
        letters.append(chr(remainder+64))
    return ''.join(reversed(letters))



_STRING_COL_CACHE = {}
for i in range(1, 18279):
    col = _get_column_letter(i)
    _STRING_COL_CACHE[i] = col


def get_column_letter(idx,):
    """Convert a column index into a column letter
    (3 -> 'C')
    """
    try:
        return _STRING_COL_CACHE[idx]
    except KeyError:
        raise ValueError("Invalid column index {0}".format(idx))

