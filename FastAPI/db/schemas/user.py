### User schema ###

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "age": user["age"]}


            