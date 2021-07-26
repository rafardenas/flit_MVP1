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


```
q1 = sess.query(SomeClass).filter(SomeClass.foo=='bar')
q2 = sess.query(SomeClass).filter(SomeClass.bar=='foo')

q3 = q1.union(q2)
```

**Is there a way to have a child DIV within a parent container DIV that is wider than it's parent. The child DIV needs to be the same width of the browser viewport.?**

```.child-div {
    position:absolute;
    left:0;
    right:0;
}
```

**CSS: how to position element in lower right?**
```
position: absolute;
bottom: 0;
right: 0;
```

**Pushing footer down**

[link](https://stackoverflow.com/questions/10099422/flushing-footer-to-bottom-of-the-page-twitter-bootstrap/36385654#36385654)

**Centering col-md-5**
[link](https://stackoverflow.com/questions/33379802/bootstrap-centering-col-md-5)

**Change rows for columns bootstrap**
[link](https://stackoverflow.com/questions/28046506/bootstrap-responsive-table-change-rows-with-column)


[link](https://stackoverflow.com/questions/25095591/how-do-i-connect-to-postgresql-using-ssl-from-sqlachemypg8000)