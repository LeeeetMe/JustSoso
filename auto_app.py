from app import create_app

app = create_app()
app.run(host='127.0.0.1', port='8888', debug=True)
