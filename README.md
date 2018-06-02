
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
POST /sets/:id -> create a new pass within a set
DELETE
GET /trick/ -> return all trick sets
GET /jump/ -> return all jump sets
GET /slalom/ -> return all slalom sets

"""
