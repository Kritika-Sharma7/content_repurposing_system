# 🚀 Quick Start Guide

Get ContentForge AI up and running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Terminal/Command Prompt

## Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/contentforge-ai.git
cd contentforge-ai/multi-agent-content

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key

Create a `.env` file in the `multi-agent-content` directory:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
```

Save and close the file.

## Step 3: Test the Installation

Run with sample content:

```bash
python main.py --sample
```

You should see:
```
[Pipeline] Starting content repurposing pipeline...
[Pipeline] Input: 450 words
[Pipeline] Stage 1/4: Running Summarizer Agent...
  ✓ Title: "The Future of Remote Work: Trust Over Tools"
  ✓ Extracted 7 key points
  ...
[Pipeline] ✅ Pipeline complete!
```

## Step 4: View the Results

Check the `outputs/` directory for generated JSON files:

```bash
# On Windows:
dir outputs\

# On macOS/Linux:
ls outputs/
```

You'll see files like:
- `summary_20260402_143000.json`
- `version_1_20260402_143000.json`
- `review_20260402_143000.json`
- `version_2_20260402_143000.json`

## Step 5: Try the UI

Launch the Streamlit interface:

```bash
streamlit run ui/app.py
```

Open http://localhost:8501 in your browser and you'll see the beautiful web interface!

## 🎯 What to Try Next

### Try Different Input Sources

```bash
# From a text file
python main.py --file article.txt

# From a URL
python main.py --url https://example.com/blog-post

# With direct text
python main.py --input "Your article content here..."
```

### Customize Preferences

```bash
python main.py --sample \
  --tone conversational \
  --audience "startup founders" \
  --platforms linkedin twitter
```

### Export Specific Platforms

```bash
# Only LinkedIn
python main.py --sample --platforms linkedin

# LinkedIn and Twitter only
python main.py --sample --platforms linkedin twitter
```

## 🎨 React UI (Optional)

For a modern frontend experience:

```bash
# Terminal 1: Start backend
python api_server.py

# Terminal 2: Start frontend
cd react-ui
npm install
npm run dev
```

Open http://localhost:5173 for the React UI.

## 📊 Understanding the Output

### Summary (Stage 1)
- **title**: Generated title for your content
- **content_dna**: Core conflict and key question
- **key_points**: 4-8 semantic insights extracted

### Version 1 (Stage 2)
- **LinkedIn**: Hook, body, CTA, hashtags
- **Twitter**: Thread of 5-8 tweets (≤280 chars each)
- **Newsletter**: Subject, intro, body sections, closing

### Review (Stage 3)
- **Scores**: Overall alignment (1-10), consistency (1-10)
- **Issues**: Critical problems identified
- **Improvements**: Suggested changes

### Version 2 (Stage 4)
- **Refined content**: Improved versions of all formats
- **Changes made**: List of improvements applied
- **Addressed issues**: Problems fixed

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Check that `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly
- Make sure no extra spaces around the `=` sign

### "Module not found" error
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Rate limit exceeded"
- OpenAI has rate limits on API usage
- Wait a few minutes and try again
- Check your API key tier/limits

### Results not appearing in `outputs/`
- Check you're in the correct directory
- Verify you didn't use `--no-save` flag
- Check terminal for error messages

## 🎓 Learn More

- **Full Documentation**: See [README.md](README.md)
- **Schema Changes**: See [SCHEMA_MIGRATION.md](SCHEMA_MIGRATION.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md)

## 💡 Pro Tips

1. **Start with sample content** to understand the flow
2. **Check the outputs/ folder** after each run
3. **Use the UI** for the best experience
4. **Experiment with preferences** to see different results
5. **Read the review feedback** to understand quality metrics

## 🎉 You're Ready!

You now have ContentForge AI running locally. Start transforming your long-form content into engaging multi-platform posts!

Need help? Open an issue on [GitHub](https://github.com/yourusername/contentforge-ai/issues) or check the [README](README.md).

Happy content creation! 🚀
