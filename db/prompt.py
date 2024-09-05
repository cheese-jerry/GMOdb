import pymysql
from datetime import datetime
from connection import get_db_connection
from prompt_execute_example import create_prompt_execute_example,get_prompt_execute_example_by_promptID
from prompt_execute_example_parameter import get_prompt_execute_example_parameter_by_promptID

class Prompt:
    def __init__(self, id=None, user_id=None, prompt_introduction_text=None, prompt_name=None, 
                 prompt_view_count=None, prompt_welcome_message=None, prompt_head=None, 
                 create_at=None, update_at=None):
        self.id = id
        self.user_id = user_id
        self.prompt_introduction_text = prompt_introduction_text
        self.prompt_name = prompt_name
        self.prompt_view_count = prompt_view_count
        self.prompt_welcome_message = prompt_welcome_message
        self.prompt_head = prompt_head
        self.create_at = create_at
        self.update_at = update_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'prompt_introduction_text': self.prompt_introduction_text,
            'prompt_name': self.prompt_name,
            'prompt_view_count': self.prompt_view_count,
            'prompt_welcome_message': self.prompt_welcome_message,
            'prompt_head': self.prompt_head,
            'create_at': self.create_at,
            'update_at': self.update_at
        }

def prompt_list():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM prompt"
            cursor.execute(sql)
            result = cursor.fetchall()

            prompts = []
            for row in result:
                prompt = Prompt(
                    id=row['id'],
                    user_id=row['user_id'],
                    prompt_introduction_text=row['prompt_introduction_text'],
                    prompt_name=row['prompt_name'],
                    prompt_view_count=row.get('prompt_view_count', None),
                    prompt_welcome_message=row['prompt_welcome_message'],
                    prompt_head=row['prompt_head'],
                    create_at=row['create_at'],
                    update_at=row['update_at']
                )
                prompts.append(prompt.to_dict())
    finally:
        connection.close()
    
    return prompts

def create_prompt(event):
    #data = event.get_json()
    data = event["body"]
    new_prompt = Prompt(
        user_id=data['user_id'],
        prompt_introduction_text=data['prompt_introduction_text'],
        prompt_name=data['prompt_name'],
        prompt_welcome_message=data['prompt_welcome_message'],
        prompt_head=data['prompt_head'],
        create_at=datetime.utcnow(),
        update_at=datetime.utcnow()
    )

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO prompt (user_id, prompt_introduction_text, prompt_name, prompt_head, prompt_welcome_message)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                new_prompt.user_id,
                new_prompt.prompt_introduction_text,
                new_prompt.prompt_name,
                new_prompt.prompt_head,
                new_prompt.prompt_welcome_message
            ))
            new_prompt_id = cursor.lastrowid
            create_prompt_execute_example(event, new_prompt_id)
            connection.commit()
            new_prompt.id = new_prompt_id
    finally:
        connection.close()

    return new_prompt.id

def get_prompt_by_ID(prompt_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQLクエリを準備して、IDに基づいてpromptを取得
            sql = "SELECT * FROM prompt WHERE id = %s;"
            cursor.execute(sql, (prompt_id,))
            result = cursor.fetchone()  # 単一のレコードを取得
            if result:
                resdic = {}
                # 結果を Prompt オブジェクトにマッピング
                prompt = Prompt(
                    id=result['id'],
                    user_id=result['user_id'],
                    prompt_introduction_text=result['prompt_introduction_text'],
                    prompt_name=result['prompt_name'],
                    prompt_view_count=result.get('prompt_view_count', None),
                    prompt_welcome_message=result['prompt_welcome_message'],
                    prompt_head=result['prompt_head'],
                    create_at=result['create_at'],
                    update_at=result['update_at']
                )
                resdic = prompt.to_dict()
                prompt_example_list = get_prompt_execute_example_by_promptID(prompt_id)
                prompt_example_parameters_list = get_prompt_execute_example_parameter_by_promptID(prompt_id)
                resdic["prompt_example"] = prompt_example_list
                resdic["prompt_parameters"] = prompt_example_parameters_list
                return resdic
            else:
                # 該当するIDのレコードがない場合
                return None
    finally:
        connection.close()



# for local test
test_event = {
  "body": {
    "prompt_name": "demo",
    "user_id": 999999,
    "prompt_introduction_text": "demo",
    "prompt_welcome_message": "hello my name is demo",
    "prompt_head": "以下の文を校正してください。{{変数11}}",
    "prompt_example": [
      {
        "sender": "ai",
        "message_text": "これはデモ"
      }
    ],
    "prompt_parameters": [
      {
        "parameter_name": "変数1",
        "parameter_example": "変数デモ"
      }
    ]
  }

}

promptlist = prompt_list()
print(promptlist)

#id = create_prompt(test_event)
#print(id)

#res = get_prompt_by_ID(15)
#print(res)




