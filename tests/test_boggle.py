from unittest import TestCase
from boggle import Boggle

class BoggleTestCase(TestCase):
    """Tests for functions from boggle.py"""
    
    @classmethod
    def setUpClass(cls):
        cls.testGame = Boggle()
        cls.check_test_board = [["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"]]

    def test_read_dict(self):
        words = self.testGame.read_dict('words.txt')
        self.assertIn('dog', words) 
        self.assertEqual(235886, len(words))

    def test_make_board(self):
        newBoard = self.testGame.make_board()

        self.assertIsInstance(newBoard, list)
        self.assertEqual(len(newBoard), 5)
        for row in newBoard:
            self.assertEqual(len(row), 5)

    def test_check_valid_word(self):
        check = self.testGame.check_valid_word

        self.assertEqual(check(self.check_test_board, 'dog'), 'ok')
        self.assertEqual(check(self.check_test_board, 'cat'), 'not-on-board')
        self.assertEqual(check(self.check_test_board, 'asdf'), 'not-word')
        self.assertEqual(check(self.check_test_board, 'doG'), 'not-word')

    def test_find_from(self):
        board = self.check_test_board

        # searching out of range
        self.assertIsNone(self.testGame.find_from(board, 'DOG',100,100,[]))
 
        # searching in range and word exists
        self.assertTrue(self.testGame.find_from(board, 'DOG',0,0,set()))

        # Word not on board/DNE
        self.assertFalse(self.testGame.find_from(board, 'ASDF',0,0,set()))

        # Letter already seen
        self.assertFalse(self.testGame.find_from(board, 'DOG',0,0,{(0,0)}))

    def test_find(self):
        board = self.check_test_board

        self.assertTrue(self.testGame.find(board,'DOG'))
        self.assertFalse(self.testGame.find(board,'CAT'))
