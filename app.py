from flask import Flask, render_template, request, redirect
import mysql.connector
import config

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', reviews=reviews)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        review = request.form['review']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reviews (title, author, review) VALUES (%s, %s, %s)", (title, author, review))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('submit.html')
if __name__ == '__main__':
    app.run(debug=True)
