from . import admin


@admin.route('/')
def home():
    return '<h1>Welcome to Naaru</h1><br><a href="/login">login</a>'

@admin.route('/login')
def login():
    return '<h1>login</h1>'
