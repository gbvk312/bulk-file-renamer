import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self, model_type="gemini"):
        self.model_type = model_type
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
        
        if self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)

    def generate_names(self, file_names, prompt):
        """
        Generate new file names for the given list of original names based on a prompt.
        file_names: list of strings (filenames with extensions).
        prompt: user string describing the renaming rule.
        Returns a list of suggested names.
        """
        if not file_names:
            return []

        # Construct the context for the AI
        file_list_str = "\n".join(file_names)
        full_prompt = f"""
Given a list of file names, suggest new names for them based on the following instructions: "{prompt}"

Rules:
1. Provide exactly one name per line.
2. The number of output lines must match the number of input file names.
3. Keep the original file extension unless the instructions explicitly ask to change it.
4. Do not include any explanation or extra text, just the list of proposed names.

Input file names:
{file_list_str}
"""

        try:
            if self.model_type == "gemini" and self.gemini_key:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(full_prompt)
                suggested_names = response.text.strip().split("\n")
            elif self.model_type == "openai" and self.openai_key:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                suggested_names = response.choices[0].message.content.strip().split("\n")
            else:
                # Mock or error handling
                return [f"AI_suggest_{i}{os.path.splitext(f)[1]}" for i, f in enumerate(file_names)]
            
            # Basic validation: ensure the length matches
            if len(suggested_names) != len(file_names):
                # If AI failed to provide exact match, fallback to some logic or error
                return [f"AI_error_{i}_original_{f}" for i, f in enumerate(file_names)]
            
            return [name.strip() for name in suggested_names]

        except Exception as e:
            # Fallback for errors
            print(f"AI Error: {e}")
            return [f"AI_failed_{i}{os.path.splitext(f)[1]}" for i, f in enumerate(file_names)]
