# from flask import Flask,render_template
# from flask_bootstrap import Bootstrap
# from flask_script import Manager
# from flask_wtf import FlaskForm
# from wtforms import StringField
# app=Flask(__name__)
# manager=Manager(app)
# bootstrap=Bootstrap(app)
# class InputName(FlaskForm):
#     name=TextField('name',validators=[Required()])
# @app.route('/')
# def index():
#     return render_template('full_tang_poets_net.html')
# @app.route('/search',methods=['GET','POST'])
# def search():
#     form=InputName()
#     return render_template('main.html')
#
# if __name__=='__main__':
#     app.run(debug=True)
import os
from utils import read_qts
qts_list=[]
author_list=[]
qts_list,author_list=read_qts("./static/qts_zht.txt")
print(qts_list[0][2])
