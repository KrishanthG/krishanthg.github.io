import os
from datetime import datetime

# Base URL of your live portfolio
BASE_URL = "https://krishanthg.github.io/"

# Files to ignore (don't include templates or components if any)
IGNORE_FILES = ["article-template.html"]

def generate_sitemap():
    directory = "."
    sitemap_path = "sitemap.xml"
    
    # XML Header
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Find all .html files
    html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f not in IGNORE_FILES]
    
    for file in html_files:
        # Determine priority and changefreq based on file type
        if file == "index.html":
            priority = "1.0"
            changefreq = "weekly"
            url = BASE_URL
        else:
            priority = "0.8"
            changefreq = "monthly"
            url = f"{BASE_URL}{file}"
            
        # Get last modified date of the file
        timestamp = os.path.getmtime(os.path.join(directory, file))
        lastmod = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        # Build the URL entry
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url}</loc>\n'
        xml_content += f'    <lastmod>{lastmod}</lastmod>\n'
        xml_content += f'    <changefreq>{changefreq}</changefreq>\n'
        xml_content += f'    <priority>{priority}</priority>\n'
        xml_content += '  </url>\n'
        
    xml_content += '</urlset>'
    
    # Write to sitemap.xml
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"Successfully generated sitemap.xml with {len(html_files)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
