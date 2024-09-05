import pymysql
from datetime import datetime
from connection import get_db_connection
from prompt_execute_example_parameter import create_prompt_execute_example_parameter

class Prompt_execute_example:
    def __init__(self, id=None, prompt_id=None, sender=None, message_text=None, send_time=None, created_at=None, updated_at=None):
        self.id = id
        self.prompt_id = prompt_id
        self.sender = sender
        self.message_text = message_text
        self.send_time = send_time
        self.created_at = created_at
        self.updated_at = updated_at

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
    #prompt = event.get_json()
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

def get_prompt_execute_example_by_promptID(prompt_id):
    dic_list = []
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 指定されたprompt_idに関連するprompt_execute_exampleを取得
            sql = "SELECT * FROM prompt_execute_example WHERE prompt_id = %s"
            cursor.execute(sql, (prompt_id,))
            result = cursor.fetchall()

            for row in result:
                prompt_execute_example = Prompt_execute_example(
                    #id=row['id'],
                    #prompt_id=row['prompt_id'],
                    sender=row['sender'],
                    message_text=row['message_text'],
                    #send_time=row['send_time'],
                    created_at=row['created_at'],
                    #updated_at=row['updated_at']
                )
                dic_list.append(prompt_execute_example.to_dict())
    finally:
        connection.close()
    # created_atでソート（昇順）
    dic_list = sorted(dic_list, key=lambda x: x['created_at'])

     # dic_listの各辞書からcreated_atを削除
    for dic in dic_list:
        if 'created_at' in dic:
            del dic['created_at']

    return dic_list