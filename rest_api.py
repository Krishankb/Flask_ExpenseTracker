from flask import Flask,jsonify
from classObject import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Project"

@app.route("/expenses/creategroup", methods = ["POST"])
def get():
    # jsonify({'Expenses' : expenses})
    return GroupTracker().post()

@app.route("/expenses/<string:group_name>" , methods = ["GET"])
def get_expenses(group_name):
    #return jsonify({"expenses": expenses[expense_id]})
    return GroupTracker().get(group_name) 

@app.route("/expenses/<string:group_name>/add", methods = ["POST"])
def add_expenses(group_name):
    return ExpenseTracker().post(group_name)


@app.route("/expenses/<string:group_name>/update", methods = ["PUT"])
def update_expenses(group_name):
    return ExpenseTracker().put(group_name)

@app.route("/expenses/<string:group_name>/<string:expense_name>/delete", methods =["DELETE"])
def delete_expenses(group_name,expense_name):
    return ExpenseTracker().delete(group_name, expense_name)

@app.route("/expenses/<string:group_name>/balance_details" , methods = ["GET"])
def get_balanceDetails(group_name):
    return GroupTracker().get(group_name) 



if __name__=="__main__":
    app.run(debug=True)