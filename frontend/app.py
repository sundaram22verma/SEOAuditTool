import streamlit as st
import re
import subprocess
import json
import time
import os
import pandas as pd
from datetime import datetime
import io

# Configure page
st.set_page_config(
    page_title="SEO Audit Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of frontend)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Define shared directory path
SHARED_DIR = os.path.join(PROJECT_ROOT, "shared")

# Ensure shared directory exists
os.makedirs(SHARED_DIR, exist_ok=True)

def is_valid_url(url):
    return re.match(r"^https?://", url)

def extract_urls_from_text(text):
    """Extract URLs from text that may contain numbered lines or other formatting."""
    # Find all URLs that start with http:// or https://
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return [url.strip() for url in urls if url.strip()]

def create_csv_download(report):
    """Create CSV data from the audit report."""
    rows = []
    for page in report.get('pages', []):
        # Main page info
        row = {
            'URL': page.get('url', ''),
            'Title': page.get('title', ''),
            'Meta Description': page.get('meta_description', ''),
            'Headings Count': len(page.get('headings', [])),
            'Broken Links Count': len(page.get('broken_links', []))
        }
        rows.append(row)
        
        # Add headings as separate rows
        for heading in page.get('headings', []):
            heading_row = {
                'URL': page.get('url', ''),
                'Title': page.get('title', ''),
                'Meta Description': page.get('meta_description', ''),
                'Heading': heading,
                'Broken Links Count': len(page.get('broken_links', []))
            }
            rows.append(heading_row)
        
        # Add broken links as separate rows
        for link in page.get('broken_links', []):
            broken_row = {
                'URL': page.get('url', ''),
                'Title': page.get('title', ''),
                'Meta Description': page.get('meta_description', ''),
                'Broken Link': link,
                'Headings Count': len(page.get('headings', []))
            }
            rows.append(broken_row)
    
    return pd.DataFrame(rows)

def create_excel_download(report):
    """Create Excel data from the audit report with multiple sheets."""
    # Create a BytesIO object to store the Excel file
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = []
        for page in report.get('pages', []):
            summary_data.append({
                'URL': page.get('url', ''),
                'Title': page.get('title', ''),
                'Meta Description': page.get('meta_description', ''),
                'Headings Count': len(page.get('headings', [])),
                'Broken Links Count': len(page.get('broken_links', []))
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Headings sheet
        headings_data = []
        for page in report.get('pages', []):
            for heading in page.get('headings', []):
                headings_data.append({
                    'URL': page.get('url', ''),
                    'Heading': heading
                })
        
        headings_df = pd.DataFrame(headings_data)
        headings_df.to_excel(writer, sheet_name='Headings', index=False)
        
        # Broken Links sheet
        broken_links_data = []
        for page in report.get('pages', []):
            for link in page.get('broken_links', []):
                broken_links_data.append({
                    'URL': page.get('url', ''),
                    'Broken Link': link
                })
        
        if broken_links_data:
            broken_links_df = pd.DataFrame(broken_links_data)
            broken_links_df.to_excel(writer, sheet_name='Broken Links', index=False)
    
    output.seek(0)
    return output

def show_download_section(report):
    """Display download buttons for the report."""
    st.markdown("---")
    st.subheader("📥 Download Report")
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # JSON Download
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"seo_audit_report_{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # CSV Download
        try:
            csv_df = create_csv_download(report)
            csv_data = csv_df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name=f"seo_audit_report_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error creating CSV: {e}")
    
    with col3:
        # Excel Download
        try:
            excel_data = create_excel_download(report)
            st.download_button(
                label="📈 Download Excel",
                data=excel_data.getvalue(),
                file_name=f"seo_audit_report_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error creating Excel file: {e}")

st.title("🔍 SEO Audit Tool")

# Check if there's an existing report
report_path = os.path.join(SHARED_DIR, "report.json")
existing_report = None
if os.path.exists(report_path):
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            existing_report = json.load(f)
    except:
        pass

# Sidebar for existing report download
if existing_report:
    st.sidebar.subheader("📋 Previous Report")
    st.sidebar.write(f"Found report with {len(existing_report.get('pages', []))} pages")
    if st.sidebar.button("📥 Download Previous Report"):
        show_download_section(existing_report)
        st.sidebar.success("Download section added below!")

st.write("Enter a URL or upload a .txt file with URLs (one per line):")

url_input = st.text_input("URL:")
file_upload = st.file_uploader("Or upload .txt file", type=["txt"])

urls = []
if url_input:
    urls.append(url_input.strip())
if file_upload:
    content = file_upload.read().decode("utf-8")
    urls += extract_urls_from_text(content)

if st.button("🚀 Run Audit"):
    if not urls:
        st.error("Please enter a URL or upload a .txt file.")
    elif not all(is_valid_url(u) for u in urls):
        st.error("All URLs must start with http:// or https://")
    else:
        with st.spinner("Running SEO audit..."):
            # Save URLs to shared/urls.txt
            urls_path = os.path.join(SHARED_DIR, "urls.txt")
            with open(urls_path, "w", encoding="utf-8") as f:
                for u in urls:
                    f.write(u + "\n")
            # Remove old report if exists
            report_path = os.path.join(SHARED_DIR, "report.json")
            if os.path.exists(report_path):
                os.remove(report_path)
            # Call Go backend
            try:
                backend_dir = os.path.join(PROJECT_ROOT, "backend")
                # Set environment variable for shared directory
                env = os.environ.copy()
                env['SHARED_DIR'] = SHARED_DIR
                result = subprocess.run(["go", "run", "main.go", "--file", urls_path], capture_output=True, text=True, cwd=backend_dir, env=env)
                if result.returncode != 0:
                    st.error(f"Backend error: {result.stderr}")
                else:
                    # Wait for report.json (max 10s)
                    for _ in range(20):
                        if os.path.exists(report_path):
                            break
                        time.sleep(0.5)
                    if os.path.exists(report_path):
                        with open(report_path, "r", encoding="utf-8") as f:
                            report = json.load(f)
                        st.success("✅ Audit complete!")
                        
                        # Display summary
                        st.subheader("📊 Audit Summary")
                        total_pages = len(report.get('pages', []))
                        total_broken_links = sum(len(page.get('broken_links', [])) for page in report.get('pages', []))
                        total_headings = sum(len(page.get('headings', [])) for page in report.get('pages', []))
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Pages Audited", total_pages)
                        with col2:
                            st.metric("Total Headings", total_headings)
                        with col3:
                            st.metric("Broken Links Found", total_broken_links)
                        
                        # Show detailed results
                        st.subheader("📋 Detailed Results")
                        st.json(report)
                        
                        # Show download section
                        show_download_section(report)
                        
                    else:
                        st.error("Report not generated.")
            except Exception as e:
                st.error(f"Error running backend: {e}")