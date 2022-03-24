



mongo_obj = db_initiator(db_config)

print(mongo_obj.get_one("accounts", {"Name":"Gnanesh Vemuri"}))
print(mongo_obj.get_list("accounts", {"Name":"Gnanesh Vemuri"}))
print(mongo_obj.del_one("accounts", {"Name":"Gnanesh Vemuri"}))
print(mongo_obj.create("Transactions", {"AccountNumber": 123456789, "Money": 100000}))