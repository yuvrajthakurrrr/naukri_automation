##-- AI Imports --##
import os
import re
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage

##---Selenium Imports ---##
import pandas as pd
import requests
import time
import string
import math
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.types import NVARCHAR
import urllib
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from shutil import which
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from lxml import etree
import random,os
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
##---End of Selenium Imports ---##

load_dotenv()

# Load your LaTeX resume
with open("yuvraj_resume.tex", "r", encoding="utf-8") as f:
    resume_content = f.read()

# Model setup (same as before)
model = ChatNVIDIA(
    model="deepseek-ai/deepseek-v3.1",
    temperature=0.2,
    top_p=0.7,
    max_tokens=8192,
    extra_body={"chat_template_kwargs": {"thinking": True}},
)

# Build the prompt
prompt = f"""
You are an expert career advisor. I will provide my resume in LaTeX format. Please extract the relevant information and generate the following sections optimized for a Naukri.com profile. Naukri recruiters look for concise, keyword‑rich content.

**Instructions:**
- Ignore LaTeX commands (like \\section, \\textbf, etc.) and only focus on the actual content.
- Tailor the output for a job search in Data and AI Engineering (adjust to your field).
- Use quantifiable achievements where possible.
- Respect the character limits strictly:
  - HEADLINE: maximum 250 characters (including spaces)
  - SKILLS: comma-separated list, each skill a short keyword (eg, Python, Machine Learning, SQL), max 19 skills, do not include any long text in the skills section, only concise skill names
  - SUMMARY: maximum 1000 characters (including spaces)
- Do not include any sections in each other sections.

Return the sections in the following format:

HEADLINE: (max 250 characters)
SKILLS: (comma-separated, max 19 skills)
SUMMARY: (max 1000 characters)

**Resume (LaTeX):**
{resume_content}
"""

messages = [HumanMessage(content=prompt)]

print("\n--- Generated Profile Sections ---")
response = model.invoke(messages)
#print(response.content)
raw_output = response.content


def extract_skills_from_latex(latex_content):
    """
    Given a LaTeX string containing \resumeSectionType{...}{:}{...} lines,
    returns a list of cleaned skill keywords.
    """
    # Pattern to capture the third argument: \resumeSectionType{...}{:}{...}
    # The third argument can contain nested braces? In this case it's simple.
    pattern = r'\\resumeSectionType\{[^}]*\}\{:?\}\{([^}]*)\}'
    matches = re.findall(pattern, latex_content)
    
    skills = []
    for match in matches:
        # Split by comma, but be careful: some entries have parentheses
        parts = [p.strip() for p in match.split(',')]
        for part in parts:
            # Remove anything in parentheses (e.g., "Python (Advanced)" -> "Python")
            cleaned = re.sub(r'\s*\([^)]*\)', '', part).strip()
            if cleaned:
                skills.append(cleaned)
    
    # Remove duplicates while preserving order
    unique_skills = []
    seen = set()
    for skill in skills:
        if skill.lower() not in seen:
            unique_skills.append(skill)
            seen.add(skill.lower())
    
    return unique_skills

# --- Parse the output into variables ---
def parse_sections(text):
    """Extract HEADLINE, SUMMARY, SKILLS from the model's output."""
    patterns = {
        'headline': r'HEADLINE:\s*(.*?)(?=\n\s*(?:SUMMARY|SKILLS)|\Z)',
        'skills':   r'SKILLS:\s*(.*?)(?=\n\s*(?:SUMMARY|ACHIEVEMENTS)|\Z)',
        'summary':  r'SUMMARY:\s*(.*?)(?=\n\s*(?:ACHIEVEMENTS)|\Z)',
    }

    sections = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        sections[key] = match.group(1).strip() if match else ""
    return sections

sections = parse_sections(raw_output)

# Assign to separate variables
headline = sections['headline']
#new_skills = list(sections['skills'].split(','))
summary = sections['summary']

# After parsing the skills section
skills_raw = sections['skills']
# Split by comma, strip whitespace, and filter out empty strings
skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
# Remove duplicates while preserving order
skills_list = list(dict.fromkeys(skills_list))
# Optionally capitalise each skill (e.g., "python" → "Python")
skills_list = [s.capitalize() if s.islower() else s for s in skills_list]
# Truncate to max 19
skills_list = skills_list[:19]

print(f"HEADLINE:\n{headline}\n")
print(f"SKILLS:\n{skills_list}\n")
print(f"SUMMARY:\n{summary}\n")
chrome_options = Options()

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-gpu")

# ✅ SAFE PROFILE (new folder)
chrome_options.add_argument(
    f"--user-data-dir={os.path.expanduser('~/selenium_profile')}"
)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.naukri.com")
time.sleep(random.uniform(2, 4)) 
driver.get(("https://www.naukri.com/mnjuser/profile"))
time.sleep(random.uniform(2, 4)) 

##---Resume headline--##
driver.find_element(By.XPATH, "//span[contains(text(),'Resume headline')]/following-sibling::span[contains(text(),'editOneTheme')]").click()
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//textarea").clear()
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//textarea").send_keys(headline)
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//div[@class='row form-actions']//button[contains(text(),'Save')]").click()
time.sleep(random.uniform(2, 4)) 

##---Updating Key Skill Section--##
driver.find_element(By.XPATH, "//span[contains(text(),'Key skills')]/following-sibling::span[contains(text(),'editOneTheme')]").click()
time.sleep(random.uniform(2, 4)) 
present_skills = driver.find_elements(By.XPATH, "//a[@class='material-icons close']")
total_skills = len(present_skills)
for i in range(total_skills):
    driver.find_element(By.XPATH, "//a[@class='material-icons close']").click()
    time.sleep(1)

for skill in skills_list:
    skill_input = driver.find_element(By.XPATH, "//input[@id='keySkillSugg']")
    skill_input.clear()
    skill_input.send_keys(skill)
    time.sleep(1)  # brief wait for dropdown to appear

    # Wait for suggestion list to be visible
    try:
        suggestion_list = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='sugDrp_keySkillSugg']//ul"))
        )
        suggestions = suggestion_list.find_elements(By.TAG_NAME, "li")
        # Find a suggestion that matches the typed skill (case-insensitive)
        selected = False
        for sugg in suggestions:
            if sugg.text.strip().lower() == skill.lower():
                sugg.click()
                selected = True
                break
        if not selected:
            # If no exact match, click the first suggestion (or handle as needed)
            suggestions[0].click()
    except:
        # Dropdown didn't appear – maybe skill is not recognised; skip or try pressing Enter
        skill_input.send_keys(Keys.RETURN)
    time.sleep(1)

driver.find_element(By.XPATH, "//div[@class='row form-actions']//button[contains(text(),'Save')]").click()
time.sleep(random.uniform(2, 4)) 


##---Profile Summary--##
try:
    driver.find_element(By.XPATH, "//li//span[contains(text(),'Profile summary')]").click()
    time.sleep(random.uniform(2, 4)) 
except:
    print("Profile summary Button not found")

driver.find_element(By.XPATH, "//span[contains(text(),'Profile summary')]/following-sibling::span[contains(text(),'editOneTheme')]").click()
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//textarea").clear()
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//textarea").send_keys(summary)
time.sleep(random.uniform(2, 4)) 
driver.find_element(By.XPATH, "//div[@class='row form-actions']//button[contains(text(),'Save')]").click()

try:
    driver.quit()
except:
    pass