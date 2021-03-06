#don't forget to set the 'FLASK_APP' env variable

import os 
import sys
#sys.path.append("..") #this was the key for everything
#sys.path.append(".") #this was the key for everything
sys.path.append(os.getcwd())
print(os.environ.get('FLASK_APP'))
#print(sys.path)
#if os.environ['FLASK_APP'] == None:
#    os.environ['FLASK_APP'] = "first"


from web_app.app import create_app, db
from web_app.app.models import User, Post, FletesTransportistas, CargasEmbarcadores

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User, 'Post': Post, 'FletesTransportistas':FletesTransportistas, 'CargasEmbarcadores':CargasEmbarcadores }

if __name__ == "__main__":
    app.run()



