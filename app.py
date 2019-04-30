import ipfsapi
from flask import Flask, render_template, session, redirect, url_for
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
class NameForm(Form):
    words = StringField('这是属于您的树洞，请说出任何您想说的话，不会有任何人知道您的真实身份', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/shudong',methods=['GET', 'POST'])
def getdata():
    api = ipfsapi.connect('129.211.27.244', 5001)
    form = NameForm()
    if form.validate_on_submit():
        with open('cont.txt','w') as f:
            session['words'] = form.words.data
            f.write(form.words.data)
        api.add('cont.txt')
        with open('cont.txt','w') as f:
            f.write("")
        return redirect(url_for('getdata'))
    return render_template('ipfs.html', form=form, words=session.get('words'))


if __name__ == '__main__':
    app.run()
