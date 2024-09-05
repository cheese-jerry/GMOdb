import pymysql
from datetime import datetime
from connection import get_db_connection

class Prompt_execute_example_parameter:
    def __init__(self, id=None, prompt_id=None, parameter_name=None, example=None, created_at=None, updated_at=None):
        self.id = id
        self.prompt_id = prompt_id
        self.parameter_name = parameter_name
        self.example = example
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'prompt_id': self.prompt_id,
            'parameter_name': self.parameter_name,
            'example': self.example,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

def create_prompt_execute_example_parameter(event,prompt_id):
    #prompt = event.get_json()
    prompt = event["body"]
    prompt_execute_example_parameters_list = prompt['prompt_parameters']

    connection = get_db_connection()
    try:
        for data in prompt_execute_example_parameters_list:
            new_prompt_execute_example_parameter = Prompt_execute_example_parameter(
                prompt_id = prompt_id,
                parameter_name = data["parameter_name"],
                example = data["parameter_example"]
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO prompt_execute_example_parameter (prompt_id,parameter_name, example)
                            VALUES (%s, %s, %s)"""
                cursor.execute(sql, (
                    new_prompt_execute_example_parameter.prompt_id,
                    new_prompt_execute_example_parameter.parameter_name,
                    new_prompt_execute_example_parameter.example
                ))
                connection.commit()
                new_prompt_execute_example_parameter.id = cursor.lastrowid  # 挿入されたIDを取得
    finally:
        connection.close()    
    return new_prompt_execute_example_parameter.id   

def get_prompt_execute_example_parameter_by_promptID(prompt_id):
    dic_list = []
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 指定された prompt_id に関連する prompt_execute_example_parameter を取得
            sql = "SELECT * FROM prompt_execute_example_parameter WHERE prompt_id = %s"
            cursor.execute(sql, (prompt_id,))
            result = cursor.fetchall()

            for row in result:
                # 各レコードを Prompt_execute_example_parameter オブジェクトに変換
                prompt_execute_example_parameter = Prompt_execute_example_parameter(
                    #id=row['id'],
                    #prompt_id=row['prompt_id'],
                    parameter_name=row['parameter_name'],
                    example=row['example'],
                    #created_at=row['created_at'],
                    #updated_at=row['updated_at']
                )
                dic_list.append(prompt_execute_example_parameter.to_dict())

    finally:
        connection.close()

    return dic_list