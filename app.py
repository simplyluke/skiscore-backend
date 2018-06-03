from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

 # configs
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(16), index=True)
    notes = db.Column(db.Text)
    trickPasses = db.relationship("TrickPass", backref='set', lazy='dynamic')
    jumpPasses = db.relationship("JumpPass", backref='set', lazy='dynamic')
    slalomPasses = db.relationship("SlalomPass", backref='set', lazy='dynamic')

    def __repr__(self):
        return '<Set {}>'.format(self.id)

    def toJson(self):
        retDict = {'id': self.id, 'event': self.event, 'notes': self.notes}
        appendPasses = []
        if self.event == "Slalom":
            for slalom in self.slalomPasses:
                appendPasses.append(slalom.toJson())
            retDict['slalomPasses'] = appendPasses

        elif self.event == "Jump":
            for jump in self.jumpPasses:
                appendPasses.append(jump.toJson())
            retDict['jumpPasses'] = appendPasses

        elif self.event == "Trick":
            for trick in self.trickPasses:
                appendPasses.append(trick.toJson())
            retDict['trickPasses'] = appendPasses

        else:
            return {"error": "Event Type Undefined"}

        return retDict

class TrickPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setId = db.Column(db.Integer, db.ForeignKey('set.id'))
    name = db.Column(db.String(128), index=True)
    points = db.Column(db.Integer)
    speed = db.Column(db.Float)
    zoSetting = db.Column(db.String(8))

    def __repr__(self):
        return '<TrickPass {}>'.format(self.id)

    def toJson(self):
        return {
            'id': self.id,
            'setId': self.setId,
            'name': self.name,
            'points': self.points,
            'speed': self.speed,
            'zoSetting': self.zoSetting
        }

class JumpPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setId = db.Column(db.Integer, db.ForeignKey('set.id'))
    boatPath = db.Column(db.String(128))
    distance = db.Column(db.Float)
    speed = db.Column(db.Float)
    rampHeight = db.Column(db.Float)
    zoSetting = db.Column(db.String(64))

    def __repr__(self):
        return '<JumpPass {}>'.format(self.id)

    def toJson(self):
        return {
            'id': self.id,
            'setId': self.setId,
            'boatPath': self.boatPath,
            'distance': self.distance,
            'speed': self.speed,
            'rampHeight': self.rampHeight,
            'zoSetting': self.zoSetting
        }

class SlalomPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setId = db.Column(db.Integer, db.ForeignKey('set.id'))
    ropeLength = db.Column(db.Float)
    boatSpeed = db.Column(db.Float)
    buoyCount = db.Column(db.Float)
    zoSetting = db.Column(db.String(8))

    def __repr__(self):
        return '<SlalomPass {}>'.format(self.id)

    def toJson(self):
        return {
            'id': self.id,
            'setId': self.setId,
            'ropeLength': self.ropeLength,
            'speed': self.boatSpeed,
            'buoyCount': self.buoyCount,
            'zoSetting': self.zoSetting
        }


# Routes
@app.route("/sets", methods=["GET"])
def sets_index():
    sets = Set.query.all()
    deserialized = []
    for skiset in sets:
        deserialized.append(skiset.toJson())
    return str(deserialized)

@app.route("/sets", methods=["POST"])
def new_set():
    # TODO: validate data
    content = request.get_json()

    if not ('event' in content and 'notes' in content):
        return(jsonify({"error": "Bad input"}), 400)

    jsonEvent = content["event"]
    jsonNotes = content["notes"]
    s = Set(event = jsonEvent, notes = jsonNotes)
    db.session.add(s)
    db.session.commit()
    return jsonify({"set_id": str(s.id)})

@app.route("/sets/<int:set_id>", methods=["DELETE"])
def delete_set(set_id):
    set = Set.query.get(set_id)
    for skiPass in set.slalomPasses:
        delete_slalom_pass(skiPass.id)
    for skiPass in set.trickPasses:
        delete_trick_pass(skiPass.id)
    for skiPass in set.jumpPasses:
        delete_jump_pass(skiPass.id)
    db.session.delete(set)
    db.session.commit()
    return jsonify({"success": "Set successfully deleted."})

