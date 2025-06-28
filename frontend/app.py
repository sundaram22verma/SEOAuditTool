import streamlit as st
import re
import subprocess
import json
import time
import os
import pandas as pd
from datetime import datetime
import io

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
    for page in report['pages']:
        # Main page info
        row = {
            'URL': page['url'],
            'Title': page['title'],
            'Meta Description': page['meta_description'],
            'Headings Count': len(page['headings']),
            'Broken Links Count': len(page['broken_links']) if page['broken_links'] else 0
        }
        rows.append(row)
        
        # Add headings as separate rows
        for heading in page['headings']:
            heading_row = {
                'URL': page['url'],
                'Title': page['title'],
                'Meta Description': page['meta_description'],
                'Heading': heading,
                'Broken Links Count': len(page['broken_links']) if page['broken_links'] else 0
            }
            rows.append(heading_row)
        
        # Add broken links as separate rows
        if page['broken_links']:
            for link in page['broken_links']:
                broken_row = {
                    'URL': page['url'],
                    'Title': page['title'],
                    'Meta Description': page['meta_description'],
                    'Broken Link': link,
                    'Headings Count': len(page['headings'])
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
        for page in report['pages']:
            summary_data.append({
                'URL': page['url'],
                'Title': page['title'],
                'Meta Description': page['meta_description'],
                'Headings Count': len(page['headings']),
                'Broken Links Count': len(page['broken_links']) if page['broken_links'] else 0
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Headings sheet
        headings_data = []
        for page in report['pages']:
            for heading in page['headings']:
                headings_data.append({
                    'URL': page['url'],
                    'Heading': heading
                })
        
        headings_df = pd.DataFrame(headings_data)
        headings_df.to_excel(writer, sheet_name='Headings', index=False)
        
        # Broken Links sheet
        broken_links_data = []
        for page in report['pages']:
            if page['broken_links']:
                for link in page['broken_links']:
                    broken_links_data.append({
                        'URL': page['url'],
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
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "shared")
report_path = os.path.join(shared_dir, "report.json")
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
    st.sidebar.write(f"Found report with {len(existing_report['pages'])} pages")
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
            # Ensure shared directory exists
            os.makedirs(shared_dir, exist_ok=True)
            
            # Save URLs to shared/urls.txt
            urls_path = os.path.join(shared_dir, "urls.txt")
            with open(urls_path, "w", encoding="utf-8") as f:
                for u in urls:
                    f.write(u + "\n")
            
            # Remove old report if exists
            if os.path.exists(report_path):
                os.remove(report_path)
            
            # Call Go backend
            try:
                backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")
                result = subprocess.run(["go", "run", "main.go", "--file", urls_path], capture_output=True, text=True, cwd=backend_dir)
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
                        total_pages = len(report['pages'])
                        total_broken_links = sum(len(page['broken_links']) if page['broken_links'] else 0 for page in report['pages'])
                        total_headings = sum(len(page['headings']) for page in report['pages'])
                        
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