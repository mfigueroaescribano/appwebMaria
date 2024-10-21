from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto a algo seguro

@app.route('/')
def home():
    db_config = session.get('db_config')
    if db_config is None:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        host = request.form['host']
        database = request.form['database']
        db_config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }
        try:
            conn = mysql.connector.connect(**db_config)
            session['db_config'] = db_config
            return redirect(url_for('list_databases'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('login.html')

@app.route('/databases')
def list_databases():
    db_config = session.get('db_config')
    if db_config is None:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Error: {err}"

    return render_template('databases.html', databases=databases)

@app.route('/databases/<db_name>/tables')
def list_tables(db_name):
    db_config = session.get('db_config')
    if db_config is None:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES FROM `{db_name}`")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Error: {err}"

    return render_template('tables.html', tables=tables, db_name=db_name)

@app.route('/databases/<db_name>/tables/<table_name>')
def view_table(db_name, table_name):
    db_config = session.get('db_config')
    if db_config is None:
        return redirect(url_for('login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{db_name}`.`{table_name}`")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Error: {err}"

    return render_template('view_table.html', data=data, db_name=db_name, table_name=table_name)

@app.route('/logout')
def logout():
    session.pop('db_config', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
