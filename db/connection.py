import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

app = Flask(__name__)
# MySQL 数据库连接配置

app.config['MYSQL_HOST'] = 'group4-db.cx8omk226wtm.ap-northeast-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'gmoyu'
app.config['MYSQL_PASSWORD'] = 'gmogroup04'
app.config['MYSQL_DB'] = 'ai_site_group4'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"

# 初始化 SQLAlchemy

db = SQLAlchemy(app)
def get_db():
    return db

# 创建 MySQL 连接
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection