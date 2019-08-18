#this is the entry point of the whole application
from myspace import create_app

#this is where the app instance is created
app = create_app()

if __name__ == '__main__':
    app.run (debug=True)