from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector as sql

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

# Database connection
conn = sql.connect(host='localhost', user='root', password='12345678', database='ATM_MACHINE')
c1 = conn.cursor()

# Function to check if user exists
def user_exists(username, password):
    c1.execute("SELECT * FROM records WHERE ACCONT_NO = %s AND Password = %s", (username, password))
    user = c1.fetchone()
    return user is not None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if user_exists(username, password):
        session['username'] = username
        return redirect('/options')
    else:
        return render_template('login.html', message='Invalid username or password')

# Route for creating a new account
@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')  # Assuming you have a field for name in your form

    # Check if any of the required fields are empty
    if not username or not password or not name:
        return jsonify({'error': 'All fields are required'}), 400

    if user_exists(username, password):
        return jsonify({'error': 'Account already exists, please login'}), 400
    else:
        c1.execute("INSERT INTO records (ACCONT_NO, Password, Name) VALUES (%s, %s, %s)", (username, password, name))
        conn.commit()
        session['username'] = username
        return redirect('/deposit')


# Route for showing options
@app.route('/options')
def options():
    if 'username' in session:
        # Fetch the user's name from the database
        username = session['username']
        c1.execute("SELECT NAME FROM records WHERE ACCONT_NO = %s", (username,))
        user_name = c1.fetchone()[0]

        # Render the options template with welcome message and user's name
        return render_template('options.html', welcome_message='Welcome', name=user_name)
    else:
        return redirect('/')

# Route for depositing money
@app.route('/deposit')
def deposit():
    if 'username' in session:
        return render_template('deposit.html')
    else:
        return redirect('/')

# Route for processing deposit
@app.route('/process_deposit', methods=['POST'])
def process_deposit():
    if 'username' in session:
        amount = int(request.form.get('amount'))
        username = session['username']

        c1.execute("SELECT BALANCE FROM records WHERE ACCONT_NO = %s", (username,))
        balance = c1.fetchone()[0]

        new_balance = balance + amount

        c1.execute("UPDATE records SET BALANCE = %s WHERE ACCONT_NO = %s", (new_balance, username))
        conn.commit()

        return render_template('transaction_success.html', message=f'Deposit successful: {amount}', balance=new_balance)
    else:
        return redirect('/')

# Route for withdrawing money
@app.route('/withdraw')
def withdraw():
    if 'username' in session:
        return render_template('withdraw.html')
    else:
        return redirect('/')

# Route for processing withdrawal
@app.route('/process_withdraw', methods=['POST'])
def process_withdraw():
    if 'username' in session:
        amount = int(request.form.get('amount'))
        username = session['username']

        c1.execute("SELECT BALANCE FROM records WHERE ACCONT_NO = %s", (username,))
        balance = c1.fetchone()[0]

        if amount > balance:
            return render_template('error.html', message='Insufficient balance')

        new_balance = balance - amount

        c1.execute("UPDATE records SET BALANCE = %s WHERE ACCONT_NO = %s", (new_balance, username))
        conn.commit()

        return render_template('transaction_success.html', message=f'Withdrawal successful: {amount}', balance=new_balance)
    else:
        return redirect('/')

# Route for checking balance
@app.route('/check_balance')
def check_balance():
    if 'username' in session:
        username = session['username']

        c1.execute("SELECT BALANCE FROM records WHERE ACCONT_NO = %s", (username,))
        balance = c1.fetchone()[0]

        return render_template('balance.html', balance=balance)
    else:
        return redirect('/')

# Route for transferring money
@app.route('/transfer')
def transfer():
    if 'username' in session:
        return render_template('transfer.html')
    else:
        return redirect('/')

# Route for processing transfer
@app.route('/process_transfer', methods=['POST'])
def process_transfer():
    if 'username' in session:
        amount = int(request.form.get('amount'))
        recipient = request.form.get('recipient')
        sender = session['username']

        # Query sender's balance
        c1.execute("SELECT BALANCE FROM records WHERE ACCONT_NO = %s", (sender,))
        sender_balance = c1.fetchone()
        if sender_balance is None:
            return render_template('error.html', message='Sender account not found')

        sender_balance = sender_balance[0]

        # Query recipient's balance
        c1.execute("SELECT BALANCE FROM records WHERE ACCONT_NO = %s", (recipient,))
        recipient_balance = c1.fetchone()
        if recipient_balance is None:
            return render_template('error.html', message='Recipient account not found')

        recipient_balance = recipient_balance[0]

        # Check if sender has sufficient balance
        if amount > sender_balance:
            return render_template('error.html', message='Insufficient balance')

        # Update sender's balance
        sender_new_balance = sender_balance - amount
        c1.execute("UPDATE records SET BALANCE = %s WHERE ACCONT_NO = %s", (sender_new_balance, sender))

        # Update recipient's balance
        recipient_new_balance = recipient_balance + amount
        c1.execute("UPDATE records SET BALANCE = %s WHERE ACCONT_NO = %s", (recipient_new_balance, recipient))

        conn.commit()

        return render_template('transaction_success.html', message=f'Transfer successful: {amount}', balance=sender_new_balance)
    else:
        return redirect('/')


# Route for changing account number
@app.route('/change_account_number')
def change_account_number():
    if 'username' in session:
        return render_template('change_account_number.html')
    else:
        return redirect('/')

# Route for processing change account number
@app.route('/process_change_account_number', methods=['POST'])
def process_change_account_number():
    if 'username' in session:
        new_account_number = int(request.form.get('new_account_number'))
        username = session['username']

        c1.execute("UPDATE records SET ACCONT_NO = %s WHERE ACCONT_NO = %s", (new_account_number, username))
        conn.commit()

        return render_template('transaction_success.html', message='Account number changed successfully')
    else:
        return redirect('/')

# Route for logging out
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
