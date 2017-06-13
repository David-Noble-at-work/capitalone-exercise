#!/usr/bin/env python36

""" ExtraHop Programming Problem--

Written by David Noble <david@thenobles.us>.

This module was developed and tested under Python 3.6 on macOS Sierra. Please ask for Python 2.7 code or code that
will run under Python 2.7 or Python 3.6, if you would prefer it. I mention this because I see that your deprecated
Python SDK is written for Python 2.7.3 or higher, but not Python 3.x.

mypy 0.511 clean

"""

import io
import random
import re

from string import ascii_lowercase
from typing import Dict, Iterator, List, Mapping, Optional, Sequence, Tuple


def find_longest_word(grid: 'Grid', words: List[str]) -> Optional[Tuple[str, Tuple[Tuple[int, int], ...]]]:
    """ Find the longest word from a list of words that can be produced from an 8 x 8 grid using grid movement rules

    Words on the grid are located using this set of rules:
    
    1.	Start at any position in the grid, and use the letter at that position as the first letter in the candidate 
        word.
        
    2.	Move to a position in the grid that would be a valid move for a knight in a game of chess, and add the letter 
        at that position to the candidate word.
        
    3.	Repeat step 2 any number of times.
    
    This function preserves the contents of the `words` list. Length ties are broken by alphabetic sort order. Hence, 
    for example, if `foo` and `bar` are 
    
    * in the list of words and
    * the longest words to be found on a graph
    
    :func:`find_longest_word` will return `'bar'` and a tuple of the coordinates of its letters in the grid as its 
    result.

    Parameters
    ----------

    :param grid: A grid presumably filled with letters from some alphabet.
    :type grid: Grid
    
    :param words: A list of words that might be produced from letters on the 'grid' using grid moves.
    :type words: List[str]
    
    :return: Longest word that can be produced from the letters on 'grid' using grid moves; or :const:`None`, if no word
    can be produced from the letters on 'grid'.
    :rtype: Optional[Tuple[str, Tuple[Tuple[int, int], ...]]]
        
    Implementation notes
    ====================

    A grid should be thought of as a directed graph. The cells of a grid are its vertices. The movements permitted from 
    a cell on the graph are edges. The vertices are labeled by row, column coordinates and contain a single piece of 
    data: a letter drawn from some alphabet. Producing a word from the letters on a grid amounts to a graph traversal 
    in the search for a path that traces out the word.
    
    In this solution we represent a grid with the `Grid` class which encapsulates two operations for tracing a word 
    path and following it: 
    
        ==================  ==========================================================================================
        Method              Description
        ==================  ==========================================================================================
        `Grid.find_path`    Searches a grid for a path to a word. A word path is represented as a tuple of row, column
                            coordinates. Coordinates are zero-based.
        `Grid.__getitem__`  Called to evaluate grid[coordinate].
        
    After finding a path you can iterate through it like this:
    
        for row, column in path:
            print(grid[(row, column)]
        
    The `Grid` class also comes with a set of methods useful for testing: 
        ==================  ==========================================================================================
        Method              Description
        ==================  ==========================================================================================
        `Grid.generate`     Creates a grid containing a set of words. Cells left unfilled by letters from the words
                            are filled with random ASCII characters. 
        `Grid.load`         Loads a grid from a file.
        `Grid.save`         Saves a grid to a file.
        
    See the `Grid` class for additional documentation
    
    Algorithm
    ---------

    `find_longest_word` non-destructively sorts words by length and alphabetic order. It then calls `Grid.find_path`
    for each word until a path is found. It then returns the word as well as the path to the word. If no word path
    is found a value of None is returned. `Grid.find_path` case-folds words to ensure all string comparisons are case
    insensitive.
    
    Grid representation
    ~~~~~~~~~~~~~~~~~~~

    For each cell on a grid we create a map of the coordinates of all reachable cells. We partition these coordinates
    by the letter contained by the cell that it addresses. Thus, for example, all cells that contain the letter 'a' are
    grouped together. This enables the Grid class to quickly determine the viability of a path based on a letter value.
      
    Structurally each cell looks like this::
    
        coordinate: Tuple[int, int],
            reachable_letters: Map[str, Tuple[Tuple[int, int], ...]
            
    Thus, for example, cell (0, 0) might look like this::
    
        (0, 0): {
            'h': ((1, 2),), 'r': ((2, 1),)
        }

    At a higher level cells are organized by letter in a dict--see the `Grid._letters` attribute. Thus, for example, 
    if cell (0, 0) contained the letter 'h' it would be stored in `Grid._letters` like this::

        'h': {    
            (0, 0): {
                'h': ((1, 2),), 'r': ((2, 1),)
            },
            ...
        }
    
    All cells containing the letter 'h' are stored under the 'h' key in `Grid._letters`. All letters contained in a
    grid are represented in `Grid._letters`. This enables quick access to the starting points for a word path search.
    The `Grid.find_path` method needs only to query for it's first letter and iterate over items in the coordinate
    map until a path is found or the coordinates in the map are exhausted.
    
    The `Grid` class also stores a compact form of the grid: An 8 x 8 list of lists. It is the basis of the 
    `Grid.__getitem__` implementation. 

    **Undone**
    
    * Elimination of previously-visited nodes known to be fruitless. During grid traversal it's possible that a cell
      will be visited more than once for the same letter. If it's visited more than once for the same letter, it clear
      that the path is fruitless. This is because the search would have succeeded on the first visit. 
       
      This might prove to be a useful optimization and would be easy to add. 
      
    * To speed searches one might consider memoization of words/word stems; pre-populating some and building up others 
      over time. One might for example, create such a map of words/word stems from the output of `Grid.generate`. Other
      words or word paths unknown to the author might likely be discovered over time. 
      
      Performance requirements would need to be established before considering implementing this.

    Command line
    ============
    
    This function may be executed from the command line using this syntax::
    
        python find_longest_word.py --grid <filename> <word>...
    
    Alternatively you may create a command argument file and reference it like this::
    
        python @<command-file-name>
        
    A command file should contain one argument per line as illustrated in `Programming-language-names.args`, included
    with this code::
     
        --grid
        grid-1
        ALGOL
        FORTRAN
        Simula

    Output includes the word found and the sequence of coordinates of the letters of the word found on the input grid.
    You will see that this command::
     
        python @Programming-language-names.args
        
    produces this output::
    
        ('FORTRAN', ((3, 4), (5, 3), (3, 2), (2, 0), (3, 2), (1, 3), (0, 5)))
        
    The coordinates written are zero-based row, column values, not unit-based column, row values as presented in 
    `PythonCodingProblem.docx`. 
    
    """
    words = sorted((word for word in words if word), key=lambda x: (-len(x), x))

    for word in words:
        path = grid.find_path(word)
        if path is not None:
            return word, path

    return None


