# *************************************Quiz Web Project*************************************
#****************************************By Rohan Movva*************************************
#*******************************************************************************************


# Imports

# Flask imports
from flask import Flask, render_template, request, session, redirect, url_for
import json
import urllib.request as ur
# Random API to get a random number within a Range.
import random
# Data object
import Model
from Model import Item
from html import unescape

#Define the Flask App
app = Flask(__name__)
app.secret_key = "SnoopyIsMyDog"

# This is the main file for the project. It has 4 routes.
# 1. home. This will redirect the user to the start page.
# 2. start. Start displays the first page. In this page, the user can select the category and level.
# 3. nextQn. This page displays the question and 4 options.
# 4. check. This page checks if the user answered the question correct or not. It also displays the score.


# Redirect the user to the start page.
@app.route("/", methods=['POST', 'GET'])
def home():
    return redirect(url_for('start'))

# Starting page to select the category and level.
# The 2 session values are initialized to 0 to reset the counter.
# Count is to track the number of questions that are asked to the user.
# Score is to track the number of questions the user answered correctly.
@app.route("/start", methods=['POST', 'GET'])
def start():
    # Track the number of questions.
    session["count"] = 0
    # Track the number of correct answers.
    session["score"] = 0
    return render_template('selectCategory.html')


# This page does 2 things. It calls the rest api to get the question and answers for the selected category and
# displays the Question to the user.
@app.route("/nextQn", methods=['POST', 'GET'])
def nextQn():
    # Get the Cateogry and level from the request.
    category = request.form.get('category')
    level = request.form.get('level')
    # If the Math category is selected, generate the questions using the Random numbers.
    # For all other categories, go to the url
    if category == "math":
        operatorNum = random.randint(0, 1)
        correctAnswer = 0
        # Did the user select easy level?
        if level == "easy":
            # Get 2 random numbers.
            num1 = random.randint(1, 10)
            # Make the second number bigger than the first one.
            num2 = random.randint(num1, 20)
            # Calculate some incorrect values to display them to the user.
            a = int(num2 - num1 - 1)
            b = int(num2 + num1 + num1)
            c = int(num2 / (num1 + 1))
            d = int(num2 + (num1 - 1))
            # Pick the operator randomly + or - for easy.
            if operatorNum == 0:
                operator = "+"
                correctAnswer = num1 + num2
            elif operatorNum == 1:
                operator = "-"
                correctAnswer = num2 - num1
        # is the level Hard?
        else:
            # get 2 random numbers
            num1 = random.randint(1, 5)
            num2 = random.randint(num1, 10)

            # Calculate some incorrect values to display them to the user.
            a = int(num2 + num1 + 2)
            b = int(num2 * (num1 + 1))
            c = int(num2 / (num1 + 2))
            d = int(num2 + num1 + 23)
            # Pick the operator randomly * or / for hard.
            if operatorNum == 0:
                operator = "*"
                correctAnswer = num1 * num2
            elif operatorNum == 1:
                operator = "/"
                correctAnswer = num2 / num1

        # Set one of the answers to the correct answer. Pick the option Randomly.
        answerNum = random.randint(0, 3)
        if answerNum == 0:
            a = correctAnswer
            correctInputAnswer = "a"
        elif answerNum == 1:
            b = correctAnswer
            correctInputAnswer = "b"
        elif answerNum == 2:
            c = correctAnswer
            correctInputAnswer = "c"
        elif answerNum == 3:
            d = correctAnswer
            correctInputAnswer = "d"

        # format the question and options.
        question = "What is the value of {} {} {} ?".format(num2, operator, num1)

        # Load all the question information into a class.
        item = Item(question, a, b, c, d, correctAnswer, correctInputAnswer, category, level)
        # Pass the item object to the question.html file to render it on the browser.
        return render_template('question.html', item=item)
    else:
        # build the url with the category and level.
        url = "https://opentdb.com/api.php?amount=1&type=multiple&difficulty={}&category={}".format(str(level), str(category))
        print(url)
        # Read the response and parse the json response.
        html = ur.urlopen(url).read()
        # Load the response into a data array.
        data = json.loads(html.decode('utf-8'))

        # Get the question details from the array.
        question = unescape(data["results"][0]["question"])
        correct = unescape(data["results"][0]["correct_answer"])
        # Pick a random number to select the correct answer randomly between 0 and 3.
        # 0 = Option A, 1 = Option B, 2 = Option C, 3 = Option D
        answerNum = random.randint(0, 3)
        # If random number is 0, make Option A as a correct answer.
        if answerNum == 0:
            incorrect1 = unescape(data["results"][0]["correct_answer"])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "a"
        # If random number is 1, make Option B as a correct answer.
        elif answerNum == 1:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["correct_answer"])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "b"
        # If random number is 2, make Option C as a correct answer.
        elif answerNum == 2:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect3 = unescape(data["results"][0]["correct_answer"])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "c"
        # If random number is 3, make Option D as a correct answer.
        elif answerNum == 3:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][2])
            incorrect4 = unescape(data["results"][0]["correct_answer"])
            correctOption = "d"
        # Load all the question information into a class.
        item = Item(question, incorrect1, incorrect2, incorrect3, incorrect4, correct, correctOption, category, level)
        # Pass the item object to the question.html file to render it on the browser.
        return render_template('question.html', item=item)


# This method checks if the user selected the correct answer by comparing the user's selection to the correct option.
# It formats the display message based on the correct or wrong answer.
# It also calculates the score with a maximum of 5 questions.
# If the total questions reaches 5, it will hide the next button.
@app.route("/check", methods=['POST', 'GET'])
def check():
    # Get the Correct Answer options from the request.
    correctAnswer = request.form.get('correctAnswer')
    correctOption = request.form.get('correctOption')
    # Get the user selected option.
    userOption = request.form.get('q_answer')
    # Get the category and level.
    category = request.form.get('category')
    level = request.form.get('level')
    # Get the scores from the session.
    score = session["score"]
    count = session["count"]
    # Increment the total questions count.
    count = int(count)+1
    # Default the Next button to show.
    hideNextButton = "block"

    # Check if the user answered the question correctly.
    if correctOption == userOption:
        displayMessage = "Correct !! "
        # If the answer is correct, increment the score.
        score = int(score) + 1
    # If the user answer is incorrect, format the display message to show the correct answer.
    else:
        displayMessage = "Oops Not Correct!! The correct Answer is {}".format(correctAnswer)

    # If the total questions count is 5, display the final score and hide the next button.
    if int(count) == 5:
        scoreMessage = "Final Score is {}/5".format(score)
        # This is a javascript attribute to hide the button.
        hideNextButton="none"
    # If the total questions is less than 5, just display the current score.
    else:
        scoreMessage = "Score is {}".format(score)

    # Put the new score and count values in the session.
    session["count"] = count
    session["score"] = score
    # Pass all the information to the checkAnswer.html page to be rendered.
    return render_template('checkAnswer.html', displayMessage=displayMessage, scoreMessage=scoreMessage, category=category, level=level, hideNextButton=hideNextButton)


# This is the main method.
if __name__ == '__main__':
    # This secret key is used by Flask to manage unique sessions.
    # app.secret_key = "SnoopyIsMyDog"
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    # Run the app in debug mode on the local machine.
    app.run(debug=True, port=5000)

