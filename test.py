body_dict = {
    "ID" : 1,
    "Title" : "Mytask1",
    "Status" : False
}
"""
if (body_dict.keys() != ["ID", "Title", "Status"]) or (type(body_dict["ID"]) != int or type(body_dict["Title"]) != str or type(body_dict["Status"]) != bool):
        print({
            "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}"
        })

else:
        #data_lis.append(body_dict)
    print({
        "success" : "The task has been added to the data dictionary successfully. Verify using GET localhost:5000/todos"
    })
"""

print(list(body_dict.keys())) #  == ['ID', 'Title', 'Status'])