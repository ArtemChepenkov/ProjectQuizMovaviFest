from multiprocessing.dummy import Namespace
import os
from flask import Flask,render_template,request,session,redirect,url_for
from data_base_helper import DataBaseHelper
import hashlib
from werkzeug.utils import secure_filename
from transliterate import translit
from flask_socketio import SocketIO,emit,send,join_room,leave_room
from random import randint

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = os.urandom(10)
db = DataBaseHelper()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        return render_template("index.html")
    elif request.method == "GET":
        d = {"authorized":0,
            "username":None
            }
        if "authorized" in session:
            username = session["authorized"]
            d["authorized"] = 1
            d["username"] = username
        return render_template("index.html",**d)

@app.route("/quizes",methods = ["GET","POST"])
def create_test():
    data = {
        "message":1,
    }
    if not "authorized" in session:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("quizes.html",**data)
    elif request.method == "POST":
        return render_template("quizes.html",**data)

@app.route("/authorization",methods = ["GET","POST"])
def auth():
    if request.method == "GET":
        return render_template("authorization.html")
    elif request.method == "POST":
        data = dict(request.form)

        sha256 = hashlib.sha256()
        sha256.update(data["email"].encode('utf-8'))
        email = sha256.hexdigest()

        sha256 = hashlib.sha256()
        sha256.update(data["password"].encode('utf-8'))
        userpassword = sha256.hexdigest()

        result = db.check_user_for_authorization((email,userpassword))
        print(result)
        d = {
            "result_of_authorization":1
        }
        if result:
            session["authorized"] = result[0]["username"]
        else:
            result_password = db.select_userpassword_using_email((email,))
            if result_password and result_password != userpassword:
                d["result_of_authorization"] = 2 #пароль неправильный
            else:
                d["result_of_authorization"] = 3 #email неправильный
        return render_template("authorization.html",**d)

