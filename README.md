# 🗺️ Google Maps Lead Scraper (V2) - With Phone Extraction 📞

An advanced automation tool built with **Python & Selenium** to generate complete B2B lead lists from Google Maps.
Unlike basic scrapers, this tool utilizes a **"Human-in-the-Loop"** strategy to safely extract data without getting blocked.

### 🌟 What makes this tool special?
It doesn't just scrape links; it visits every business profile, extracts the phone number, and **automatically cleans it** from any extra text (English, French, or Arabic labels).

## 🚀 Key Features
- **Smart Search:** Works with any keyword/location (e.g., "Real Estate in Dubai").
- **Anti-Bot Detection:** Uses manual search input to bypass Google's security.
- **Deep Extraction:** Visits every business profile to scrape hidden phone numbers.
- **Smart Cleaning:** Automatically removes text like "Phone:", "Numéro de téléphone:", "الهاتف:" to give you raw numbers.
- **Auto-Save:** Saves progress every 5 entries to prevent data loss.
- **Excel Export:** Outputs a professional `.xlsx` file ready for clean analysis.

## 🛠️ Built With
- **Language:** Python 3.x
- **Automation:** Selenium WebDriver
- **Data Management:** Pandas

## 💻 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hamzadeeci/Google-Maps-Lead-Scraper.git
* Install requirements:
 ```pip install -r requirements.txt```

##🔄 Workflow (How to run)

Step 1: Collect Links (The Harvester) Run the first script to gather business links:
 ```python bot_maps_final.py```
  Follow the on-screen instructions to search and scroll.
  
Step 2: Extract Phones (The Hunter) Run the second script to visit links and grab phone numbers:
 ```python bot_phones.py```
  The bot will open each link, extract the phone number, clean it, and save it automatically.
  
##📊 Output Example
The tool generates google_maps_leads.xlsx:

| Name | Google Maps Link | Phone | 
|------|------------------|-------|
| Lion | http://google... | +971..| 
| Social| http://google...| +971..|

👨‍💻 Author
**Hamza Delleci**
*Quantitative Economics Student & Python Developer*

I combine **Economic Analysis** with **Python Automation** to deliver valuable data insights.
I am available for freelance projects in:
- Web Scraping & Data Mining
- Process Automation
- Data Cleaning & Analysis

📫 Contact me: hamzadeeci@gmail.com
💼 Hire me: Open for Freelance Work

---
## 📄 License
This project is for educational purposes. Feel free to use and modify the code.

