# Bulk File Renamer

A powerful, user-friendly desktop application for bulk renaming files with advanced features like AI-powered renaming, pattern matching, and batch operations.

## Features

- **AI-Powered Renaming**: Use AI to automatically generate meaningful file names based on file content or context
- **Pattern-Based Renaming**: Define custom patterns with variables (index, date, original name, etc.)
- **Batch Operations**: Rename multiple files at once with preview and confirmation
- **File Management**: Search, filter, and organize files before renaming
- **Multi-Platform**: Works on macOS, Windows, and Linux

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/gbvk/bulk-file-renamer.git
   cd bulk-file-renamer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Basic Usage

1. Launch the application: `python main.py`
2. Select the folder containing the files you want to rename
3. Choose your renaming method:
   - **AI Rename**: Click "AI Rename" and follow the prompts
   - **Pattern Rename**: Enter a pattern in the "Pattern" field
4. Preview the changes in the "Preview" section
5. Click "Apply Changes" to rename the files

### AI Renaming

1. Select "AI Rename" from the main menu
2. Choose the AI model (OpenAI or Gemini)
3. Enter a prompt describing how you want to rename the files
4. Click "Generate Names" to preview AI-generated names
5. Review and click "Apply Changes"

### Pattern Renaming

Use patterns with these variables:
- `{index}` - Sequential number (001, 002, etc.)
- `{date}` - Current date (YYYY-MM-DD)
- `{time}` - Current time (HH-MM-SS)
- `{original}` - Original file name
- `{ext}` - File extension

**Examples:**
- `photo_{date}_{index}{ext}` → `photo_2023-10-27_001.jpg`
- `report_{original}` → `report_Q3_financials.pdf`

## Configuration

Create a `.env` file in the project root for API keys:

```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Development

### Adding New Features

1. Create a new branch: `git checkout -b feature/new-feature`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

### Testing

Run the test suite:
```bash
python -m unittest test_renamer.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Support

For issues or questions, please open an issue on GitHub.