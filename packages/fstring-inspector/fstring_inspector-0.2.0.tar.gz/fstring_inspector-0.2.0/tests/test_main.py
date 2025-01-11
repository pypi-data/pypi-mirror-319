import unittest
import tempfile
import os
from pathlib import Path
from fstring_inspector import inspect_fstring, inspect_file, inspect_directory


class TestFStringInspection(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for file-based tests
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after tests
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_inspect_fstring_with_nested_double_quotes(self):
        # Should detect problematic nested double quotes
        line = 'print(f"This is a "nested" quote")'
        result = inspect_fstring(line)
        self.assertEqual(result, line)

    def test_inspect_fstring_with_nested_single_quotes(self):
        # Should detect problematic nested single quotes
        line = "print(f'This is a 'nested' quote')"
        result = inspect_fstring(line)
        self.assertEqual(result, line)

    def test_inspect_fstring_with_mixed_quotes(self):
        # Should not detect any issues with mixed quotes
        line = "print(f\"This is a 'valid' quote\")"
        result = inspect_fstring(line)
        self.assertIsNone(result)

    def test_inspect_fstring_without_nesting(self):
        # Should not detect any issues with simple f-strings
        line = 'print(f"Simple fstring")'
        result = inspect_fstring(line)
        self.assertIsNone(result)

    def test_inspect_fstring_with_curly_braces(self):
        # Should not detect issues with f-strings containing expressions
        line = 'print(f"Value: {1 + 1}")'
        result = inspect_fstring(line)
        self.assertIsNone(result)

    def test_inspect_file(self):
        # Create a temporary file with test content
        test_file = Path(self.temp_dir) / "test.py"
        content = """
            print("Normal string")
            print(f"Normal f-string")
            print(f"Problem "here" with quotes")
            print(f'Another "valid" string')
        """
        with open(test_file, "w") as f:
            f.write(content)

        results = inspect_file(test_file)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 4)  # Line number
        self.assertTrue('Problem "here" with quotes' in results[0][1])

    def test_inspect_directory(self):
        # Create test directory structure with multiple files
        test_dir = Path(self.temp_dir) / "test_dir"
        test_dir.mkdir()

        # Create a file with issues
        file1 = test_dir / "file1.py"
        with open(file1, "w") as f:
            f.write('print(f"Problem "here" exists")\n')

        # Create a file without issues
        file2 = test_dir / "file2.py"
        with open(file2, "w") as f:
            f.write('print(f"No problem here")\n')

        # Create a non-Python file
        file3 = test_dir / "file3.txt"
        with open(file3, "w") as f:
            f.write('print(f"Problem "here" exists")\n')

        results = inspect_directory(test_dir)
        self.assertEqual(len(results), 1)  # Only one file should have issues
        self.assertTrue(str(file1) in results)
        self.assertTrue(str(file2) not in results)

    def test_inspect_directory_with_nested_directories(self):
        # Test nested directory structure
        test_dir = Path(self.temp_dir) / "nested_test_dir"
        test_dir.mkdir()
        nested_dir = test_dir / "nested"
        nested_dir.mkdir()

        # Create files in both directories
        file1 = test_dir / "file1.py"
        with open(file1, "w") as f:
            f.write('print(f"Problem "here" exists")\n')

        file2 = nested_dir / "file2.py"
        with open(file2, "w") as f:
            f.write('print(f"Another "problem" here")\n')

        results = inspect_directory(test_dir)
        self.assertEqual(len(results), 2)  # Both files should have issues
        self.assertTrue(str(file1) in results)
        self.assertTrue(str(file2) in results)

    def test_inspect_file_with_invalid_path(self):
        # Test handling of non-existent file
        with self.assertRaises(FileNotFoundError):
            inspect_file("nonexistent.py")


if __name__ == "__main__":
    unittest.main()
