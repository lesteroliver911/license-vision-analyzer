# License Vision Analyzer

A Streamlit app using Google Gemini Flash Thinking multimodal model to intelligently extract and analyze user-specified entities from driver's licenses through natural language prompts, delivering structured results with step-by-step reasoning.

## Quick Start

```bash
# Clone repository
git clone https://github.com/lesteroliver911/license-vision-analyzer.git
cd license-vision-analyzer

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run application
streamlit run app.py
```

## Features

- Natural language prompts for custom entity extraction
- Real-time image preview
- Structured analysis output
- One-click result downloads
- Comprehensive error handling

## Usage

1. Upload license image (sidebar)
2. Enter analysis prompt (e.g., "extract name and expiration date")
3. Click "Analyze License"
4. View/download results

## Technical Stack

- **Model**: gemini-2.0-flash-thinking-exp-1219
- **Frontend**: Streamlit
- **Image Processing**: Pillow
- **Supported Formats**: JPG, JPEG, PNG

## Limitations

- Requires clear, well-lit images
- Text must be readable
- No glare/reflections
- Complete license image required

## License

MIT

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request
