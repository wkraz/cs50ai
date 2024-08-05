import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the number of known mines = the number of cells, then they're all mines
        if self.count == len(self.cells) and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if there are no known mines, then they're all safe
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1 # we know this is a mine so decrease count by 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            # don't have to change self.count because it's not a mine


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # mark the cell as a move that has been made
        self.moves_made.add(cell) 

        # mark the cell as safe
        self.mark_safe(cell)

        # add new sentence to AI's knowledge base
        # get neighbors and 
        unknown_neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # if it's the actual cell it's not a neighbor
                if (i, j) == cell:
                    continue

                # see if we know it's a mine
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # see if we know it's safe
                if (i, j) in self.safes:
                    continue

                # make sure the cell is in the actual grid and add it to our set
                if 0 <= i < self.height and 0 <= j < self.width:
                    unknown_neighbors.add((i, j))

        # add a sentence to the knowledge base with the neighbors we don't know and how many mines we know are in them
        new_sentence = Sentence(unknown_neighbors, count)
        self.knowledge.append(new_sentence)

        # look at the knowledge base and try and get more information
        for sentence in self.knowledge:

            known_mines = sentence.known_mines()
            if known_mines:
                for cell in known_mines.copy():
                    self.mark_mine(cell)

            known_safes = sentence.known_safes()
            if known_safes:
                for cell in known_safes.copy():
                    self.mark_safe(cell)

        # remove empty sentence objects from list
        empty_sentence = Sentence(set(), 0)
        self.knowledge = [sentence for sentence in self.knowledge if sentence != empty_sentence]

        # try and infer more information from existing knowledge and add it to knowledge base
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:

                # make sure they're not the same sentence
                if sentence1 is sentence2:
                    continue
                
                # remove duplicates
                if sentence1 == sentence2:
                    self.knowledge.remove(sentence2)

                if sentence1.cells.issubset(sentence2.cells): # looking for all possible subsets

                    # get the set difference of the 2 
                    subset_set = sentence2.cells - sentence1.cells

                    # since it's a subset, the mine count is just the difference of the 2
                    subset_count = sentence2.count - sentence1.count

                    # add a sentence to the knowledge base with these 2 pieces of knowledge
                    new_knowledge = Sentence(subset_set, subset_count)
                    if new_knowledge not in self.knowledge:
                        self.knowledge.append(new_knowledge)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                    
                if cell not in self.moves_made:

                    # check the list of safe mines and see if it's there
                    if cell in self.safes:
                        return cell
                    
                    for sentence in self.knowledge:
                        # if any knowledge in the base says cell is safe, then return cell
                        known_safes = sentence.known_safes()
                        if known_safes is not None:
                            if cell in known_safes:
                                return cell
                
        # we don't know it's safe so return nothing
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # empty set of moves we can make
        moves = set()

        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)

                valid_move = True

                # make sure a move has not occurred in the cell
                if cell in self.moves_made:
                    valid_move = False

                # make sure it's not in the list of mines
                if cell in self.mines:
                    valid_move = False

                for sentence in self.knowledge:
                    # make sure no knowledge base says it's a mine
                    known_mines = sentence.known_mines()
                    if known_mines is not None:
                        if cell in known_mines:
                            valid_move = False
            
                # if nothing above has happened, add it to the set of valid moves
                if valid_move:
                    moves.add(cell)
            
        # if there's no moves, return None
        if len(moves) == 0:
            return None
        
        # return a random move in the move set now that it's not empty
        return random.choice(list(moves))
