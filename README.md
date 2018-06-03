
"""
Sets consist of passes
Set has an event type (Trick, Jump, Slalom)
Set has_many passes
TrickPass, JumpPass, SlalomPass
Table - Sets (id: PrimaryKey, notes: Text, event: String (Jump/Trick/Slalom))
Table - TrickPasses (id: PrimaryKey, setId: ForeignKey, trickName: String, trickPoints: Int, boatSpeed: Float)
Table - JumpPasses (id: PrimaryKey, setId: ForeignKey, boatSpeed: float, boatPath: String, rampHeight: Float, distance: Float)
Table - SlalomPasses (id: PrimaryKey, setId: ForeignKey, boatSpeed: Float, ropeLength: Float, buoyCount: Float)

GET /sets/ -> list of all sets
POST /sets/ -> create a new set of a type
DELETE
GET /sets/:id -> return passes of this set
DELETE
GET /trick/ -> return all trick sets
POST /trick/ -> create new trick pass
GET /jump/ -> return all jump sets
POST /jump/ -> create new jump pass
GET /slalom/ -> return all slalom sets
POST /slalom/ -> create new slalom pass

"""
