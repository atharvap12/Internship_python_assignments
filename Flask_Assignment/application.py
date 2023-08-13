from distutils.log import debug, error
from flask import Flask, jsonify, request

data_lis = []
id_set = set()
myapp = Flask(__name__) #This instance represents our Flask web application. 
#The __name__ argument is used to determine the root path for the application.


#This is a route definition using a decorator. The @myapp.route('/') line associates the following function with the URL path '/', 
#which is the root of the application. The hellofunc function is executed when a user accesses the root URL.
@myapp.route('/')
def hellofunc():
    return "Hello there!"

@myapp.route('/todos', methods=['GET'])
def getall():
    if len(data_lis) == 0:
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
    
    return jsonify(filtered_tasks) #The jsonify() function in flask returns a flask.Response() object that already has the appropriate 
    #content-type header 'application/json' for use with json responses. Whereas, the json.dumps() method will just return an encoded string, 
    # which would require manually adding the MIME type header. jsonify() handles kwargs or dictionaries, while json.dumps() additionally 
    # supports lists and others.

@myapp.route('/todos', methods=['POST'])
def post_task():
    body_dict = request.get_json()
    if (list(body_dict.keys()) != ['ID', 'Title', 'Status']) or (type(body_dict["ID"]) != int or type(body_dict["Title"]) != str or type(body_dict["Status"]) != bool):
        return jsonify({
            "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}"
        })

    elif body_dict["ID"] < 0:
        return jsonify({
            "error" : "ID provided in the body must not be negative."
        })

    elif body_dict["ID"] in id_set:
        return jsonify({
            "error" : "ID provided in the body must be unique. A task with this ID already exists."
        })

    else:
        data_lis.append(body_dict)
        id_set.add(body_dict["ID"])
        return jsonify({
            "success" : "The task has been added to the data dictionary successfully. Verify using GET localhost:5000/todos"
        })

@myapp.route('/todos/<int:id>', methods=['DELETE'])
def del_task(id):
    flag = False
    for dict in data_lis:
        if dict["ID"] == id:
            flag = True
            data_lis.remove(dict)
            id_set.remove(id)

    if flag == False:
        return jsonify(error="No task exists with this ID")
    else:
        return jsonify({
            "success" : "The task has been deleted the data dictionary successfully. Verify using GET localhost:5000/todos"
        })

@myapp.route('/todos/<int:id>', methods=['GET'])
def get_by_id(id):
    flag = False
    req = {}
    for dict in data_lis:
        if dict["ID"] == id:
            flag = True
            req = dict

    if flag == False:
        return jsonify(error="No task exists with this ID")
    else:
        return jsonify(req)
    

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
        return jsonify(error="No task exists with this ID")
    else:
        body_dict = request.get_json()
        if (list(body_dict.keys()) != ['ID', 'Title', 'Status']) or (type(body_dict["ID"]) != int or type(body_dict["Title"]) != str or type(body_dict["Status"]) != bool):
            return jsonify({
                "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}"
            })

        elif body_dict["ID"] != id:
            return jsonify({
                "error" : "ID provided in the body doesn't match with the ID provided in the path variable. ID should be same as it is a non modifiable attribute."
            })

        elif body_dict["ID"] < 0:
            return jsonify({
                "error" : "ID provided in the body must not be negative. ID is a non modifiable attribute."
            })

        else:
            data_lis[req] = body_dict
            return jsonify({
                "success" : "The task has been overwritten to the data dictionary successfully. Verify using GET localhost:5000/todos"
            })


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
        return jsonify(error="No task exists with this ID")
    else:
        valid_keys = {'Title', 'Status'}  
        valid_types = {'Title': str, 'Status': bool}
        body_dict = request.get_json()

        for k, v in body_dict.items():
            if k not in valid_keys: #O(1) because it is a set.
                return jsonify({
                "error" : "The body must be a SUBSET of this format as these are the only attributes that can be modified - {Title : String val, Status: Boolean val}"
            })

            if not isinstance(v, valid_types[k]):
                return jsonify({
                "error" : "The body must be a SUBSET of this format and the values of keys should strictly be of following types - {Title : String val, Status: Boolean val}"
            })
            
        data_lis[req].update(body_dict)
        return jsonify({
            "success" : "The task has been modified to the data dictionary successfully. Verify using GET localhost:5000/todos"
        })

    '''
        is_sublist = all(item in ['ID', 'Title', 'Status'] for item in body_keys)
        if is_sublist == False or (type(body_dict["ID"]) != int or type(body_dict["Title"]) != str or type(body_dict["Status"]) != bool):
            return jsonify({
                "error" : "the body must be a SUBSET of this format - {ID : Int val, Title : String val, Status: Boolean val}"
            })
        '''


if __name__ == "__main__":
    myapp.run(debug=True)




