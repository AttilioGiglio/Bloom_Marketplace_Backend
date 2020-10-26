To storage image
https://stackoverflow.com/questions/43309343/working-with-user-uploaded-image-in-flask
https://stackoverflow.com/questions/31325655/python-flask-uploading-image
https://stackoverflow.com/questions/62320284/react-best-practice-storing-images-on-server
https://stackoverflow.com/questions/60957369/flask-reactjs-file-uploading-not-working}
https://www.roytuts.com/python-flask-multiple-files-upload-example/
https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.scalar
# UPLOAD_FOLDER = 'uploads/test'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = 'uploads/test'
# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'pictures'
# configure_uploads(app, photos)
# from flask_uploads import UploadSet, configure_uploads, IMAGES
# from werkzeug.utils import secure_filename
dasdsa
  # image_filename = photos.save(request.files['thefile'])  
    #         return 
    # if request.method == 'POST':
    #     # check if the post request has the file part
	# 	if 'file' not in request.files:
	# 		flash('No file part')
	# 		return redirect(request.url)
	# 	file = request.files['file']
	# 	if file.filename == '':
	# 		flash('No file selected for uploading')
	# 		return redirect(request.url)
	# 	if file and allowed_file(file.filename):
	# 		filename = secure_filename(file.filename)
	# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	# 		flash('File successfully uploaded')
	# 		return redirect('/')
	# 	else:
	# 		flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
	# 		return redirect(request.url)
    
    # file = request.files['inputFile']
    # newFile = Img(data=file.read(), name=file.filename)
    # db.session.add(newFile)
    # db.sesison.commit()
    # return 'saved'+file.filename+' to the database!'
    
    # if not pic:
    #     return 'No pic uploaded!', 400
    # new_img =request.json.get('image', None)
    # filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype
    # if not filename or not mimetype:
    #     return 'Bad upload!', 400

    # img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    # target = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    # logger.info("welcome to upload`")
    # file = request.files['file']
    # filename = secure_filename(file.filename)
    # destination = "/".join([target, filename])
    # file.save(destination)
    # session['uploadFilePath'] = destination
    # response = "Whatever you wish too return"
    # return response


PENDIENTES

- HACER FUNCION PARA ALMACENAR IMAGENES EN LA DB



# Flask Boilerplate for Profesional Development

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/from-referrer/)
<p align="center">
    <a href="https://youtu.be/ORxQ-K3BzQA"><img height="200px" src="https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/assets/how-to.png?raw=true" /></a>
</p>

## Features

- Extensive documentation [here](https://github.com/4GeeksAcademy/flask-rest-hello/tree/master/docs).
- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## Installation (automatic if you are using gitpod)

> Important: The boiplerplate is made for python 3.7 but you can easily change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv install;
mysql -u root -e "CREATE DATABASE example";
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
control+shift+f
```

## How to Start coding?

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:
```
$ pipenv run migrate (to make the migrations)
$ pipenv run upgrade  (to update your databse with the migrations)
```


# Manual Installation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `MySQL` installed on your computer and MySQL is running, then run the following commands:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```


## Deploy to Heroku

This template is 100% compatible with Heroku[https://www.heroku.com/], just make sure to understand and execute the following steps:

```sh
// Install heroku
$ npm i heroku -g
// Login to heroku on the command line
$ heroku login -i
// Create an application (if you don't have it already)
$ heroku create <your_application_name>
// Commit and push to heroku (commited your changes)
$ git push heroku master
```
:warning: For a more detailed explanation on working with .env variables or the MySQL database [read the full guide](https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/DEPLOY_YOUR_APP.md).
