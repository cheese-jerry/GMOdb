import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask,jsonify
from connection import get_db_connection,get_db

app = Flask(__name__)
db = get_db()

class Prompt_execute_example_parameter(db.Model):
    __tablename__ = "prompt_execute_example_parameter"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    prompt_id = db.Column(db.BigInteger, db.ForeignKey('prompts.id'), nullable=False, index=True)
    parameter_name = db.Column(db.String(15), nullable=True)
    example = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    prompt = event.get_json()
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