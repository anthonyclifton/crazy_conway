import unittest


def crazy_conway(grid):
    falsed_grid = pad_grid(grid)
    return [[two_live_neighbors_retains_life(live_neighbor_count(slice_it(falsed_grid, rowIndex + 1, columnIndex + 1)), grid[rowIndex][columnIndex]) for columnIndex in range(len(grid[0]))] for rowIndex in range(len(grid))]


def pad_grid(grid):
    falsed_grid = [[False for _ in range(len(grid[0]) + 2)] for _ in range(len(grid) + 2)]
    c = [[False] + row + [False] for row in grid]
    falsed_grid[1:-1] = c
    return falsed_grid


def slice_it(grid, rowIndex, columnIndex):
    return [row[columnIndex - 1: columnIndex + 2] for row in grid[rowIndex - 1: rowIndex + 2]]


def live_neighbor_count(grid):
    return sum([sum(x) for x in grid]) - int(grid[1][1])


def two_live_neighbors_retains_life(count, life):
    rules = {(0, True) : False, (0, False) : False,
             (1, True): False, (1, False): False,
             (2, True): True, (2, False): False,
             (3, True): False, (3, False): True,
             (4, False): False,
             }
    return rules[(count, life)]


class TestCrazyConwayGame(unittest.TestCase):
    def setUp(self):
        pass

    def test__one_lonely_live_cell_dies_from_loneliness(self):
        grid = [[True]]

        tng = crazy_conway(grid)

        self.assertEqual([[False]], tng)

    def test__two_lonely_horizontal_cells_die_from_loneliness(self):
        grid = [[True, True]]

        tng = crazy_conway(grid)

        self.assertEqual([[False, False]], tng)

    def test__two_lonely_vertical_cells_die_from_loneliness(self):
        grid = [[True], [True]]

        tng = crazy_conway(grid)

        self.assertEqual([[False], [False]], tng)

    def test__one_lonely_cell_with_dead_neighbor_dies(self):
        grid = [[True], [False]]

        tng = crazy_conway(grid)

        self.assertEqual([[False], [False]], tng)

    def test__three_neighbors_spawn_new_friend(self):
        grid = [[True, False],
                [True, True]]

        tng = crazy_conway(grid)

        self.assertEqual([[True, True], [True, True]], tng)

    def test__tainted_puppy_chow_causes_much_death(self):
        grid = [
            [True, False, True],
            [False, False, False],
            [True, False, True],

        ]
        
        expected_grid = [
            [False, False, False],
            [False, False, False],
            [False, False, False],
        ]

        tng = crazy_conway(grid)

        self.assertEqual(expected_grid, tng)

    def test__live_neighbor_count_for_single_cell_is_zero(self):
        grid = [[True]]
        foo = live_neighbor_count(slice_it(pad_grid(grid), 1, 1))

        self.assertEqual(0, foo)

    def test__live_neighbor_count_with_horizontal_true_and_false(self):
        grid = [[True], [False]]
        foo = live_neighbor_count(slice_it(pad_grid(grid), 2, 1))
        self.assertEqual(1, foo)

    def test__live_neighbor_count_with_vertical_true_and_false(self):
        grid = [[True, False]]
        foo = live_neighbor_count(slice_it(pad_grid(grid), 1, 2))
        self.assertEqual(1, foo)

    def test__live_neighbor_count_l_shape(self):
        grid = [[True, False], [True, True]]
        slice = slice_it(pad_grid(grid), 1, 2)
        foo = live_neighbor_count(slice)
        self.assertEqual(3, foo)

    def test__slice(self):
        grid = [[False, False, False, False],
                [False, True, False, False],
                [False, True, True, False],
                [False, False, False, False]]

        expected_grid = [[False, False, False],
                         [True, False, False],
                         [True, True, False]]

        self.assertEqual(expected_grid, slice_it(grid, 1, 2))

    def test__pad_single_cell(self):
        grid = [[True]]
        expected_grid = [[False, False, False], [False, True, False], [False, False, False]]
        self.assertEqual(expected_grid, pad_grid(grid))

    def test__pad_l_shape(self):
        grid = [[True, False], [True, True]]
        expected_grid = [[False, False, False, False],
                         [False, True, False, False],
                         [False, True, True, False],
                         [False, False, False, False]
                         ]
        self.assertEqual(expected_grid, pad_grid(grid))
