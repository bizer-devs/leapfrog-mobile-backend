from datetime import datetime
from flask import render_template, request, jsonify
from sqlalchemy.exc import IntegrityError
from leapfrog import app, db
from leapfrog.models import User, PendingTransfer, Transfer, Leapfrog
from leapfrog.tools import new_transfer_code


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

        return 'User Created: {}'.format(request.form['username']), 201

    else:
        return 'Missing arguments', 400


@app.route('/pendingtransfers', methods=['GET'])
def get_pending_transfers():
    query = PendingTransfer.query.all()
    return jsonify(query)


@app.route('/pendingtransfers/<int:id>', methods=['GET'])
def get_pending_transfer(id):
    query = PendingTransfer.query.filter(PendingTransfer.id == id)
    try:
        return query[0], 200
    except IndexError:
        return 'Pending transfer {} not found'.format(id), 404


@app.route('/pendingtransfers', methods=['POST'])
def add_pending_transfer():
    try:
        old_holder = User.query.filter(User.id == request.form['old_holder_id'])[0]
    except IndexError:
        return 'User {} not found'.format(request.form['old_holder_id']), 404

    try:
        leapfrog = Leapfrog.query.filter(Leapfrog.id == request.form['leapfrog_id'])[0]
    except IndexError:
        return 'Leapfrog {} not found'.format(request.form['leapfrog_id']), 404

    if old_holder != leapfrog.holder:
        return 'Leapfrog {} not held by user {}'.format(request.form['leapfrog_id'], request.form['old_holder_id'])

    pending_transfer = PendingTransfer(old_holder=old_holder,
                                       leapfrog=leapfrog,
                                       transfer_code=new_transfer_code(30),
                                       time_created=datetime.utcnow())
    db.session.add(pending_transfer)
    try:
        db.session.commit()
    except IntegrityError:
        return 'Leapfrog {} is already involved in a pending transfer'.format(request.form['leapfrog_id']), 404

    return jsonify(pending_transfer), 201


@app.route('/pendingtransfers/<int:id>/confirm', methods=['POST'])
def confirm_pending_transfer(id):
    try:
        pending_transfer = PendingTransfer.query.filter(PendingTransfer.id == id)[0]
    except IndexError:
        return 'Pending transfer {} not found'.format(id), 404

    try:
        new_holder = User.query.filter(User.id == request.form['new_holder_id'])[0]
    except IndexError:
        return 'User {} not found'.format(request.form['new_holder_id']), 404

    if pending_transfer.transfer_code != request.form['transfer_code']:
        return 'Submitted transfer code does not match that of pending transfer', 403

    # update leapfrog's holder to new_holder
    pending_transfer.leapfrog.holder = new_holder

    # create new transfer object to represent leapfrog transfer
    num_previous_transfers = Transfer.query.filter(Transfer.leapfrog is PendingTransfer.leapfrog).count()
    transfer = Transfer(old_holder=pending_transfer.old_holder,
                        new_holder=new_holder,
                        leapfrog=pending_transfer.leapfrog,
                        transfer_number=num_previous_transfers+1,)

    # delete the transfer request
    db.session.delete(pending_transfer)

    db.session.add(transfer)
    db.session.commit()

    return jsonify(transfer), 201

@app.route('/transfers', methods=['GET'])
def get_transfers():
    query = Transfer.query.all()
    return jsonify(query)


@app.route('/leapfrogs', methods=['GET'])
def get_leapfrogs():
    query = Leapfrog.query.all()
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

    return jsonify(leapfrog), 201