from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["catdb"]
    collection = db["cats"]
    # Checking the connection
    client.admin.command('ismaster')
    print("MongoDB connected successfully")
except ConnectionFailure:
    print("Failed to connect to MongoDB, check the connection")


# Create a document (Create)
def create_document():
    try:
        name = input("Enter the name of the animal: ")
        age = int(input("Enter the age of the animal: "))
        features_input = input("Enter the features of the animal, separated by commas: ")
        features = features_input.split(", ")
        document = {"name": name, "age": age, "features": features}
        collection.insert_one(document)
        print("Document created.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")
    except ValueError as e:
        print(f"Input error: {e}")


# Read all documents (Read)
def read_all_documents():
    try:
        documents = list(collection.find({}))
        if not documents:
            print("No records found.")
        else:
            for doc in documents:
                print(doc)
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")


# Read document by name (Read by Name)
def read_document_by_name():
    try:
        name = input("Enter the name of the animal: ")
        res = collection.find_one({"name": name})
        if res:
            print(res)
        else:
            print("Record not found.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")


# Update animal's age (Update Age)
def update_document_age():
    try:
        name = input("Enter the name of the animal: ")
        age = int(input("Enter the new age of the animal: "))
        res = collection.update_one({"name": name}, {"$set": {"age": age}})
        if res.matched_count:
            print("Age updated.")
        else:
            print("Record not found.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")
    except ValueError as e:
        print(f"Input error: {e}")


# Add feature to document (Update: Add Feature)
def add_feature_to_document():
    try:
        name = input("Enter the name of the animal: ")
        feature = input("Enter a new feature: ")
        res = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if res.matched_count:
            print("Feature added.")
        else:
            print("Record not found.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")


# Delete document by name (Delete)
def delete_document():
    try:
        name = input("Enter the name of the animal: ")
        res = collection.delete_one({"name": name})
        if res.deleted_count:
            print("Record deleted.")
        else:
            print("Record not found.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")


# Delete all documents (Delete All)
def delete_all_documents():
    try:
        res = collection.delete_many({})
        print(f"Deleted {res.deleted_count} records.")
    except PyMongoError as e:
        print(f"Error working with MongoDB: {e}")


# Main menu
def main():
    while True:
        print("\nAvailable actions:")
        print("1 - Create a record about the animal")
        print("2 - Show all records")
        print("3 - Search record by the animal's name")
        print("4 - Update the animal's age")
        print("5 - Add a feature to the animal")
        print("6 - Delete record by animal's name")
        print("7 - Delete all records")
        print("8 - Exit")
        choice = input("Choose an action: ")

        if choice == "1":
            create_document()
        elif choice == "2":
            read_all_documents()
        elif choice == "3":
            read_document_by_name()
        elif choice == "4":
            update_document_age()
        elif choice == "5":
            add_feature_to_document()
        elif choice == "6":
            delete_document()
        elif choice == "7":
            delete_all_documents()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
