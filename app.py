# -*- coding: utf-8 -*-
from flask import Flask
from flask_babel import Babel, gettext, ngettext

app = Flask(__name__)
app.config.from_pyfile('mysettings.cfg')
babel = Babel(app)

@app.route('/')
def hello_world():
    number_of_apples = 4
    s1 = gettext("A simple string")
    s2 = gettext("Value: %(value)s", value=42)
    s3 = ngettext("%(num)s Apple", "%(num)s Apples", number_of_apples)
    
    return "<br>\n".join([s1, s2, s3])
