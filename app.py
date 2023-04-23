from flask import Flask, render_template, request
import pickle

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def normalize_age():
    input_age = float(request.form['input_age'])
    age = input_age / 80
    return age


def normalize_sex():
    input_sex = str(request.form['input_sex'])
    if input_sex == 'male':
        sex = 0
    elif input_sex == 'female':
        sex = 1
    else:
        sex = -1
    return sex


def normalize_sblng_sps():
    input_sblng = int(request.form['input_sblng'])
    if input_sblng == 0:
        siblings_cnt = 0
    else:
        siblings_cnt = input_sblng / 8
    return siblings_cnt


def input_prnts_chldrn():
    input_prnts_chldrn = int(request.form['input_prnts_chldrn'])
    if input_prnts_chldrn == 0:
        parents_children = 0
    else:
        parents_children = input_prnts_chldrn / 6
    return parents_children


def normalize_fare():
    input_fare = float(request.form['input_fare'])
    if input_fare <= 0:
        price = 0
    elif input_fare <= 513:
        price = input_fare / 513
    else:
        price = 1
    return price


@app.route('/', methods=['POST'])
def calculate():
    with open('ModelDevelopment/svm_model.sav', 'rb') as f:
        model = pickle.load(f)

    age = normalize_age()
    sex = normalize_sex()
    siblings_spouses = normalize_sblng_sps()
    parents_children = normalize_sblng_sps()
    ticket_price = normalize_fare()
    ticket_class = float(request.form['input_fare'])
    input_embark = float(request.form['input_embark'])
    result = model.predict([[ticket_class, sex, age, siblings_spouses, parents_children, ticket_price, input_embark]])
    result_str = f"{result[0]}"

    return render_template('index.html', result=result_str)


if __name__ == '__main__':
    app.run(debug=True)