@app.route("/sets/<int:set_id>", methods=["GET"])
def get_set(set_id):
    set = Set.query.get(set_id)
    return str(set.toJson())

@app.route("/slalom", methods=["GET"])
def get_slalom_sets():
    sets = Set.query.filter(Set.event == "Slalom")
    deserialized = []
    for skiset in sets:
        deserialized.append(skiset.toJson())
    return str(deserialized)

@app.route("/slalom", methods=["POST"])
def new_slalom_pass():
    # TODO: validate data
    content = request.get_json()

    if not ('setId' in content and 'ropeLength' in content and 'buoyCount' in content and 'speed' in content and 'zoSetting' in content):
        return(jsonify({"error": "Bad input"}), 400)

    jsonSetId = content["setId"]
    jsonRopeLength = content["ropeLength"]
    jsonBuoyCount = content["buoyCount"]
    jsonSpeed = content["speed"]
    jsonZoSetting = content["zoSetting"]
    sp = SlalomPass(setId = jsonSetId, ropeLength = jsonRopeLength, buoyCount = jsonBuoyCount, boatSpeed = jsonSpeed, zoSetting = jsonZoSetting)
    db.session.add(sp)
    db.session.commit()
    return jsonify({"pass_id": str(sp.id)})

@app.route("/slalom/<int:pass_id>", methods=["DELETE"])
def delete_slalom_pass(pass_id):
    skiPass = SlalomPass.query.get(pass_id)
    db.session.delete(skiPass)
    db.session.commit()
    return jsonify({"success": "Slalom pass successfully deleted."})

@app.route("/trick", methods=["GET"])
def get_trick_sets():
    sets = Set.query.filter(Set.event == "Trick")
    deserialized = []
    for skiset in sets:
        deserialized.append(skiset.toJson())
    return str(deserialized)

@app.route("/trick", methods=["POST"])
def new_trick_pass():
    # TODO: validate data
    content = request.get_json()

    if not ('setId' in content and 'name' in content and 'points' in content and 'speed' in content and 'zoSetting' in content):
        return(jsonify({"error": "Bad input"}), 400)

    jsonSetId = content["setId"]
    jsonName = content["name"]
    jsonPoints = content["points"]
    jsonSpeed = content["speed"]
    jsonZoSetting = content["zoSetting"]
    tp = TrickPass(setId = jsonSetId, name = jsonName, points = jsonPoints, speed = jsonSpeed, zoSetting = jsonZoSetting)
    db.session.add(tp)
    db.session.commit()
    return jsonify({"pass_id": str(tp.id)})

@app.route("/trick/<int:pass_id>", methods=["DELETE"])
def delete_trick_pass(pass_id):
    skiPass = TrickPass.query.get(pass_id)
    db.session.delete(skiPass)
    db.session.commit()
    return jsonify({"success": "Trick pass successfully deleted."})

@app.route("/jump", methods=["GET"])
def get_jump_sets():
    sets = Set.query.filter(Set.event == "Jump")
    deserialized = []
    for skiset in sets:
        deserialized.append(skiset.toJson())
    return str(deserialized)

@app.route("/jump", methods=["POST"])
def new_jump_pass():
    # TODO: validate data
    content = request.get_json()

    if not ('setId' in content and 'boatPath' in content and 'distance' in content and 'speed' in content and 'zoSetting' in content and 'rampHeight' in content):
        return(jsonify({"error": "Bad input"}), 400)

    jsonSetId = content["setId"]
    jsonBoatPath = content["boatPath"]
    jsonDistance = content["distance"]
    jsonSpeed = content["speed"]
    jsonRampHeight = content["rampHeight"]
    jsonZoSetting = content["zoSetting"]
    jp = JumpPass(setId = jsonSetId, boatPath = jsonBoatPath, distance = jsonDistance, speed = jsonSpeed, rampHeight = jsonRampHeight, zoSetting = jsonZoSetting)
    print(jp)
    db.session.add(jp)
    db.session.commit()
    return jsonify({"pass_id": str(jp.id)})

@app.route("/jump/<int:pass_id>", methods=["DELETE"])
def delete_jump_pass(pass_id):
    skiPass = JumpPass.query.get(pass_id)
    db.session.delete(skiPass)
    db.session.commit()
    return jsonify({"success": "Jump pass successfully deleted."})
