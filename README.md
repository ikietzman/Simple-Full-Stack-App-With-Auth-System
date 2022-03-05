# Simple Full Stack App With Auth System

This application is intended as project boilerplate for simple applications and prototypes which need a quick and simple user-based auth system in place. It is not intended to be used in production, and you should assume it is insecure.

There are only two database tables, users and sessions, as can be seen in ./v0/schema.sql. Any further data storage will need to be added.

The back end (./v0) is built in Python 3, running Flask, and connects to a local sqlite instance.

The front end is built using Vue, with the Bulma CSS library. You can easily switch in a different CSS library, or add custom styles by starting at ./v0-front/src/assets/styles.scss.

Once installed and initialized, the full project should look something like this:

```
-/instance
-/v0
-/v0-front
-/venv
-.gitignore
-README.md
```

## Get started:

### Back End

```
git clone https://github.com/ikietzman/Simple-Full-Stack-App-With-Auth-System.git app_name

cd app_name

python3 -m venv venv

. venv/bin/activate

pip install flask flask_cors

flask init-db

export FLASK_APP=v0
export FLASK_ENV=development

flask run
```

### Front End

```
cd v0-front

npm install

npm run serve
```

The front end should then be accessible at http://127.0.0.1:8080.
