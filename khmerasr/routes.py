from khmerasr import app

@app.route('/')
def index_page():
    return 'Hello World'