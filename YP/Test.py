import sqlite3
from flask import Flask, render_template, request

conn = sqlite3.connect("YummyPeace.db")
c = conn.cursor()

c.execute("SELECT * FROM restaurants, food, menu WHERE restaurants.rid = menu.rid AND food.fid = menu.fid")
data = c.fetchall()

app = Flask(__name__)
Cafe = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food', methods = ['POST', 'GET'])
def food():
    if request.method == 'GET':
        return render_template('food_form.html')
    elif request.method == 'POST':
        Food = request.form['Food']
        Rest = []
        for i in data:
            lf = Food.lower()
            ld = i[-6].lower()
            if lf in ld:
                Rest.append([i[1], i[-6], i[-2], i[-1]])
        if Rest != []:
            return render_template('food_disp.html', Food = Food, Rest = Rest)
        else:
            return render_template('no_food_disp.html')

@app.route('/cafe', methods = ['POST', 'GET'])
def cafe():
    if request.method == 'GET':
        return render_template('cafe_form.html')

@app.route('/theCafes', methods = ['POST', 'GET'])
def theCafes():
    if request.method == 'POST':
        if(request.form.get('Cafe')):
            Rest = request.form['Cafe']
            count = 0
            Cafe.clear()
            for i in data:
                lf = Rest.lower()
                ld = i[1].lower()
                check = 0
                if lf in ld:
                    if Cafe != []:
                        for j in Cafe:
                            if ld == j.lower():
                                check = 1
                                break
                    if count == 0 or check == 0:
                        Cafe.append(i[1])
                        count+=1
            if Cafe != []:
                return render_template('cafe_disp.html', Cafe = Cafe, Rest = Rest)
            else:
                return render_template('no_cafe_disp.html')
        else:
            if(request.form.get("submit")):
                Rest = Cafe[int(request.form["submit"]) - 1]
                Menu = []
                for i in data:
                    lf = Rest.lower()
                    ld = i[1].lower()
                    if lf in ld:
                        Menu.append([i[-6], i[-2], i[-1]])
                return render_template('menu_disp.html', Rest = Rest, Menu = Menu)
            else:
                Rest = Cafe[int(request.form["details"]) - 1]
                Det = []
                for i in data:
                    lf = Rest.lower()
                    ld = i[1].lower()
                    if lf in ld:
                        Det = i[1:7]
                        break
                print (Det)
                return render_template('cafe_details.html', Rest = Rest, Det = Det)

@app.route('/cuisine/<ftype>', methods = ['POST','GET'])
def cuisine(ftype):
    if request.method == 'GET':
        Cafe.clear()
        for i in data:
            lf = ftype.lower()
            ld = i[-5].lower()
            if lf in ld:
                if i[1] not in Cafe:
                    Cafe.append(i[1])
        return render_template('cuisine_rest.html', Ftype = ftype, Rest = Cafe)
    if request.method == 'POST':
        Rest = Cafe[int(request.form["submit"])-1]
        Menu = []
        print (ftype)
        for i in data:
            lf = Rest.lower()
            ld = i[1].lower()
            if (lf in ld) and (ftype.lower() in i[-5]):
                Menu.append([i[-6], i[-2], i[-1]])
        return render_template('menu_disp_cuisine.html', Rest = Rest, Menu = Menu)

if __name__ == '__main__':
    app.run(debug = True)

c.close()
conn.close()
