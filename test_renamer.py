import unittest
import os
import shutil
from renamer_logic import RenamerLogic

class TestRenamerLogic(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = "test_files_renamer"
        os.makedirs(self.test_dir, exist_ok=True)
        # Create some dummy files
        for i in range(1, 4):
            with open(os.path.join(self.test_dir, f"file_{i}.txt"), 'w') as f:
                f.write(f"Content for file {i}")

        self.logic = RenamerLogic(self.test_dir)

    def tearDown(self):
        # Clean up the temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_pattern_renaming_index(self):
        pattern = "renamed_{index}{ext}"
        self.logic.refresh_files()
        preview = self.logic.generate_preview(pattern)
        
        # Verify the suggestions
        self.assertEqual(len(preview), 3)
        self.assertEqual(preview[0][1], "renamed_1.txt") # Assuming index starts at 1, padding based on 3 files (len('3')=1)
        self.assertEqual(preview[1][1], "renamed_2.txt")
        self.assertEqual(preview[2][1], "renamed_3.txt")

    def test_pattern_renaming_original(self):
        pattern = "copy_{original}_backup{ext}"
        self.logic.refresh_files()
        preview = self.logic.generate_preview(pattern)
        
        self.assertEqual(preview[0][1], "copy_file_1_backup.txt")
        self.assertEqual(preview[1][1], "copy_file_2_backup.txt")

    def test_apply_renaming(self):
        self.logic.refresh_files()
        rename_map = [("file_1.txt", "file_one.txt"), ("file_2.txt", "file_two.txt")]
        results = self.logic.apply_renaming(rename_map)
        
        self.assertEqual(results[0][1], "success")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "file_one.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "file_1.txt")))

    def test_conflict_detection(self):
        self.logic.refresh_files()
        # Pretend we want to rename file_1.txt to file_2.txt, but file_2.txt already exists
        rename_map = [("file_1.txt", "file_2.txt")]
        results = self.logic.apply_renaming(rename_map)
        
        self.assertIn("error", results[0][1])
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "file_1.txt")))

if __name__ == "__main__":
    unittest.main()
