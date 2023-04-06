import json
import firebase_admin
from firebase_admin import firestore
import functions_framework
from flask import request, jsonify


firebase_admin.initialize_app()
databaseClient = firestore.client()


@functions_framework.http
def elections_api(request):

    request_args = request.args

    if request.method == 'POST' and '/voter' in request.path:
        return registeringVoter()

    if request.method == 'POST' and '/election' in request.path:
        return creatingElection()
    
    if request.method == 'PUT' and '/voter' in request.path:
        return updatingVoters()
    
    if request.method == 'PUT' and '/election' in request.path:
        return updatingElection()

    if request.method == 'GET' and '/voter' in request.path:
        return gettingVoter(request.args['id'])
    
    if request.method == 'GET' and '/election' in request.path:
        return gettingElection(request.args['id'])

    if request.method == 'DELETE' and '/voter' in request.path:
        return deletingVoter(request.args['id'])
    
    if request.method == 'DELETE' and '/election' in request.path:
        return delete_election(request.args['id'])
    
    return jsonify({"Error": "Unknow Request"})


def registeringVoter():

    record = json.loads(request.data)
    
    voter = databaseClient.collection('voters').document(record['id'])
    if voter.get().exists:
        return jsonify({'Error': 'Voter exits'}), 409
    else:
        voter.set(record)
    return jsonify({'Message': 'Success'}), 200


def creatingElection():
    record = json.loads(request.data)
    
    election = databaseClient.collection('elections').document(record['id'])
    if election.get().exists:
        return jsonify({'Error': 'Unsuccessful'}), 409
    else:
        election.set(record)
    return jsonify({'Message': 'Success'}), 200


def gettingVoter(id):

    voter = databaseClient.collection('voters').document(id).get()
    if voter.exists:
        return jsonify(voter.to_dict())
    return jsonify({'Error': 'Data not found'}), 404

def gettingElection(id):
    election = databaseClient.collection('elections').document(id).get()
    if election.exists:
        return jsonify(election.to_dict()), 200
    return jsonify({'Error': "Unsuccessful"}), 404


def deletingVoter(id):

    voter = databaseClient.collection('voters').document(id).get()
    if voter.exists:
        voter.delete()
        return jsonify({'Message:': "Success"}), 200
    return jsonify({'Error': 'Data not found'}), 404

def delete_election():

    election_id = request.args['id']
    election = databaseClient.collection('elections').document(election_id).get()
    if election.exists:
        databaseClient.collection('elections').document(election_id).delete()
        return jsonify({'Message': 'Successful'}), 200
    return jsonify({'Error': "Unsuccessful"}), 404


def updatingVoters():

    record = json.loads(request.data)
    voterId = record['id']
    votersDocs = databaseClient.collection('voters').get()
    for doc in votersDocs:
        if doc.id == voterId:
            databaseClient.collection('voters').document(doc.id).update(record)
        return jsonify({'Message:': 'Success'}),200
    return jsonify({'Error': 'Data not found'}), 404
        
def updatingElection():
    record = json.loads(request.data)
    electionId = record['id']
    docs = databaseClient.collection('elections').get()
    for doc in docs:
        if doc.id == electionId:
            databaseClient.collection('elections').document(doc.id).update(record)
        return jsonify({'Message': 'Successful'}),200
    return jsonify({'Error': "Unsuccessful"}), 404

