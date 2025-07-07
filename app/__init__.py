import os
import json
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from pathlib import Path
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),   
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb
        
mydb.connect()
mydb.create_tables([TimelinePost], safe=True)

personal_info_path = Path(__file__).with_name("personal_info.json")
    
with open(personal_info_path, encoding="utf-8") as pif:
    personal_info = json.load(pif)


@app.route('/')
def index():

    about_info   = personal_info.get("about", {})
    educations   = personal_info.get("education", [])
    experiences  = personal_info.get("experience", [])
    countries    = personal_info.get("countries", [])
    
    return render_template('index.html', title="MLH Fellow", about_info=about_info, educations=educations, experiences=experiences, countries=countries, url=os.getenv("URL"))
  
@app.route('/hobbies')
def hobby():
    
    hobbies  = personal_info.get("hobbies", [])
    
    return render_template('hobby.html', title="Hobbies", hobbies=hobbies)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [model_to_dict(post) for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    }
    
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)
    if not post:
        return {"error": "Post not found"}, 404
    post.delete_instance()
    return {"status": "deleted", "id": post_id}

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")