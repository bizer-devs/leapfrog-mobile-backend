from flask import render_template, request, jsonify
from leapfrog import app, db
from leapfrog.models import User, Transfer, Leapfrog


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route('/users', methods=['GET'])
def get_users():
    query = User.query.all()
    return jsonify(query), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    query = User.query.filter(User.id == id)
    if len(query) > 0:
        return jsonify(query), 200
    else:
        return 'User {} not found'.format(id), 404


@app.route('/users', methods=['POST'])
def new_user():
    if all(i in request.form for i in ['username', 'email']):
        user = User(username=request.form['username'],
                    email=request.form['email'])
        db.session.add(user)
        db.session.commit()

        return 'User Created: {}'.format(request.form['username'])

    else:
        return 'Missing arguments', 400


@app.route('/transfers', methods=['GET'])
def get_transfers():
    query = Transfer.query.all()
    return jsonify(query)


@app.route('/leapfrogs', methods=['GET'])
def get_leapfrog():
    query = Leapfrog.query.filter(Leapfrog.id == id)
    return jsonify(query)


@app.route('/leapfrogs/<int:id>', methods=['GET'])
def get_leapfrog(id):
    query = Leapfrog.query.filter(Leapfrog.id == id)
    if len(query) > 0:
        return jsonify(query)
    else:
        return 'Leapfrog {} not found'.format(id), 404


@app.route('/leapfrogs', methods=['POST'])
def new_leapfrog():
    try:
        # find user referenced by 'user_id'
        query = User.query.filter(User.id == request.form['user_id'])
        # nested try blocks: what separates the boys from the men
        try:
            user = query[0]
        except IndexError:
            return 'User with id {} was not found'.format(request.form['user_id'])

        # make the new leapfrog object and commit to our database
        leapfrog = Leapfrog(holder=user)
        db.session.add(leapfrog)
        db.session.commit()

    except AttributeError as e:
        return 'Missing arguments: {}'.format(str(e)), 400

    return jsonify(leapfrog), 200