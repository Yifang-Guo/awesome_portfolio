import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():

    about_text = os.getenv("ABOUT", "No about text provided.")

    raw_educations = os.getenv("EDUCATION", "")
    education_entries = []

    for edu in raw_educations.split("\n"):
        fields = [f.strip() for f in edu.split("|")]
        if len(fields) == 5:
            education_entries.append({
                "university": fields[0],
                "major": fields[1],
                "degree": fields[2],
                "location": fields[3],
                "time": fields[4]
            })

    raw_experiences = os.getenv("EXPERIENCE", "")
    experience_entries = []

    for exp in raw_experiences.split("\n"):
        fields = [f.strip() for f in exp.split("|")]
        if len(fields) == 4:
            experience_entries.append({
                "role": fields[0],
                "company": fields[1],
                "duration": fields[2],
                "details": [d.strip() for d in fields[3].split(";") if d.strip()]
            })

    countries_str = os.getenv("COUNTRIES", "")  # e.g., "USA,CAN,GBR"
    visited_countries = [code.strip() for code in countries_str.split(",") if code.strip()]

    
    return render_template('index.html', title="MLH Fellow", about_text=about_text, educations=education_entries, experiences=experience_entries, countries=visited_countries, url=os.getenv("URL"))
  
@app.route('/hobbies')
def hobby():
    img_path_prefix = "/static/img/hobby_imgs/"
    
    # Get and parse hobbies and image file names from .env
    raw_hobbies = os.getenv("HOBBIES", "")
    hobbies_name = [h.strip() for h in raw_hobbies.split(",") if h.strip()]
    
    raw_hobbies_imgs = os.getenv("HOBBIES_IMGS", "")
    hobbies_imgs = [img_path_prefix + img.strip() for img in raw_hobbies_imgs.split(",") if img.strip()]
    
    # Zip hobby names with corresponding image paths
    hobbies = list(zip(hobbies_name, hobbies_imgs))

    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)