@app.route("/registration",methods = ["GET","POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")
    elif request.method == "POST":
        data = dict(request.form)
        username = data["username"]

        sha256 = hashlib.sha256()
        sha256.update(data["email"].encode('utf-8'))
        email = sha256.hexdigest()

        sha256 = hashlib.sha256()
        sha256.update(data["password"].encode('utf-8'))
        userpassword = sha256.hexdigest()

        print(type(username),type(email),type(userpassword))
        result1 = db.check_user_registration_name((username,))
        result2 = db.check_user_registration_email((email,))
        print(result1,result2)
        error_dict = {
            "wrong_username":0,
            "wrong_email":0
        }
        if result1 and result2:
            db.insert_user((username,email,userpassword))
            session["authorized"] = username
        if not result1:
            error_dict["wrong_username"] = 1
        if not result2:
            error_dict["wrong_email"] = 1
        return render_template("registration.html",**error_dict)
@app.route("/sign_out")
def sign_out():
    try:
        del session["authorized"]
    except Exception as ex:
        print(ex)
    return redirect(url_for("index"))

@app.route("/create_question",methods=["GET","POST"])
def create_question():
    if not "authorized" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        values = dict(request.form)

        if "first_answer" in values.keys():
            values = dict(request.form)
            print("VALUES",values)
            # right_answers = ""
            # if "first_checkbox" in values.keys():
            #     right_answers += values["first_answer"]+","
            # if "second_checkbox" in values.keys():
            #     right_answers += values["second_answer"]+","
            # if "third_checkbox" in values.keys():
            #     right_answers += values["third_answer"]+","
            # if "fourth_checkbox" in values.keys():
            #     right_answers += values["fourth_answer"]+","
            # if right_answers[-1] == ",":
            #     right_answers = right_answers[0:-1]
            question = values["question"]
            answers = values["first_answer"]+","+values["second_answer"]+","+values["third_answer"]+","+values["fourth_answer"]
            #question_picture = values["question_picture"]
            file = request.files['question_picture']
            # print("RIGHT ANSWERS",right_answers)
            picture = ""
            if file and allowed_file(file.filename):
                filename = secure_filename(translit(file.filename, 'ru',reversed=True))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                picture = app.config['UPLOAD_FOLDER']+filename
            else:
                picture = app.instance_path[:-9:]+"/static/images/default_picture.png"
            print(picture)
            id_quiz = db.find_quiz_id((session["QUIZ_NAME"],))[0]["id"]
            print("ID_QUIZ",id_quiz)
            db.insert_question((id_quiz,question,picture))
            id_question = db.select_all_questions_by_id((id_quiz,))[-1]["id"]

            if "first_answer" in values.keys():
                right = 0
                if "first_checkbox" in values.keys():
                    right = 1
                db.insert_answers((id_question,values["first_answer"],right))
            if "second_answer" in values.keys():
                right = 0
                if "second_checkbox" in values.keys():
                    right = 1
                db.insert_answers((id_question,values["second_answer"],right))
            if "third_answer" in values.keys():
                right = 0
                if "third_checkbox" in values.keys():
                    right = 1
                db.insert_answers((id_question,values["third_answer"],right))
            if "fourth_answer" in values.keys():
                right = 0
                if "fourth_checkbox" in values.keys():
                    right = 1
                db.insert_answers((id_question,values["fourth_answer"],right))

            return render_template("create_question.html")
        else:
            quiz_name = values["quiz_name"]
            res = db.check_quizname((quiz_name,))
            data = {
                    "message":1
                }
            if not res:
                data["message"] = 0
                return render_template("quizes.html",**data)
            description = values["description"]
            print(app.instance_path[:-9:])
            UPLOAD_FOLDER = uploads_dir = app.instance_path[:-9:]+f'/static/images_for_tests/{quiz_name}/'
            os.makedirs(uploads_dir, exist_ok=True) 

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            print(request.files)
            file = request.files['quiz_picture']
            print("FILE",file)
            picture = ""
            if file and allowed_file(file.filename):
                filename = secure_filename(translit(file.filename, 'ru',reversed=True))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                picture = app.config['UPLOAD_FOLDER']+filename
            else:
                picture = app.instance_path[:-9:]+"/static/images/default_picture.png"

            print(values)
            id_user = db.find_user_id((session["authorized"],))[0]["id"]
            print(id_user)
            db.insert_quiz((id_user,quiz_name,description,picture))
            session["QUIZ_NAME"] = quiz_name
            return render_template("create_question.html")
    elif request.method == "GET":
        return render_template("create_question.html")
@app.route("/pass_quizes",methods=["GET","POST"])
def pass_quizes():
    quizes_dict = db.select_quizes()
    if not quizes_dict:
        return "Пока нет викторин"
    quizes = []
    for i in range(len(quizes_dict)):
        quizes.append(quizes_dict[i]["id"])
    if len(quizes) > 10:
        quizes.reverse()
        quizes = quizes[0:10]
        quizes.reverse()
    print(quizes)
    d = {}
    for i in range(len(quizes)):
        # author = ""
        # quizname = ""
        # description = ""
        # picture = ""
        author_id = db.get_author_id((quizes[i],))[0]["id_user"]
        author = db.get_author_name((author_id,))[0]["username"]
        
        quizname = db.get_quizname((quizes[i],))[0]["quizname"]

        description = db.get_description((quizes[i],))[0]["description"]
        
        picture = db.get_quiz_picture((quizes[i],))[0]["picture"]
        picture = picture[picture.index("/"):]
        d[quizes[i]] = [author,quizname,description,picture]
    for i in d:
        print(i)
    print(d)
    if request.method == "GET":
        return render_template("quizes_list.html",d=d)
    elif request.method == "POST":
        return render_template("quizes_list.html",d=d)

@app.route("/quiz/<id>")
def quiz(id):
    quizname = db.select_quizname((id,))[0]["quizname"]

    codes_d = db.select_all_codes()
    codes = []
    if len(codes_d) > 0:
        for i in range(len(codes_d)):
            codes.append(codes_d[i]["code"])
    print(codes)
    while True:
        code = randint(100000,1000000)
        if not code in codes:
            break
    db.insert_code((code,))
    d = {"quizname":quizname,
        "code":code}
    #idq code status
    id_user = int(db.find_user_id((session["authorized"],))[0]["id"])
    print("IDUSER",id_user)
    session["CODE"] = code
    db.insert_quiz_started((id,id_user,code,0))
    return render_template("quiz.html",**d)
@app.route("/quiz_guest",methods=["GET","POST"])
def quiz_guest():
    if request.method == "GET":
        # code = request.args.get("game_code")
        player_name = request.args.get("playername")
        # codes_d = db.select_all_codes()
        # codes = []
        # if len(codes_d) > 0:
        #     for i in range(len(codes_d)):
        #         codes.append(codes_d[i]["code"])
        # if code in codes:
        #     db.insert_player((id_player,id_quiz))
        # else:
        id_quiz = db.select_id_quiz_using_code((session["CODE"],))[0]["id_quiz"]
        session["PLAYER"] = player_name
        db.insert_player_status((player_name,id_quiz,session["CODE"],0))
        #emit("new player", {"playername":player_name},namespace = "quiz")
        return render_template("quiz_guest.html")
    if request.method == "POST":
        
        return render_template("index.html")

@app.route("/enter_name")
def enter_name():
    if request.method == "GET":
        code = int(request.args.get("game_code"))
        codes_d = db.select_all_codes()
        codes = []
        if len(codes_d) > 0:
            for i in range(len(codes_d)):
                codes.append(int(codes_d[i]["code"]))
        if code in codes:
            # id_quiz = db.select_id_quiz_using_code((code,))[0]["id_quiz"]
            # print(id_quiz)
            # db.insert_player((player,id_quiz))
            session["CODE"] = code
            return render_template("enter_name.html")
        else:
            return redirect(url_for("index"))
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("enter_name.html")
@app.route("/showing_quiz_leader")
def showing_quiz_leader():
    db.change_quiz_status((session["CODE"],))
    id_quiz = db.select_id_quiz_using_code((session["CODE"],))[0]["id_quiz"]
    questions = db.select_questions((id_quiz,))
    print(questions)
    answers = {}
    right_answers = {}
    for i in range(len(questions)):
        id = questions[i]["id"]
        answers[id] = db.select_answers(questions[i]["id"],)
    ids = list(answers.keys())
    session["ID_ANSWER"] = ids[0]
    session["AMOUNT_QUESTIONS"] = 0
    print("ANSWERS",answers)
    session["ID_INDEX"] = 0
    d = {
        "picture":questions[session["ID_INDEX"]]["picture"][questions[session["ID_INDEX"]]["picture"].index('/'):],
        "question":questions[session["ID_INDEX"]]["question"],
        "first_answer":answers[session["ID_ANSWER"]][0]["answer"],
        "second_answer":answers[session["ID_ANSWER"]][1]["answer"],
        "third_answer":answers[session["ID_ANSWER"]][2]["answer"],
        "fourth_answer":answers[session["ID_ANSWER"]][3]["answer"]
    }
    return render_template("showing_quiz_leader.html",**d)
@app.route("/showing_quiz_next_question")
def showing_quiz_next_question():
    db.change_quiz_status((session["CODE"],))
    id_quiz = db.select_id_quiz_using_code((session["CODE"],))[0]["id_quiz"]
    questions = db.select_questions((id_quiz,))
    answers = {}
    right_answers = {}
    for i in range(len(questions)):
        id = questions[i]["id"]
        answers[id] = db.select_answers(questions[i]["id"],)
    ids = list(answers.keys())
    print("№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№",session["AMOUNT_QUESTIONS"])
    if  session["AMOUNT_QUESTIONS"]+1 == len(ids):
        session["ID_ANSWER"] = 0
        session["AMOUNT_QUESTIONS"] = 0
        session["ID_INDEX"] = 0
        code = session["CODE"]
        id_quiz = db.select_id_quiz_using_code((code,))[0]["id_quiz"]
        players_and_scores = db.select_player_and_score((session["CODE"],))
        print("PLAYERS_AND_SCORES",players_and_scores)
        players = []
        scores = []
        for i in range(len(players)):
            players.append(players_and_scores[i]["player"])
            scores.append(players_and_scores[i]["score"])
        d = {
            "players":players,
            "scores":scores,
            "len":len(scores)
        }
        return redirect(url_for("final_score"))
    session["ID_INDEX"] += 1
    session["ID_ANSWER"] = ids[session["ID_INDEX"]]
    
    
    
    session["AMOUNT_QUESTIONS"] += 1
    print("ANSWERS",answers)
    

    d = {
        "picture":questions[session["ID_INDEX"]]["picture"][questions[session["ID_INDEX"]]["picture"].index('/'):],
        "question":questions[session["ID_INDEX"]]["question"],
        "first_answer":answers[session["ID_ANSWER"]][0]["answer"],
        "second_answer":answers[session["ID_ANSWER"]][1]["answer"],
        "third_answer":answers[session["ID_ANSWER"]][2]["answer"],
        "fourth_answer":answers[session["ID_ANSWER"]][3]["answer"]
    }
    return render_template("showing_quiz_next_question.html",**d)
@app.route("/final_score")
def final_score():
    code = session["CODE"]
    id_quiz = db.select_id_quiz_using_code((code,))[0]["id_quiz"]
    players_and_scores = db.select_player_and_score((session["CODE"],))
    print("PLAYERS_AND_SCORES",players_and_scores)
    players = []
    scores = []
    for i in range(len(players_and_scores)):
        players.append(players_and_scores[i]["player"])
        scores.append(players_and_scores[i]["score"])
    # d = {
    #     "players":players,
    #     "scores":scores,
    #     "len":len(scores)
    # }
    d = {}
    for i in range(len(players)):
        d[players[i]] = scores[i]
    print("D",d)
    return render_template("final_score.html",d=d)
@socketio.on("is_there_new_player")
def is_there_new_player(d):
    print("players",d)
    code = d["text"]
    code = code[code.index(":")+2:]
    players = db.find_players_using_code((code,))
    players_list = []
    for i in range(len(players)):
        players_list.append(players[i]["player"])
    emit("players_list",players_list)

@socketio.on("quiz_started")
def check_quiz_started(s):
    res = db.check_quiz_status((session["CODE"],))
    if res:
        id_quiz = db.select_id_quiz_using_code((session["CODE"],))[0]["id_quiz"]
        questions = db.select_questions((id_quiz,))
        print(questions)
        answers = {}
        right_answers = {}
        for i in range(len(questions)):
            id = questions[i]["id"]
            answers[id] = db.select_answers(questions[i]["id"],)
        session["ID_QUESTION"] = questions[0]["id"]
        socketio.emit("started_quiz")
@socketio.on("player_answered")
def player_answered(val):
    id=session["ID_QUESTION"]
    answers = db.select_answers((id,))
    id_quiz = db.select_id_quiz_using_code((session["CODE"],))[0]["id_quiz"]
    questions = db.select_questions((id_quiz,))
    print(questions)
    answers = {}
    right_answers = {}
    print("OTVETY",db.select_answers(questions[session["ID_QUESTION"]]["id"],))
    print(questions[session["ID_QUESTION"]])
    for i in range(len(questions)):
        id = questions[i]["id"]
        answers[id] = db.select_answers(questions[i]["id"],)
    answers = db.select_answers(questions[session["ID_QUESTION"]]["id"],)
    session["ID_QUESTION"] = questions[session["ID_QUESTION"]+1]["id"]
    user_ans = answers[int(val)-1]["rightanswer"]
    score = db.select_score((session["PLAYER"],))[0]["score"]
    score += user_ans*1000
    db.change_score((score,session["PLAYER"]))
    print(score)
if __name__=="__main__":
    
    socketio.run(app, port=3000)

# uploads_dir = os.path.join(app.instance_path, 'uploads') 
# os.makedirs(uploads_dir, exists_ok=True) 