import unittest


class TestOut(unittest.TestCase):

    def test_happy_path(self):
        self.assertEqual('happy', 'happy', msg='We are not happy')

    def test_should_time_out(self):
        # self.assertEqual('not all things', 'are equal', 'inequality now!')
        pass

    def test_should_fail_to_parse(self):
        pass


if __name__ == '__main__':
    unittest.main()
