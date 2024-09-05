"""
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
"""
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# MySQL 数据库连接配置
MYSQL_HOST = 'group4-db.cx8omk226wtm.ap-northeast-1.rds.amazonaws.com'
MYSQL_USER = 'gmoyu'
MYSQL_PASSWORD = 'gmogroup04'
MYSQL_DB = 'ai_site_group4'
DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# 初始化 SQLAlchemy
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 获取 SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建 MySQL 连接
def get_db_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# 你可以在 Base 子类中定义你的模型，并使用 get_db() 进行数据库操作
