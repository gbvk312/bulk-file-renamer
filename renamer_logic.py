import os
import re
from datetime import datetime

class RenamerLogic:
    def __init__(self, directory):
        self.directory = directory
        self.files = []
        self.refresh_files()

    def refresh_files(self):
        """Update the list of files in the directory."""
        if not os.path.isdir(self.directory):
            self.files = []
            return
        self.files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        self.files.sort()

    def generate_preview(self, pattern, selected_files=None):
        """
        Generate a preview of renamed files based on the pattern.
        Returns a list of tuples: (original_name, suggested_name, status).
        """
        if selected_files is None:
            selected_files = self.files

        preview = []
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        
        # Determine the padding based on the number of files
        total_files = len(selected_files)
        padding = len(str(total_files))

        for i, original_name in enumerate(selected_files):
            name_no_ext, ext = os.path.splitext(original_name)
            
            # Format the index
            index_str = str(i + 1).zfill(padding)
            
            # Replace variables in the pattern
            new_name = pattern
            new_name = new_name.replace("{index}", index_str)
            new_name = new_name.replace("{date}", date_str)
            new_name = new_name.replace("{time}", time_str)
            new_name = new_name.replace("{original}", name_no_ext)
            new_name = new_name.replace("{ext}", ext)
            
            # Simple conflict detection within the preview set
            status = "ready"
            if new_name == original_name:
                status = "no_change"
            
            preview.append((original_name, new_name, status))
            
        return preview

    def apply_renaming(self, rename_map):
        """
        Apply the renaming.
        rename_map: list of (original, new) tuples.
        Returns a list of (original, result_status).
        """
        results = []
        for original, new in rename_map:
            old_path = os.path.join(self.directory, original)
            new_path = os.path.join(self.directory, new)
            
            try:
                if old_path == new_path:
                    results.append((original, "skipped"))
                    continue
                    
                if os.path.exists(new_path):
                    results.append((original, f"error: skip as '{new}' already exists"))
                    continue
                
                os.rename(old_path, new_path)
                results.append((original, "success"))
            except Exception as e:
                results.append((original, f"error: {str(e)}"))
        
        self.refresh_files()
        return results
