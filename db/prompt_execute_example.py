import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask,jsonify
from connection import get_db_connection,get_db
from prompt_execute_example_parameter import create_prompt_execute_example_parameter

app = Flask(__name__)
db = get_db()

class Prompt_execute_example(db.Model):
    __tablename__ = "prompt_execute_example"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    prompt_id = db.Column(db.BigInteger, db.ForeignKey('prompts.id'), nullable=False, index=True)
    sender = db.Column(db.Integer, nullable=False)
    message_text = db.Column(db.String(500), nullable=True)
    send_time = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def to_dict(self):
        return {
            'id': self.id,
            'prompt_id': self.prompt_id,
            'sender': self.sender,
            'message_text': self.message_text,
            'send_time': self.send_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

def create_prompt_execute_example(event,prompt_id):
    prompt = event.get_json()
    prompt = event["body"] 
    prompt_execute_example_list = prompt['prompt_example']

    connection = get_db_connection()
    try:
        for data in prompt_execute_example_list:
            new_prompt_execute_example = Prompt_execute_example(
                prompt_id = prompt_id,
                sender = data["sender"],
                message_text = data["message_text"]
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO prompt_execute_example (prompt_id,sender, message_text)
                            VALUES (%s, %s, %s)"""
                cursor.execute(sql, (
                    new_prompt_execute_example.prompt_id,
                    new_prompt_execute_example.sender,
                    new_prompt_execute_example.message_text
                ))
                create_prompt_execute_example_parameter(event,prompt_id)
                connection.commit()
                new_prompt_execute_example.id = cursor.lastrowid  # 挿入されたIDを取得
    finally:
        connection.close()    

    return new_prompt_execute_example.id   