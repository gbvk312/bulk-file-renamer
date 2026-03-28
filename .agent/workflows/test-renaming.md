---
description: Test Renaming Logic Safely
---

# Workflow: Test Renaming Logic Safely

This workflow ensures that the bulk file renaming logic works as expected without damaging any user files.

## Steps

1. **Create Test Environment**
   - Create a temporary directory `test_files_renamer`.
   - Populated it with dummy files (e.g., `file_1.txt`, `image_2.jpg`, `data_3.csv`).
   
2. **Run Pattern Tests**
   - Execute the `renamer_logic.py` with specific patterns (e.g., `test_{index}{ext}`).
   - Verify that the files in the temporary directory are renamed correctly.

3. **Run AI Tests (Mocked)**
   - Run the AI renaming logic using a mock response from `ai_engine.py` to verify the flow.

4. **Verify Rollback/Preview**
   - Test that the preview functionality correctly identifies potential name collisions.
   
5. **Clean Up**
   - Delete the `test_files_renamer` directory.
