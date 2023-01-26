from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# Don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


# Testing Class Methods
class BoggleTests(TestCase):

    def setUp(self):
        """Set up for each test - instantiate Boggle class as self.test_boggle"""
        self.test_boggle = Boggle();
        print(self.test_boggle);

    def tearDown(self):
        """Tear down for each test - delete Boggle class as self.test_boggle"""
        del self.test_boggle

    def test__init__(self):
        """Test that Boggle class can be initialized"""
        self.assertTrue(self.test_boggle)

    def test_read_dict(self):
        """Test that instance of Boggle class can implement read_dict method"""
        self.assertIn("aardvark", self.test_boggle.read_dict("words.txt"), True)
        self.assertIn("pentachromic", self.test_boggle.read_dict("words.txt"), True)
        self.assertIn("zymurgy", self.test_boggle.read_dict("words.txt"), True)

    def test_make_board(self):
        """Test that instance of Boggle class can implement make_board method"""

        # Checking colomn height
        self.assertTrue(len(self.test_boggle.make_board()), 5)

        # Checking each row length
        for row in (self.test_boggle.make_board()):
            self.assertTrue(len(row), 5)
        
    def test_check_valid_word(self):
        """Test that instance of Boggle class can implement check_valid_word method"""
        self.test_boggle.test_board = [
                    ['G', 'M', 'E', 'X', 'X'],
                    ['A', 'H', 'X', 'X', 'X'],
                    ['X', 'X', 'E', 'X', 'X'],
                    ['X', 'D', 'A', 'Y', 'X'],
                    ['X', 'R', 'X', 'O', 'B']
                    ]
        print(self.test_boggle.test_board)
        self.assertEqual(self.test_boggle.check_valid_word(self.test_boggle.test_board, "fish" ), "not-on-board")
        self.assertEqual(self.test_boggle.check_valid_word(self.test_boggle.test_board, "georgecostanza" ), "not-word")
        self.assertEqual(self.test_boggle.check_valid_word(self.test_boggle.test_board, "game" ), "ok")
        self.assertEqual(self.test_boggle.check_valid_word(self.test_boggle.test_board, "board" ), "ok")

    # Come back and add more if time permits -
    # self.test)boggle.find_from
    # self.test)boggle.find


# Testing View Functions
class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_home_page(self):
        """Test that home_page responds with home.html"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1> Press "Start" to play Boggle!</h1>', html)
        self.assertIn('<a href="/board"><button>Start</button></a>', html)

    def test_game_board(self):
        """Test that game_board responds with board.html"""
        with app.test_client() as client:
            resp = client.get('/board')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<form id="guess-submit" action="" method="POST">', html)
        self.assertIn('<p id="guess-response-message">', html)
        self.assertIn('<p>Your Valid Guesses:</p>', html)
        self.assertIn('<ul id="valid-word-list">', html)

    def test_check_word(self):
        """
        Test that check_word responds with appropriate JSON for each case:
        'ok'
        'not-on-board'
        'not-word'
        """
        with app.test_client() as client:
            with client.session_transaction() as faux_board:
                faux_board['board'] = [
                    ['G', 'M', 'E', 'X', 'X'],
                    ['A', 'H', 'X', 'X', 'X'],
                    ['X', 'X', 'E', 'X', 'X'],
                    ['X', 'D', 'A', 'Y', 'X'],
                    ['X', 'R', 'X', 'O', 'B']
                    ]
            resp = client.get('/check-word?word=game')
            self.assertEqual(resp.json['result'], 'ok')
            resp = client.get('/check-word?word=board')
            self.assertEqual(resp.json['result'], 'ok')
            resp = client.get('/check-word?word=hey')
            self.assertEqual(resp.json['result'], 'ok')
            resp = client.get('/check-word?word=fish')
            self.assertEqual(resp.json['result'], 'not-on-board')
            resp = client.get('/check-word?word=georgecostanza')
            self.assertEqual(resp.json['result'], 'not-word')

    # def test_post_score(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as faux_score:
    #             faux_score[]
    #         resp = client.post('/post-new-score')
    #         html = resp.get_data(as_text=True)

    #         print(html)