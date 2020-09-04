import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://root:rnsit@rnsece.5xj7v.mongodb.net/student_db?retryWrites=true&w=majority")
db = client.get_database('students_db')
collections=db.student_col

c=collections.find({})
for a in c:
    print(a["name"])


# collections.delete_one({'_id':1})
# collections.delete_many({'_id':1})


# student_update={
#     'name' : 'legend'
# }
#
# collections.update_one({'_id':1},{'$set': student_update})
# collections.update_many({'_id':1},{'$set': student_update})

# new_student={
#     '_id':1,
#     'sem':7,
#     'name':"hi"
# }
#
# collections.insert_one(new_student)