class Grid(object):
    """ Represents an 8 x 8 grid containing letters drawn from an alphabet
    
    Grid entries are case folded when the grid is instantiated to ensure that case-insensitive comparisons can be made 
    with any alphabet.
    
    **WARNING**
    
    In some languages case-folding produces more than one character from a single letter.
       
    Example: The German letter 'ß' case folds to 'ss'.
    
    This fact must be taken into account when creating grids. You would not want to include the 'ß' character in a
    grid created by this code without taking care to ensure that the 8 x 8 grid constraint is met following case 
    folding. 
    
    Implementation notes
    --------------------
    See the implementation notes for the `find_longest_word` function.
    
    """
    __slots__ = ('_grid', '_letters')  # saves space; good practice for objects with no dynamic membership requirements

    def __init__(self, data: Sequence[str]) -> None:

        assert len(data) == Grid.size
        grid: List[List[str]] = []

        for line in data:
            line = Grid._replace_whitespace('', line).casefold()  # type: ignore
            assert len(line) == Grid.size
            grid.append([letter for letter in line])

        self._grid = grid

        letters: Dict[str, Dict[Tuple[int, int], Dict[str, Tuple[Tuple[int, int], ...]]]] = {}

        for row, record in enumerate(grid):
            for column, letter in enumerate(record):
                origin = row, column
                vertices = letters.setdefault(letter, {})
                edges = vertices.setdefault(origin, {})
                for delta_y, delta_x in Grid._moves:
                    position = row + delta_y, column + delta_x
                    if 0 <= position[0] < Grid.size and 0 <= position[1] < Grid.size:
                        other_letter = self._grid[position[0]][position[1]]
                        edges[other_letter] = edges.setdefault(other_letter, tuple()) + (position,)

        self._letters = letters

    def __getitem__(self, position: Tuple[int, int]) -> str:
        """ Get the letter in a cell on the current grid
        
        This method only partially implements `self[key]` semantics. Most notably slicing is not supported.
        
        :param position: row, column coordinates of a cell on the current grid
        :type position: Tuple[int, int]
        
        :return: The letter at 'position' on the current grid.
        :rtype: str
        
        :raises IndexError: If 'position' does not specify a location on the current grid.
         
        """
        return self._grid[position[0]][position[1]]

    def __str__(self) -> str:
        """ Get a human readable string representation of the current grid
         
        :return: A human readable string representation of the current grid
        :rtype: str
        
        """
        return '\n'.join(' '.join(field for field in record) for record in self._grid)

    def find_path(self, word: str) -> Optional[Tuple[Tuple[int, int], ...]]:
        """ Perform a recursive search for the tail end of a case-folded word from a position on the current grid 

        This local function economizes on stack space by relying on variables in its closure and short-circuiting 
        recursion along previously traversed paths. It is worth noting that words, even very long words in languages
        like German aren't that long. Stack space should not be an issue and the code is straight forward with this
        recursive implementation.

        Sidebar 
        -------
        According to the [BBC](http://www.bbc.com/news/world-europe-22762040) the longest German word was just lost 
        after an EU law change. It is 65 characters long, one more than the number of cells in a grid:: 

            Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz  

        In our experiments the `Grid.generate` function has not yet found a placement for this word in a grid; though
        there is a non-zero probability that the current implementation could. Alternatively one could update
        `Grid.generate` to consider all possible starting places and all possible paths from each of them. We leave
        this as an exercise.

        Parameters
        ----------

        :param word: The word to find in the current grid 
        :type word: str

        :return: A tuple containing the coordinates of the letters of 'word' or const:`None`, if 'word' is not found.
        :rtype: Optional[Tuple[Tuple[int, int], ...]] 

        """
        assert len(word) > 0

        word = word.casefold()  # type: ignore

        try:
            nodes = self._letters[word[0]]
        except KeyError:
            path = None
        else:
            path = self._find_path(word, iter(nodes.keys()))

        return path

    @classmethod
    def generate(cls, words: Iterator[str]) -> Tuple['Grid', Mapping[str, Tuple[str, Tuple[Tuple[int, int],...]]]]:
        """ Generate a grid containing a set of words that can be found using grid movement rules
        
        Use this method to create test grids. An error message is produced for each word that cannot be put on the grid.
        Randomly generated ASCII characters are used to fill cells not filled by the words or--as explained in the 
        code--partial words we put on the grid.

        The implementation of this method is rudimentary, but useful for producing test grids and verifying correctness.
        
        Parameters
        ----------
        
        :param words: An iterator over the set of words to be put on to the grid.
        :type words: Iterator[str]
        
        :return: A grid object containing the words or partial words we put on the grid mixed with random ASCII fill
        characters.
        :rtype: Grid

        Example
        -------
        To see this method in action run these statements from a Python 3.6 REPL. A variable number of letters from
        the German word "Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz" will be placed on the
        grid::
        
            from find_longest_word import Grid, find_longest_word
            grid, paths = Grid.generate([
                'foo', 'bar', 'Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz'
            ])
            find_longest_word(grid, ['foo', 'bar', 'rindfleischetikettierun'])
            grid.save('grid-4')
          
        We're OK with this given our intent: generate some useful test grids. As indicated in the above REPL session 
        output you will find the results of example this REPL session in `grid-4'. We did not save the paths created
        for the words.
        
        """
        paths: Dict[str, Tuple[str, Tuple[Tuple[int, int], ...]]] = {}
        missing_data = chr(0)
        data = [[missing_data] * Grid.size for i in range(0, Grid.size)]

        for word in words:

            # Put this word on the grid starting at a random location

            origins = [(x, y) for x in range(0, Grid.size) for y in range(0, Grid.size)]
            path: List[Tuple[int, int]] = None
            row, column = None, None
            random.shuffle(origins)

            case_folded_word = word.casefold()  # type: ignore

            def put(letter: str, x: int, y: int) -> bool:
                if data[x][y] in (missing_data, letter):
                    data[x][y] = letter
                    return True
                return False

            index = 0

            for row, column in origins:
                if put(case_folded_word[0], row, column):
                    path = [None] * len(case_folded_word)
                    path[0] = row, column
                    index = 1
                    break

            if index == 0:
                print('could not find a place for any of the letters from', case_folded_word)
                paths[word] = None
            else:
                while index < len(case_folded_word):

                    # Try to put the letter at word[index] on the grid using a sequence of random grid moves
                    # One might try alternative paths the way function find_longest_word does, but we'll
                    # scope that out of this exercise and accept two things:
                    #
                    # * By selecting the first random letter placement that works and not trying alternatives path ways
                    #   out chance of failure is high.
                    # * In the failure case this algorithm will leave partial words on the grid.
                    #
                    # We're OK with this given our intent for this method: generate some random grids for testing.

                    moves = [move for move in cls._moves]
                    random.shuffle(moves)
                    put_letter = False

                    for x, y in moves:
                        x, y = row + x, column + y
                        if 0 <= x < Grid.size and 0 <= y < Grid.size:
                            if put(case_folded_word[index], x, y):
                                path[index] = row, column = x, y
                                put_letter = True
                                index += 1
                                break

                    if not put_letter:
                        break

                if index < len(case_folded_word):
                    print(
                        'only placed', index,  'out of', len(case_folded_word), 'letters from', case_folded_word,
                        ':', case_folded_word[:index]
                    )

                paths[word] = case_folded_word[:index], tuple(path[:index])

        for record in data:
            for column in range(0, Grid.size):
                if record[column] == missing_data:
                    record[column] = random.choice(ascii_lowercase)  # we do not use a larger alphabet like latin-1 :(

        return Grid([' '.join(row) for row in data]), paths

    @classmethod
    def load(cls, filename: str) -> 'Grid':
        """ Load a grid from a file
        
        :param filename: Name of a file containing a grid.
        :type filename: str
        
        :return: A Grid object
        :rtype: Grid
         
        """
        with io.open(filename) as istream:
            lines: List[str] = istream.readlines()
        return cls(lines)

    def save(self, filename: str) -> None:
        """ Save the current grid to a file 
        
        :param filename: Name of the file to which the current grid should be saved.
        :type filename: str
        
        :return: :const:`None`
        
        """
        with io.open(filename, 'w') as ostream:
            ostream.write(str(self))

    size = 8

    # region Protected

    _moves = [
        (-1, +2),  # lt 1 up 2
        (-1, -2),  # lt 1 dn 2
        (-2, +1),  # lt 2 up 1
        (-2, -1),  # lt 2 dn 1
        (+1, +2),  # rt 1 up 2
        (+1, -2),  # rt 1 dn 2
        (+2, +1),  # rt 2 up 1
        (+2, -1),  # rt 2 dn 1
    ]

    _replace_whitespace = re.compile('\s+').sub

    def _find_path(self, word: str, candidates: Iterator[Tuple[int, int]]) -> Optional[Tuple[Tuple[int, int], ...]]:

        stack = [(word, next(candidates), candidates)]

        while len(stack) > 0:

            stem, candidate, candidates = stack.pop()

            if len(stem) == 1:
                stack.append((stem, candidate, candidates))
                return tuple(candidate for stem, candidate, candidates in stack)

            # Collect the data we need to move on to the next letter

            nodes = self._letters[stem[0]]  # represents all occurrences of the current letter on the current grid
            neighbors = nodes[candidate]  # represents all nodes reachable from the current candidate
            next_letter = stem[1]

            try:
                new_candidates = iter(neighbors[next_letter])
            except KeyError:
                # There's no path to the next letter and so we back up until we've got another viable path to search
                while True:
                    try:
                        candidate = next(candidates)
                    except StopIteration:
                        if len(stack) == 0:  # there's no where else to look
                            break
                        stem, candidate, candidates = stack.pop()
                    else:
                        stack.append((stem, candidate, candidates))
                        break
            else:
                next_stem = stem[1:]
                stack.append((stem, candidate, candidates))
                stack.append((next_stem, next(new_candidates), new_candidates))

        return None

    # endregion


if __name__ == '__main__':

    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(
        description='Find the longest word from a list of words that can be produced from an 8 x 8 grid of letters',
        fromfile_prefix_chars='@'
    )

    parser.add_argument('--grid', required=True)
    parser.add_argument('words', nargs='+')

    arguments = parser.parse_args(sys.argv[1:])

    print(find_longest_word(Grid.load(arguments.grid), arguments.words))
