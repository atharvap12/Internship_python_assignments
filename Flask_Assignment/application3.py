from distutils.log import debug, error
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, post_load
from logging.config import dictConfig
from collections import defaultdict

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "app3.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console","file"]},
    }
)

myapp = Flask(__name__)
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(myapp)


class Task(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable = False)
    Status = db.Column(db.Boolean, nullable = False)
    
    """
    def __init__(self, ID, Title, Status):
        self.ID = ID
        self.Title = Title
        self.Status = Status
    """
    def __repr__(self):
        return f'<{self.title}:{self.status}>'

class Post_GetSchema(Schema):
    class Meta:
        model = Task  #read about model binding in 'class_Meta.txt' in notes folder.

    ID = fields.Int(dump_only = True)
    Title = fields.Str(required=True)
    Status = fields.Bool(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data) #data will actually be a dictionary deserialised from JSON. This ** unpacks the dictionary into key-value pairs
        #and passes it to the constructor of the 'Task' class

class PatchSchema(Schema):
    Title = fields.Str(required=False)
    Status = fields.Bool(required=False)

class PutSchema(Schema):
    Title = fields.Str(required=True)
    Status = fields.Bool(required=True)

patch_schema = PatchSchema()
put_schema = PutSchema()
post_get_schema = Post_GetSchema()
get_all_schema = Post_GetSchema(many=True)

#with myapp.app_context():   #Executed application3.py only upto this line. This will create the database file 'tasks.db' inside a folder called 
#    db.create_all()      #instances. The database will contain all the models and relationships defined before these two lines.


@myapp.route('/')
def hellofunc():

    myapp.logger.info("A user visited the home page >>>")
    return "Hello there!"


@myapp.route('/todos', methods=['GET'])
def getall():

    query = Task.query
    
    if (query.count() == 0):
        
        myapp.logger.info(
            "A user tried to retrieve all tasks when 0 tasks were added. >>>"
        )

        return jsonify(error="no tasks added yet!")


    title_filter = request.args.get('title')
    status_filter = request.args.get('status')
    limit_val = request.args.get('limit', default=None, type=int)
    offset_val = request.args.get('offset', default=None, type=int)

    if title_filter is not None:
        query = query.filter(Task.Title.ilike(f'%{title_filter}%'))

    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'  # Convert to bool
        query = query.filter(Task.Status == status_filter)

    if offset_val is not None:
        query = query.offset(offset_val)

    tasks = query.limit(limit_val).all() if limit_val is not None else query.all()

    serialized_tasks = get_all_schema.dumps(tasks)

    myapp.logger.info(
        "A user retrieved all added tasks. >>>"
    )
    
    return serialized_tasks, 200, {'Content-Type': 'application/json'}

@myapp.route('/todos', methods=['POST'])
def post_task():
    #body_dict = request.get_json()
    json_data = request.data.decode('utf-8')
    try:
        post_obj = post_get_schema.loads(json_data)
    
    except ValidationError as err:
        #d = { "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}" }
        myapp.logger.info(
            "A user performed a POST operation with bad request body. | ValidationError: %s >>>", err.messages
        )
        return jsonify(err.messages), 400

    else:
        db.session.add(post_obj)
        db.session.commit()
        myapp.logger.info(
            "A user performed a POST operation succesfully. >>>"
        )
        return jsonify({
            "success" : "The task has been added to the data dictionary successfully. Verify using GET localhost:5000/todos"
        }), 200

@myapp.route('/todos/<int:id>', methods=['DELETE'])
def del_task(id):
    t = Task.query.get(id)

    if t == None:
        myapp.logger.info(
            "A user tried to DELETE a task which doesn't exist. | ID: %s >>>", id
        )

        return jsonify(error="No task exists with this ID"), 404
    
    else:
        db.session.delete(t)
        db.session.commit()
        myapp.logger.info(
            "A user performed DELETE on a task successfully. | ID: %s >>>", id
        )

        return jsonify({
            "success" : "The task has been deleted the data dictionary successfully. Verify using GET localhost:5000/todos"
        }), 200

@myapp.route('/todos/<int:id>', methods=['GET'])
def get_by_id(id):
    t = Task.query.get(id)

    if t == None:

        myapp.logger.info(
            "A user tried to GET a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        serialized_task = post_get_schema.dumps(t)

        myapp.logger.info(
            "A user performed GET on a task successfully. | ID: %s >>>", id
        )
        return serialized_task, 200, {'Content-Type': 'application/json'} 

@myapp.route('/todos/<int:id>', methods=['PUT'])
def put_task(id):
    t = Task.query.get(id)

    if t == None:
        myapp.logger.info(
            "A user tried to perform PUT on a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            put_dict = put_schema.loads(json_data)
    
        except ValidationError as err:
            myapp.logger.info(
                "A user performed a PUT operation with bad request body. | ValidationError: %s >>>", err.messages
            )
            return jsonify(err.messages), 400

        else:
            for field, value in put_dict.items():
                setattr(t, field, value) #setattr(task, field, value) sets the value of the attribute named 'field' on the 'task' object to 
                #the value 'value'.

            db.session.commit()

            myapp.logger.info(
                "A user performed PUT operation on a task successfully. | ID: %s >>>", id
            )
            return jsonify({
                "success" : "The task has been PUT to the data dictionary successfully. Verify using GET localhost:5000/todos"
            }), 200


@myapp.route('/todos/<int:id>', methods=['PATCH'])
def patch_task(id):
    t = Task.query.get(id)

    if t == None:
        myapp.logger.info(
            "A user tried to perform PATCH on a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            patch_dict = patch_schema.loads(json_data)
    
        except ValidationError as err:
            myapp.logger.info(
                "A user performed a PATCH operation with bad request body. | ValidationError: %s >>> ", err.messages
            )
            return jsonify(err.messages), 400

        else:
            default_dict = defaultdict(int, patch_dict)

            title = default_dict['Title']
            status = default_dict['Status']

            if title != 0:
                t.Title = title

            if status != 0:
                t.Status = status

            db.session.commit()

            myapp.logger.info(
                "A user performed PUT operation on a task successfully. | ID: %s >>>", id
            )
            return jsonify({
                "success" : "The task has been modified to the data dictionary successfully. Verify using GET localhost:5000/todos"
            }), 200


@myapp.after_request
def logAfterRequest(response):

    myapp.logger.info(
        "path: %s | method: %s | status: %s | size: %s >>>",
        request.path,
        request.method,
        response.status,
        response.content_length,
    )

    return response

if __name__ == "__main__":
    myapp.run(debug=True)
