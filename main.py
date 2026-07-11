import os
import re
import time
import requests

# Dictionary mapping complex names to their official web domains or clear sub-names
domain_mappings = {
    "Accenture": "accenture.com",
    "Anna University Chennai": "annauniv.edu",
    "Canva": "canva.com",
    "Coding Ninjas": "codingninjas.com",
    "Cognitive Class (IBM course delivery)": "cognitiveclass.ai",
    "Coursera": "coursera.org",
    "CS50 (Harvard University)": "harvard.edu",
    "Department of Science & Technology, Government of India": "dst.gov.in",
    "Edunet Foundation": "edunetfoundation.org",
    "European Space Agency - ESA": "esa.int",
    "Google / Google Cloud Community India": "google.com",
    "Government of Tamil Nadu": "tn.gov.in",
    "HackerRank": "hackerrank.com",
    "HCL GUVI": "guvi.in",
    "HP": "hp.com",
    "IBM": "ibm.com",
    "Indian Space Research Organisation (ISRO)": "isro.gov.in",
    "LinkedIn": "linkedin.com",
    "Microsoft": "microsoft.com",
    "Ministry of Education, Government of India": "education.gov.in",
    "MyGov India": "mygov.in",
    "Naan Mudhalvan": "naanmudhalvan.tn.gov.in",
    "National Association of State Boards of Accountancy (NASBA)": "nasba.org",
    "NITI Aayog": "niti.gov.in",
    "NPTEL (in collaboration with IITM)": "nptel.ac.in",
    "ProProfs": "proprofs.com",
    "Programming Hub": "programminghub.io",
    "Project Management Institute": "pmi.org",
    "Spoken Tutorial, EduPyramids, SINE, IIT Bombay": "iitb.ac.in",
    "Stanford University's Code in Place": "stanford.edu",
    "Tata Group": "tata.com",
    "Udemy": "udemy.com",
    "United Latino Students Association": "unitedlatinostudents.org"
}

# Leftover entities that are events or hyper-niche and better fetched via Wikipedia structure
wikipedia_targets = [
    "India AI Impact Summit 2026",
    "StudAI One",
    "WisdomQuantz"
]

output_folder = "logos"
os.makedirs(output_folder, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>| ]', '_', name) + ".png"

def download_image(url, filename):
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        if response.status_code == 200:
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f" -> Successfully downloaded: {filename}")
            return True
    except Exception:
        pass
    return False

def get_wikipedia_logo(title):
    """Safely fetches a page image URL directly from Wikipedia API."""
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "pageimages",
        "format": "json",
        "piprop": "original",
        "titles": title,
        "redirects": 1
    }
    try:
        res = requests.get(api_url, params=params, headers=headers, timeout=10).json()
        pages = res.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if "original" in page_data:
                return page_data["original"]["source"]
    except Exception:
        pass
    return None

print("Starting custom domain & API logo downloader...")

# Process Domain Mappings via Clearbit Logo API
for org_name, domain in domain_mappings.items():
    filename = clean_filename(org_name)
    
    if os.path.exists(os.path.join(output_folder, filename)):
        print(f"Skipping {org_name} (Already exists)")
        continue
        
    print(f"Processing (Domain-API): {org_name}...")
    clearbit_url = f"https://logo.clearbit.com/{domain}?size=600"
    
    if not download_image(clearbit_url, filename):
        # Fallback to Wikipedia API if the domain API misses it
        wiki_url = get_wikipedia_logo(org_name)
        if wiki_url:
            download_image(wiki_url, filename)
        else:
            print(f" -> [⚠️] Failed to fetch logo for {org_name}")
            
    time.sleep(0.5)

# Process remaining items via Wikipedia Structural API
for org_name in wikipedia_targets:
    filename = clean_filename(org_name)
    
    if os.path.exists(os.path.join(output_folder, filename)):
        print(f"Skipping {org_name} (Already exists)")
        continue
        
    print(f"Processing (Wiki-API): {org_name}...")
    wiki_url = get_wikipedia_logo(org_name)
    if wiki_url:
        download_image(wiki_url, filename)
    else:
        print(f" -> [⚠️] Failed to fetch logo for {org_name}")
        
    time.sleep(0.5)

print("\nAll downloads processed! Check the 'logos' directory.")