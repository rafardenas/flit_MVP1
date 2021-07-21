# Flit_beta

Beta version of Flit, better said MVP
Web page to offer and request loads in Mexico logistics ecosystem


##### Updating the database after a push
```
$ heroku run python
>>> from flit_beta import db    
>>> from flit_beta import app
>>> db.init_app(app)
>>> app.app_context().push()
>>> db.create_all()
>>> db.session.commit()
>>> exit() \\
```






