from multiprocessing import connection
from sqlite3 import Cursor
import pymysql

def connect_to_mysql(): #подключится к самому mysql
    try:
        connection = pymysql.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        password = "MovaviSchoolFest",
        cursorclass = pymysql.cursors.DictCursor
        )   
        print("success")
        cursor = connection.cursor()
        return connection
    except Exception as ex:
        return ex
#users: id,username,email,user_password




class DataBaseHelper():
    def __init__(self):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "CREATE DATABASE IF NOT EXISTS quiz_project_db"
        self.cursor.execute(query)
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(100),email VARCHAR(100),userpassword VARCHAR(100))"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS quizes(id INT PRIMARY KEY AUTO_INCREMENT,id_user INT, quizname VARCHAR(100),description VARCHAR(200),picture VARCHAR(200))"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS questions(id INT PRIMARY KEY AUTO_INCREMENT,id_quiz INT, question VARCHAR(100),picture VARCHAR(200))"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS answers(id INT PRIMARY KEY AUTO_INCREMENT,id_question INT, answer VARCHAR(100), rightanswer INT)"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS codes(id INT PRIMARY KEY AUTO_INCREMENT, code INT)"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS quizes_status(id INT PRIMARY KEY AUTO_INCREMENT,id_quiz INT,id_user INT, code INT, status INT)"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS players_status(id INT PRIMARY KEY AUTO_INCREMENT, player VARCHAR(200), id_quiz INT, code INT, score INT)"
        self.cursor.execute(query)
        # query = "CREATE TABLE IF NOT EXISTS questions(id INT PRIMARY KEY AUTO_INCREMENT, quizname VARCHAR(100),question VARCHAR(200),picture VARCHAR(200),answers VARCHAR(200),rightanswers VARCHAR(200))"
        # self.cursor.execute(query)
        self.connection.commit()
        
    def insert_user(self,data = []): #при регистрации вставить в бд
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO users(username,email,userpassword) VALUES(%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()

    def check_user_registration_name(self,data = []): # True - можно вставлять False - нельзя
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM users WHERE username=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return False
        return True

    def check_user_registration_email(self,data = []): # True - можно вставлять False - нельзя
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM users WHERE email=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return False
        return True
    def check_user_for_authorization(self,data = []):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT username FROM users WHERE email=%s AND userpassword=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return False

    def select_userpassword_using_email(self,data = []):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT userpassword FROM users WHERE email=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return False
    def check_quizname(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM quizes WHERE quizname=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return False
        return True
    def insert_quiz(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO quizes(id_user,quizname,description,picture) VALUES(%s,%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def find_user_id(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM users WHERE username=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def insert_question(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO questions(id_quiz,question,picture) VALUES(%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def find_quiz_id(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM quizes WHERE quizname=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_all_questions_by_id(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM questions WHERE id_quiz=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def insert_answers(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO answers(id_question,answer,rightanswer) VALUES(%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def select_quizes(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM quizes"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def get_author_id(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id_user FROM quizes WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def get_author_name(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT username FROM users WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def get_quizname(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT quizname FROM quizes WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def get_description(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT description FROM quizes WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def get_quiz_picture(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT picture FROM quizes WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_quizname(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT quizname FROM quizes WHERE id=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_all_codes(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT code FROM codes"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return []
    def insert_code(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO codes(code) VALUES(%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def insert_player(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO players_status(id_player,id_quiz) VALUES(%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    #idq cod sta
    def insert_quiz_started(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO quizes_status(id_quiz,id_user,code,status) VALUES(%s,%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def select_id_quiz_using_code(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id_quiz FROM quizes_status WHERE code=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_id_quiz_using_quizname(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id FROM quizes WHERE quizname=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def insert_player_status(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "INSERT INTO players_status(player,id_quiz,code,score) VALUES(%s,%s,%s,%s)"
        self.cursor.execute(query,data)
        self.connection.commit()
    def find_players_using_code(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT player FROM players_status WHERE code=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return []
    def change_quiz_status(self,data=[]):
        #UPDATE users SET email = "new@php.zone" WHERE id = 2
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = 'UPDATE quizes_status SET status="1" WHERE code=%s'
        self.cursor.execute(query,data)
        self.connection.commit()
    def check_quiz_status(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT status FROM quizes_status WHERE code=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return 1
        return 0
    def select_questions(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT * FROM questions WHERE id_quiz=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_id_quiz_using_code(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT id_quiz FROM quizes_status WHERE code=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_answers(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT * FROM answers WHERE id_question=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def select_score(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT score FROM players_status WHERE player=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def change_score(self,data=[]):
        #UPDATE users SET email = "new@php.zone" WHERE id = 2
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = 'UPDATE players_status SET score=%s WHERE player=%s'
        self.cursor.execute(query,data)
        self.connection.commit()
    def select_player_and_score(self,data=[]):
        self.connection = connect_to_mysql()
        self.cursor = self.connection.cursor()
        query = "USE quiz_project_db"
        self.cursor.execute(query)
        query = "SELECT player,score FROM players_status WHERE code=%s"
        self.cursor.execute(query,data)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    # with connection.cursor() as cursor:
    #     query = "CREATE "
    #     cursor.execute(query)
    #     connection.commit()
    # try:
    #     cursor = connection.cursor()
    #     with connection.cursor() as cursor:
    #         query = "INSERT INTO users (username,email,password) VALUES(ТЕСТ,13,йцу)"
    #         cursor.execute(query)
    #         connection.commit()        
    # finally:
    #     connection.close()
