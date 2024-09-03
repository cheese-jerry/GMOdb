import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask,jsonify
from datetime import datetime
from connection import get_db_connection,get_db
from prompt_execute_example import create_prompt_execute_example

app = Flask(__name__)
db = get_db()

class Prompt(db.Model):
    __tablename__ = "prompt"
    id = db.Column(db.BigInteger,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    prompt_introduction_text = db.Column(db.String(200))
    prompt_name = db.Column(db.String(25))
    prompt_view_count = db.Column(db.Integer)
    prompt_welcome_message = db.Column(db.String(100))
    prompt_head = db.Column(db.String(500))
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'prompt_introduction_text': self.prompt_introduction_text,
            'prompt_name': self.prompt_name,
            'prompt_view_count': self.prompt_view_count,
            'prompt_welcome_message': self.prompt_welcome_message,
            "prompt_head":self.prompt_head,
            'create_at': self.create_at,
            'update_at': self.update_at
        }
    
def prompt_list():
    # open db get connection
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query
           
            sql = "SELECT * FROM prompt"
            cursor.execute(sql)
            
            # get sql query result
            result = cursor.fetchall()
            
            # result reflect to db model Prompt
            prompts = []
            for row in result:
                prompt = Prompt(
                    id=row['id'],
                    user_id=row['user_id'],
                    prompt_introduction_text=row['prompt_introduction_text'],
                    prompt_name = row['prompt_name'],
                    prompt_view_count = row['prompt_view_count'],
                    prompt_welcome_message =  row['prompt_welcome_message'],
                    prompt_head = row['prompt_head'],
                    create_at=row['create_at'],
                    update_at=row['update_at']
                )
                prompts.append(prompt.to_dict())
    
    finally:
        connection.close()  # close db connection
    
    # return JSON    
    with app.app_context():
        return jsonify(prompts)




def create_prompt(event):
    data = event.get_json()
    data = event["body"] 
     # reflect to db model Prompt
    new_prompt = Prompt(
        user_id=data['user_id'],
        prompt_introduction_text=data['prompt_introduction_text'],
        prompt_name=data['prompt_name'],
        prompt_welcome_message=data['prompt_welcome_message'],
        prompt_head=data['prompt_head'],
        create_at=datetime.utcnow(),
        update_at=datetime.utcnow()
    )
    with app.app_context():
        connection = get_db_connection()
        try:
            # from db model Prompt get information and insert into db
            with connection.cursor() as cursor:
                sql = """INSERT INTO prompt (user_id, prompt_introduction_text, prompt_name,prompt_head, prompt_welcome_message)
                        VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    new_prompt.user_id,
                    new_prompt.prompt_introduction_text,
                    new_prompt.prompt_name,
                    new_prompt.prompt_head,
                    new_prompt.prompt_welcome_message
                ))
                new_prompt_id = cursor.lastrowid
                print("=========================")
                print(new_prompt_id)
                create_prompt_execute_example(event,new_prompt_id)
                connection.commit()
                new_prompt.id = cursor.lastrowid  # 挿入されたIDを取得
        finally:
            connection.close()

        return new_prompt.id


#for local test
test_event = {
  "body": {
    "prompt_name": "string",
    "user_id": 0,
    "prompt_introduction_text": "string",
    "prompt_welcome_message": "校正したい文を入力して",
    "prompt_head": "以下の文を校正してください。{{変数1}}",
    "prompt_example": [
      {
        "sender": "ai",
        "message_text": "以下のように修正します。「ごめんなさい。」"
      }
    ],
    "prompt_parameters": [
      {
        "parameter_name": "変数1",
        "parameter_example": "ごめんなさい"
      }
    ]
  }
}

import json

res = create_prompt(test_event)
print(res)