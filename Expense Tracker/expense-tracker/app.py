from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_tracker"
mongo = PyMongo(app)

# Home route
@app.route('/')
def index():
    expenses = mongo.db.expenses.find()
    return render_template('index.html', expenses=expenses)

# Add expense route
@app.route('/add', methods=['GET', 'POST'])
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Use .get() to safely access form data
        category = request.form.get('category')
        amount = request.form.get('amount')
        
        # Check if values are not None or empty
        if category and amount:
            try:
                amount = float(amount)
                mongo.db.expenses.insert_one({'category': category, 'amount': amount})
                return redirect(url_for('index'))
            except ValueError:
                # Handle case where amount is not a valid float
                return "Invalid amount format", 400
        else:
            # Handle case where category or amount is missing
            return "Category or amount is missing", 400
    
    return render_template('add_expense.html')


# Delete expense route
@app.route('/delete/<id>')
def delete_expense(id):
    mongo.db.expenses.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

