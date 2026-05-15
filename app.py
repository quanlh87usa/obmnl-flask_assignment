# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():

   return render_template("transactions.html", transactions = transactions) 

# Create operation
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template("form.html")
    else:
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))


# Update operation
@app.route("/edit/<int:transaction_id>", methods=['GET','POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction = transaction)
    
    return {"message": "transaction not found"}

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=['GET', 'POST'])
def search_transactions():
    search_transactions = []
    if request.method == 'POST':
        min_amount = request.form['min_amount']
        max_amount = request.form['max_amount']
        for transaction in transactions:
            if int(min_amount) <= int(transaction['amount']) <= int(max_amount):
                search_transactions.append(transaction)
        
        return render_template("search.html", transactions = search_transactions)

    else:
        return render_template("search.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
