from . import admin


@admin.route('/')
def home():
    return '<h1>Welcome to Naaru</h1>'
