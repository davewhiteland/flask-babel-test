# i18n Flask Babel test

## Background

This is using [Flask-Babel](https://flask-babel.tkte.ch).


## Setup

Make sure you've got `flask` (the web framework) and `flask_babel` (the i18n
library that plays nicely with it):

    pip install flask
    pip install flask_babel

The repo has _no_ translations in it because I want to check/replicate the
process from scratch.

## How to run

Once it's setup, just run the Flask app (by default, Flask runs `app.py`):

    flask run

Then hit [localhost:5000](http://localhost:5000) and you should see:

> A simple string<br>
> Value: 42<br>
> 4 Apples

Note `mysettings.cfg` controls what languages you get back: to start with it's
`en`.

Kill flask (Crtl-C) and run the translation process...

## How to translate

### Extract strings

    pybabel extract -F babel.cfg -o messages.pot .

This will use the mapping from the babel.cfg file and store the generated
template in `messages.pot`.


### Generate the translation file

Pick your language: here `de` for German:

    pybabel init -i messages.pot -d translations -l de

`-d translations` tells pybabel to store the translations in this folder. This
is where Flask-Babel will look for translations. 

### Translate the words

Now edit the `translations/de/LC_MESSAGES/messages.po` file as needed.

For example (this is just the string mapping part of the file):

```
#: app.py:12
msgid "A simple string"
msgstr "Eine einfache Zeichenfolge"

#: app.py:14
#, python-format
msgid "Value: %(value)s"
msgstr "Wert: %(value)s"

#: app.py:16
#, python-format
msgid "%(num)s Apple"
msgid_plural "%(num)s Apples"
msgstr[0] "%(num) Apfel"
msgstr[1] "%(num) Äpfel"
```

### Compile the translation

First time (new file):

    pybabel compile -d translations

Subsequently (updating translations):

    pybabel update -i messages.pot -d translations

That creates `messages.mo` in the `translations/de` directory.

Afterwards some strings might be marked as fuzzy (where it tried to figure out
if a translation matched a changed key). If you have fuzzy entries, make sure to
check them by hand and remove the fuzzy flag before compiling. _There won't be
any fuzzy strings the first time you run this._


### Run with translation

See if that worked: change Flask default language to German:

Edit `mysettings.cfg` to 

    BABEL_DEFAULT_LOCALE = 'de'

Now start the app up again:

    flask run

then hit [localhost:5000](http://localhost:5000) again: you _should_ see this:

> Eine einfache Zeichenfolge<br>
> Wert: 42<br>
> 4 Äpfel

Did that work?

Spoiler: not for me: I'm getting this:

```
    return get_domain().ngettext(*args, **kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/flask_babel/__init__.py", line 605, in ngettext
    return s if not variables else s % variables
ValueError: unsupported format character 'A' (0x41) at index 7
```

Note there's a specific
[troubleleshooting tip](https://flask-babel.tkte.ch/#troubleshooting) in the
flask-babel docs  that looked encouraging... but nope.


---

### More detail when extracting

_Detail for later_:

If you are using the lazy_gettext() function you should tell pybabel that it
should also look for such function calls:

    pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
