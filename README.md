# 🔍 SEO Audit Tool

A comprehensive SEO auditing tool that analyzes websites for SEO best practices, broken links, and provides detailed reports. Built with Go backend for web scraping and Python Streamlit frontend for user interface.

## 🚀 Features

- **Web Scraping**: Automated analysis of web pages using Go's Colly framework
- **SEO Analysis**: Checks for title tags, meta descriptions, heading structure
- **Broken Link Detection**: Identifies and reports broken links with status codes
- **Multiple Input Methods**: Support for single URLs or batch processing via text files
- **Interactive Dashboard**: Beautiful Streamlit-based user interface
- **Export Options**: Download reports in JSON, CSV, and Excel formats
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📁 Project Structure

```
SEOAuditTool/
├── backend/                 # Go backend for web scraping
│   ├── main.go             # Main Go application
│   ├── go.mod              # Go module dependencies
│   └── go.sum              # Go dependency checksums
├── frontend/               # Python Streamlit frontend
│   ├── app.py              # Main Streamlit application
│   └── requirements.txt    # Python dependencies
├── shared/                 # Shared data between backend and frontend
│   ├── report.json         # Generated audit reports
│   └── urls.txt            # Input URLs file
└── myenv/                  # Python virtual environment
```

## 🛠️ Installation

### Prerequisites

- **Go 1.23+** - [Download here](https://golang.org/dl/)
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Backend Setup (Go)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Go dependencies:
   ```bash
   go mod download
   ```

3. Build the application:
   ```bash
   go build -o seo-audit-tool main.go
   ```

### Frontend Setup (Python)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv myenv
   myenv\Scripts\activate

   # macOS/Linux
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Method 1: Web Interface (Recommended)

1. Start the Streamlit frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter a URL or upload a text file with URLs (one per line)

4. Click "Run Audit" to start the analysis

5. View results and download reports in various formats

### Method 2: Command Line

1. Run the Go backend directly:
   ```bash
   cd backend
   go run main.go https://example.com
   ```

2. Or process multiple URLs from a file:
   ```bash
   go run main.go -file urls.txt
   ```

3. The report will be generated in `shared/report.json`

## 📊 What the Tool Analyzes

### SEO Elements
- **Page Title**: Checks for presence and content of `<title>` tags
- **Meta Description**: Analyzes meta description tags for SEO optimization
- **Heading Structure**: Examines H1-H6 tags for proper hierarchy
- **Content Structure**: Identifies heading patterns and content organization

### Technical Issues
- **Broken Links**: Detects links that return 4xx or 5xx status codes
- **Link Validation**: Tests both internal and external links
- **Response Times**: Monitors page load performance

### Report Features
- **Comprehensive Analysis**: Detailed breakdown of each analyzed page
- **Multiple Export Formats**: JSON, CSV, and Excel downloads
- **Timestamped Reports**: Each report includes generation timestamp
- **Error Handling**: Graceful handling of inaccessible pages

## 📋 Input Format

### Single URL
```
https://example.com
```

### Multiple URLs (text file)
```
https://example.com
https://example.com/page1
https://example.com/page2
https://another-site.com
```

## 📈 Output Format

The tool generates structured reports containing:

```json
{
  "pages": [
    {
      "url": "https://example.com",
      "title": "Example Page Title",
      "meta_description": "Page meta description",
      "headings": [
        "H1: Main Heading",
        "H2: Sub Heading",
        "H3: Section Heading"
      ],
      "broken_links": [
        "https://broken-link.com [status: 404]",
        "https://another-broken.com [status: 500]"
      ]
    }
  ]
}
```

## 🔧 Configuration

### Backend Configuration
- **Timeout**: HTTP client timeout is set to 5 seconds
- **User Agent**: Uses default Colly user agent
- **Rate Limiting**: Built-in rate limiting to be respectful to servers

### Frontend Configuration
- **Port**: Streamlit runs on port 8501 by default
- **Theme**: Modern, clean interface with dark/light mode support
- **File Upload**: Supports .txt files up to 200MB

## 🐛 Troubleshooting

### Common Issues

1. **Go build errors**:
   - Ensure Go 1.23+ is installed
   - Run `go mod tidy` to clean dependencies

2. **Python import errors**:
   - Activate virtual environment: `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (macOS/Linux)
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Permission errors**:
   - Ensure write permissions to the `shared/` directory
   - Run as administrator if needed (Windows)

4. **Network issues**:
   - Check firewall settings
   - Verify internet connectivity
   - Some sites may block automated requests

### Performance Tips

- **Large URL lists**: Process in batches of 50-100 URLs
- **Rate limiting**: The tool includes built-in delays to be respectful
- **Memory usage**: Monitor system resources for large audits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Colly**: Go web scraping framework
- **Streamlit**: Python web app framework
- **Pandas**: Data manipulation library
- **OpenPyXL**: Excel file handling

## 📞 Support

For issues, questions, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the code comments for implementation details

---

**Happy SEO Auditing! 🎯** 