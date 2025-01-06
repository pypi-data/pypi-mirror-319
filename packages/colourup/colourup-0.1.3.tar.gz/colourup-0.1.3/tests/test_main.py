import unittest
from unittest.mock import patch
import colourup
import io


class TestColourup(unittest.TestCase):
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_title(self, mock_stdout):
        colourup.title("Test Title", "-", 8, True)

        expected_output = "\n-------- Test Title --------\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdin")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_pinput_custom_prompt(self, mock_stdout, mock_stdin):
        mock_stdin.readline.return_value = "test"

        result = colourup.pinput("What's your name?", "?>")
        self.assertEqual(result, "test")

        expected_output = "\nWhat's your name?\n?> "
        self.assertEqual(mock_stdout.getvalue(), expected_output)

        mock_stdin.readline.assert_called_once()

    @patch("sys.stdin")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_pinput_default(self, mock_stdout, mock_stdin):
        mock_stdin.readline.return_value = "test"

        result = colourup.pinput("Question?")
        self.assertEqual(result, "test")

        expected_output = "\nQuestion?\n>> "
        self.assertEqual(mock_stdout.getvalue(), expected_output)

        mock_stdin.readline.assert_called_once()


if __name__ == "__main__":
    unittest.main()
