# AI Agent Project - Groq Implementation

This project is a **Groq conversion** of the AI Agent course from [Boot.dev](https://boot.dev), originally designed to use Google's Gemini API. This implementation leverages Groq's lightning-fast inference speeds and superior rate limits.

## 🚀 Why Groq Over Gemini?

- **Higher Rate Limits**: Groq offers significantly more generous API rate limits
- **Better Key Security**: More secure API key management practices
- **Faster Inference**: Groq's specialized hardware provides exceptional speed
- **Better Developer Experience**: More reliable API responses and error handling

## 📁 Project Structure

This repository contains 14 chapters (lessons) from the Boot.dev AI Agent course, each converted to use Groq:

```
ai_agent_groq/
├── Ch1L3/          # Basic Groq API usage
├── Ch1L4/          # API interaction fundamentals  
├── Ch1L6/          # Enhanced prompting
├── Ch2L1/          # Function calling introduction
├── Ch2L2/          # File system operations
├── Ch2L3/          # File content management
├── Ch2L4/          # File writing capabilities
├── Ch2L5/          # Python execution functions
├── Ch3L1/          # Advanced function calling
├── Ch3L2/          # Multi-function workflows
├── Ch3L3/          # Complex agent behaviors
├── Ch3L4/          # Agent interaction patterns
├── Ch4L1/          # Advanced agent features
└── Ch4L2/          # Final implementation
```

## 🛠 Setup Instructions

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Groq API key

### 2. Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Create a new API key
3. Copy the key (starts with `gsk_`)

### 3. Environment Setup

Each chapter directory contains an `.env.example` file. For any chapter you want to run:

```bash
# Navigate to the chapter directory
cd Ch1L3  # or any chapter you want to try

# Copy the environment template
cp .env.example .env

# Edit the .env file and add your API key
nano .env  # or use your preferred editor
```

Your `.env` file should look like:
```env
# Groq API Configuration
# Get your API key from: https://console.groq.com/keys
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 4. Install Dependencies

Each chapter has its own dependencies managed by `uv`:

```bash
# Navigate to desired chapter
cd Ch1L3

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 5. Run the Examples

```bash
# Basic usage (most chapters)
python main.py "Your prompt here"

# With verbose output (shows token usage)
python main.py "Your prompt here" --verbose

# Example
python main.py "What is artificial intelligence?" --verbose
```

## 📚 Chapter Progression

### **Chapter 1: Fundamentals**
- **Ch1L3**: Basic Groq API integration
- **Ch1L4**: Understanding API responses and token management
- **Ch1L6**: Advanced prompting techniques

### **Chapter 2: Function Calling**
- **Ch2L1**: Introduction to Groq function calling
- **Ch2L2**: File system exploration functions
- **Ch2L3**: Reading file contents
- **Ch2L4**: Writing and modifying files
- **Ch2L5**: Executing Python code dynamically

### **Chapter 3: Advanced Agents**
- **Ch3L1**: Multi-step function workflows
- **Ch3L2**: Complex agent decision-making
- **Ch3L3**: Advanced file operations
- **Ch3L4**: Interactive agent behaviors

### **Chapter 4: Production Features**
- **Ch4L1**: Error handling and robust agents
- **Ch4L2**: Final implementation with all features

## 🔧 Key Differences from Original (Gemini) Version

### API Integration
- **Groq SDK** instead of Google AI SDK
- **Different model names**: `llama3-8b-8192` instead of Gemini models
- **Enhanced function calling**: Groq's improved function calling implementation

### Performance Improvements
- **Faster response times** due to Groq's specialized inference hardware
- **Higher throughput** for batch operations
- **Better rate limiting** for development and testing

### Security Enhancements
- **Environment variable management** with `.env` files
- **Proper API key handling** with better security practices
- **`.gitignore` protection** for sensitive files

## 🔒 Security Notes

- **Never commit API keys** to version control
- **Use `.env` files** for local development (already gitignored)
- **Use environment variables** in production
- **Rotate API keys** regularly

## 🎯 Usage Examples

### Basic Chat
```bash
python main.py "Explain how machine learning works"
```

### File Operations (Ch2L2+)
```bash
python main.py "List all Python files in the current directory"
python main.py "Read the calculator.py file and explain what it does"
```

### Code Execution (Ch2L5+)
```bash
python main.py "Create a simple calculator and test it"
python main.py "Write a function to sort a list and demonstrate it"
```

## 🤝 Contributing

This is an educational project based on Boot.dev's curriculum. Feel free to:

- Report issues with the Groq conversion
- Suggest improvements to the implementation
- Share your learning experience

## 📄 License

This project is for educational purposes, based on the Boot.dev AI Agent course curriculum.

## 🙏 Acknowledgments

- **Boot.dev** for the excellent AI Agent course structure
- **Groq** for providing fast and reliable AI inference
- Original course design adapted from Gemini to Groq implementation

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your `.env` file is in the correct directory
   - Ensure your API key is valid and starts with `gsk_`
   - Check that you've activated the virtual environment

2. **Import Errors**
   - Run `uv sync` to install dependencies
   - Ensure you're in the correct chapter directory
   - Activate the virtual environment

3. **Rate Limiting**
   - Groq has generous limits, but check your usage at [console.groq.com](https://console.groq.com)
   - Use `--verbose` flag to monitor token usage

### Getting Help

- Check the original Boot.dev course for conceptual guidance
- Review Groq's [official documentation](https://console.groq.com/docs)
- Examine the function implementations in each chapter's `/functions/` directory

---

**Happy coding!** 🚀 This implementation showcases the power of Groq's fast inference while following the educational structure of Boot.dev's excellent AI Agent curriculum.
