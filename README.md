# 🔍 SEO Audit Tool

A comprehensive SEO analysis tool built with **Streamlit** and **Go**, designed to run without any database integration. All data is processed locally and can be downloaded in multiple formats.

## ✨ Features

- **🔍 Comprehensive SEO Analysis**: Title tags, meta descriptions, headings, broken links
- **📊 Multiple Export Formats**: JSON, CSV, and Excel downloads
- **🚀 No Database Required**: Session-based data storage
- **📱 User-Friendly Interface**: Clean Streamlit UI with real-time feedback
- **⚡ Fast Processing**: Go backend for efficient web scraping
- **📋 Batch Processing**: Support for multiple URLs via file upload

## 🏗️ Architecture

```
Frontend (Streamlit) ←→ Backend (Go)
       ↓                    ↓
Session State         File Processing
       ↓                    ↓
Download Reports      JSON Output
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SEOAuditTool
   ```

2. **Install Python dependencies**
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

3. **Install Go dependencies**
   ```bash
   cd ../backend
   go mod tidy
   ```

4. **Run the application**
   ```bash
   cd ../frontend
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file path to: `frontend/app.py`
5. Deploy!

## 📁 Project Structure

```
SEOAuditTool/
├── frontend/
│   ├── app.py              # Streamlit application
│   └── requirements.txt    # Python dependencies
├── backend/
│   ├── main.go            # Go backend for SEO analysis
│   ├── go.mod             # Go module file
│   └── go.sum             # Go dependencies
├── shared/                # Temporary file storage
│   ├── report.json        # Generated reports
│   └── urls.txt          # Input URLs
├── .streamlit/            # Streamlit configuration
│   ├── config.toml
│   └── secrets.toml
└── README.md
```

## 🎯 Usage

1. **Enter URLs**: Type a single URL or upload a .txt file with multiple URLs
2. **Run Audit**: Click the "Run Audit" button
3. **View Results**: See summary metrics and detailed analysis
4. **Download**: Export results as JSON, CSV, or Excel files

## 📊 What Gets Analyzed

- **Page Title**: Length and content analysis
- **Meta Description**: Length and content analysis
- **Headings**: H1-H6 structure and content
- **Broken Links**: Internal and external link validation
- **URL Structure**: SEO-friendly URL analysis

## 🔧 Technical Details

### Frontend (Streamlit)
- **Framework**: Streamlit
- **Data Processing**: Pandas for CSV/Excel generation
- **Session Management**: Streamlit session state
- **File Handling**: Temporary file operations

### Backend (Go)
- **Language**: Go
- **Web Scraping**: HTTP client for page analysis
- **HTML Parsing**: Goquery for DOM manipulation
- **Output**: JSON format for data exchange

### Data Flow
1. User inputs URLs in Streamlit
2. URLs saved to `shared/urls.txt`
3. Go backend processes each URL
4. Results saved to `shared/report.json`
5. Streamlit reads and displays results
6. User can download in multiple formats

## 🛡️ Security & Privacy

- **No Database**: No persistent data storage
- **Local Processing**: All analysis happens locally
- **Session-Based**: Data only persists during the session
- **No External APIs**: Self-contained analysis

## 📈 Performance

- **Concurrent Processing**: Go backend handles multiple URLs efficiently
- **Timeout Protection**: 5-minute timeout for large audits
- **Memory Efficient**: Streamlit session state management
- **Fast Downloads**: Optimized file generation

## 🐛 Troubleshooting

### Common Issues

**Backend not found**
- Ensure Go is installed
- Check if `backend/main.go` exists

**Audit timeout**
- Reduce number of URLs
- Check network connectivity

**Import errors**
- Verify all dependencies in `requirements.txt`
- Check Python environment

### Error Messages

- "Backend error" → Check Go backend logs
- "Report not generated" → Verify file permissions
- "Timeout expired" → Try with fewer URLs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the deployment guide
3. Open an issue on GitHub

---

**Ready to audit your SEO!** 🚀 