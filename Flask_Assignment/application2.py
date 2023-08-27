from distutils.log import debug, error
from typing_extensions import Required
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, validates
from logging.config import dictConfig

from flask import session #a dictionary-like object that allows you to store data that persists across multiple requests within a user's 
#session. It's a way to maintain stateful information about a user's interaction with your web application at server side
# without relying solely on cookies or other client-side mechanisms.

import uuid #module provides tools for creating universally unique identifiers (UUIDs), which are unique across all devices and all time. 


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
                "filename": "app2.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console","file"]},
    }
)

data_lis = []
id_set = set()
myapp = Flask(__name__) #This instance represents our Flask web application. 
#The __name__ argument is used to determine the root path for the application.

#myapp.secret_key = "secret_key"

class Post_PutSchema(Schema):
    ID = fields.Int(required=True)
    Title = fields.Str(required=True)
    Status = fields.Bool(required=True)

    @validates('ID')
    def validate_ID(self, id):
        if id < 0:
            raise ValidationError("ID must not have negative value!")
        elif id in id_set:
            raise ValidationError("This ID already exists. You must enter unique ID.")

class PatchSchema(Schema):
    Title = fields.Str(required=False)
    Status = fields.Bool(required=False)

#class ListSchema(Schema):
    #data = fields.List(fields.Nested(Post_PutSchema))

#listschema = ListSchema()
patchschema = PatchSchema()
post_putschema = Post_PutSchema()

#This is a route definition using a decorator. The @myapp.route('/') line associates the following function with the URL path '/', 
#which is the root of the application. The hellofunc function is executed when a user accesses the root URL.
@myapp.route('/')
def hellofunc():
    """
    session["ctx"] = {"request_id": str(uuid.uuid4())} 
    """
    #generates a unique ID for our request and stores it in the newly created
    # "ctx" or "context" field in the dictionary-like object 'session'. 

    # Basically we are storing the state at server-side instead of the other popular mechanisms like cookies which are sent by server to the
    # client in the header of the response and then the client always includes the cookies in the headers of its requests to the same server.
    # This way the server knows that the request is coming from the same client and within the same session.

    myapp.logger.info("A user visited the home page >>>")
    return "Hello there!"

@myapp.route('/todos', methods=['GET'])
def getall():
    if len(data_lis) == 0:

        myapp.logger.info(
            "A user tried to retrieve all tasks when 0 tasks were added. >>>"
        )

        return jsonify(error="no tasks added yet!")

    title_filter = request.args.get('title')
    status_filter = request.args.get('status')
    limit = request.args.get('limit', default=None, type=int)

    filtered_tasks = data_lis.copy()

    if title_filter is not None:
        filtered_tasks = list(filter(lambda task: title_filter.lower() in task['Title'].lower(), filtered_tasks))

    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'  # Convert to bool
        filtered_tasks = list(filter(lambda task: task['Status'] == status_filter, filtered_tasks))

    if limit is not None:
        filtered_tasks = filtered_tasks[:limit]
    
    #serialized_tasks = listschema.dumps(filtered_tasks) #validation does not occur at the time of dump.
    
    myapp.logger.info(
        "A user retrieved all added tasks. >>>"
    )
    return jsonify(filtered_tasks), 200, {'Content-Type': 'application/json'} 
    
    #The jsonify() function in flask returns a flask.Response() object that already has the appropriate 
    #content-type header 'application/json' for use with json responses. Whereas, the json.dumps() method will just return an encoded string, 
    # which would require manually adding the MIME type header. jsonify() handles kwargs or dictionaries, while json.dumps() additionally 
    # supports lists and others.

@myapp.route('/todos', methods=['POST'])
def post_task():
    #body_dict = request.get_json()
    json_data = request.data.decode('utf-8')
    try:
        post_dict = post_putschema.loads(json_data)
    
    except ValidationError as err:
        #d = { "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}" }
        myapp.logger.info(
            "A user performed a POST operation with bad request body. | ValidationError: %s >>>", err.messages
        )
        return jsonify(err.messages), 400

    else:
        data_lis.append(post_dict)
        id_set.add(post_dict["ID"])
        myapp.logger.info(
            "A user performed a POST operation succesfully. >>>"
        )
        return jsonify({
            "success" : "The task has been added to the data dictionary successfully. Verify using GET localhost:5000/todos"
        }), 200


@myapp.route('/todos/<int:id>', methods=['DELETE'])
def del_task(id):
    flag = False
    for dict in data_lis:
        if dict["ID"] == id:
            flag = True
            data_lis.remove(dict)
            id_set.remove(id)

    if flag == False:
        myapp.logger.info(
            "A user tried to DELETE a task which doesn't exist. | ID: %s >>>", id
        )

        return jsonify(error="No task exists with this ID"), 404
    
    else:
        myapp.logger.info(
            "A user performed DELETE on a task successfully. | ID: %s >>>", id
        )

        return jsonify({
            "success" : "The task has been deleted the data dictionary successfully. Verify using GET localhost:5000/todos"
        }), 200

@myapp.route('/todos/<int:id>', methods=['GET'])
def get_by_id(id):
    flag = False
    req = {}
    for dict in data_lis:
        if dict["ID"] == id:
            flag = True
            req = dict

    if flag == False:

        myapp.logger.info(
            "A user tried to GET a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:

        myapp.logger.info(
            "A user performed GET on a task successfully. | ID: %s >>>", id
        )
        return jsonify(req), 200, {'Content-Type': 'application/json'} 
    

@myapp.route('/todos/<int:id>', methods=['PUT'])
def put_task(id):
    flag = False
    req = 0
    for i in range(len(data_lis)):
        dict = data_lis[i]
        if dict["ID"] == id:
            flag = True
            req = i

    if flag == False:
        myapp.logger.info(
            "A user tried to perform PUT on a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            put_dict = post_putschema.loads(json_data)
    
        except ValidationError as err:
            myapp.logger.info(
                "A user performed a PUT operation with bad request body. | ValidationError: %s >>>", err.messages
            )
            #d = { "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}" }
            return jsonify(err.messages), 400

        else:
            if put_dict["ID"] != id:
                myapp.logger.info(
                    "A user performed a PUT operation with ID provided in the body not matching with the ID provided in the path variable. | ID: %s >>>", id
                )
                return jsonify({
                    "error" : "ID provided in the body doesn't match with the ID provided in the path variable. ID should be same as it is a non modifiable attribute."
                }), 400

            data_lis[req] = put_dict
            myapp.logger.info(
                "A user performed PUT operation on a task successfully. | ID: %s >>>", id
            )
            return jsonify({
                "success" : "The task has been overwritten to the data dictionary successfully. Verify using GET localhost:5000/todos"
            }), 200


@myapp.route('/todos/<int:id>', methods=['PATCH'])
def patch_task(id):
    flag = False
    req = 0
    for i in range(len(data_lis)):
        dict = data_lis[i]
        if dict["ID"] == id:
            flag = True
            req = i

    if flag == False:
        myapp.logger.info(
            "A user tried to perform PATCH on a task which doesn't exist. | ID: %s >>>", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            patch_dict = patchschema.loads(json_data)
    
        except ValidationError as err:
            myapp.logger.info(
                "A user performed a PATCH operation with bad request body. | ValidationError: %s >>> ", err.messages
            )
            #d = { "error" : "The body must be a SUBSET of this format as these are the only attributes that can be modified - {Title : String val, Status: Boolean val}" }
            return jsonify(err.messages), 400

        else:

            data_lis[req].update(patch_dict)
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
