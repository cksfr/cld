from pymongo import MongoClient

# ---------------- CONFIGURE ----------------
MONGO_URI = "mongodb+srv://cksfr:CKSG641014@cluster0.e5khcbv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Create or access database and collection
db = client['testdb']          # Database name (auto-created if doesn't exist)
collection = db['users']       # Collection name (auto-created if doesn't exist)

# ---------------- 1. Insert One Record ----------------
user = {"name": "Alice", "email": "alice@example.com", "age": 25}
insert_result = collection.insert_one(user)
print(f"Inserted One Record ID: {insert_result.inserted_id}")

# ---------------- 2. Insert Many Records ----------------
users = [
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 28},
    {"name": "Diana", "email": "diana@example.com", "age": 22}
]
insert_many_result = collection.insert_many(users)
print(f"Inserted Many Record IDs: {insert_many_result.inserted_ids}")

# ---------------- 3. List All Records ----------------
print("\nAll Records:")
for record in collection.find():
    print(record)

# ---------------- 4. List a Particular Record ----------------
print("\nRecord for Alice:")
alice = collection.find_one({"name": "Alice"})
print(alice)

# ---------------- 5. Update a Record ----------------
update_result = collection.update_one(
    {"name": "Alice"},
    {"$set": {"age": 26, "email": "alice_new@example.com"}}
)
print(f"\nModified Count: {update_result.modified_count}")

# Verify update
print("After Update:")
print(collection.find_one({"name": "Alice"}))

# ---------------- 6. Delete a Record ----------------
delete_result = collection.delete_one({"name": "Bob"})
print(f"\nDeleted Count: {delete_result.deleted_count}")

# Verify deletion
print("After Deletion of Bob:")
for record in collection.find():
    print(record)

# Close the connection
client.close()
