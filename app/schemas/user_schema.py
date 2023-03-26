from pydantic import BaseModel

class CreateUser():
    first_name = str
    last_name= str
    email= str
    phone_number = str
    password = str
