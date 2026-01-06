from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

print("Connecting to mongodb")

db = client['school']

students = db['students']

student = {
    "name":"John",
    "age": 32,
    "mobile":'9383949284'
}

# insert data single entry
students.insert_one(student)

#insert data multiple entries
students.insert_many([
    {"name":"Merry", "age":23, "email":"merry@gmail.com"},
    {"name":"Ram", "age":43, "email":"ram@gmail.com"},
])

#read data
for student in students.find():
    print(student)

#find one
student = students.find_one({"name":"Ram"})
print(student)

#update one
students.update_one(
    {"name":"Merry"},
    {"$set":{"age":21}}
)

#delete one
students.delete_one({"name":"John"})

#read data
for student in students.find():
    print(student)

#list available databases
print(client.list_database_names())
