from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.args.get("error"):
        b = request.args.get('error')
        return render_template('login.html', b = b)
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
def data_from_log():
    a = request.form
    for samth in a:
        print(samth)
        print(a.get(samth))
    return render_template('dashboard.html', a= a)

if __name__ == "__main__":
    app.run(debug=True)