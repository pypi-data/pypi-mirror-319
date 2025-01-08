# MongoRex

MongoRex is a powerful and easy-to-use Python library that simplifies MongoDB operations, providing a clean and reusable interface for CRUD, indexing, aggregation, and database management tasks. Whether you're building a small app or managing large-scale databases, MongoRex helps you interact with MongoDB effortlessly.

---

## 🚀 Features

- **CRUD Operations**: Simplify creating, reading, updating, and deleting MongoDB documents.
- **Index Management**: Efficiently create, drop, and list indexes to enhance performance.
- **Aggregation Pipeline**: Perform advanced queries using MongoDB’s aggregation framework.
- **Database Management**: Handle database and collection tasks with ease.
- **Transactions & Bulk Writes**: Streamline operations with session-based transactions and bulk write capabilities.
- **MapReduce**: Perform complex transformations and aggregations on data.
- **Distinct & Stats**: Get distinct values and gather database statistics.
- **Watch for Changes**: Monitor changes in collections or the entire database.
- **Server & Collection Stats**: Fetch detailed information about the server and individual collections.

---

## 📦 Installation

Install MongoRex using pip:

```bash
pip install mongorex
```

---

## 🛠️ Quick Start

Here’s how you can start using MongoRex in your Python application:

### 1. Initialize MongoRex

```python
from mongorex import DataBase

# Replace with your MongoDB URI and database name
mongo = DataBase(DB_Name="your_database", MongoURI="mongodb://localhost:27017")
```

### 2. Basic CRUD Operations

#### Add a Document

```python
document = {"name": "Alice", "age": 30}
mongo.add_doc("users", document)
```

#### Find Documents

```python
user = mongo.find_doc("users", {"name": "Alice"})
```

#### Update a Document

```python
mongo.update_doc("users", {"name": "Alice"}, {"age": 31})
```

#### Delete a Document

```python
mongo.delete_doc("users", {"name": "Alice"})
```

---

## 📚 Documentation

### **CRUD Operations**

- **add_doc(collection, document)**: Insert a single document into the specified collection.
- **add_docs(collection, documents)**: Insert multiple documents into the specified collection.
- **find_doc(collection, query)**: Retrieve a single document based on the query.
- **find_docs(collection, query)**: Retrieve multiple documents based on the query.
- **update_doc(collection, filter_query, update_data)**: Update a single document matching the filter.
- **update_docs(collection, filter_query, update_data)**: Update multiple documents matching the filter.
- **delete_doc(collection, query)**: Delete a single document matching the query.
- **delete_docs(collection, query)**: Delete multiple documents matching the query.

---

### **Aggregation**

- **aggregate(collection, pipeline)**: Perform advanced aggregation operations using MongoDB's aggregation pipeline.

---

### **Index Operations**

- **create_index(collection, keys, **kwargs)**: Create an index for the specified collection.
- **drop_index(collection, index_name)**: Drop an existing index from the collection.
- **list_indexes(collection)**: List all indexes for the given collection.

---

### **Collection & Database Management**

- **drop_collection(collection)**: Drop a collection from the database.
- **list_collections()**: List all collections in the database.
- **server_status()**: Retrieve the status of the MongoDB server.
- **db_stats()**: Get statistics about the database.
- **collection_stats(collection)**: Retrieve statistics for a specific collection.

---

### **Transactions & Bulk Write**

- **start_session()**: Start a new session for MongoDB transactions.
- **bulk_write(collection, operations)**: Perform bulk write operations on a collection.

---

### **Advanced Operations**

- **replace_doc(collection, filter_query, replacement)**: Replace a document with a new one.
- **distinct(collection, field, query=None)**: Retrieve distinct values for a specified field.
- **map_reduce(collection, map_function, reduce_function, out)**: Perform map-reduce operations on a collection.
- **rename_collection(old_name, new_name)**: Rename a collection.
- **watch(collection=None, pipeline=None)**: Watch for changes in a collection or the entire database.

---

### **Connection Management**

- **close_connection()**: Close the MongoDB connection safely.

---

## ⚙️ Requirements

- Python 3.6+
- pymongo library

To install required dependencies, simply run:

```bash
pip install pymongo
```

---

## 📝 License

MongoRex is licensed under the **CC-BY-SA 4.0** license. Feel free to use, modify, and share it, but make sure to give appropriate credit.

---

## 🏆 Contributors

MongoRex is developed and maintained by [TraxDinosaur](https://traxdinosaur.github.io). Contributions are welcome! Feel free to open an issue or create a pull request on [GitHub](https://github.com/TraxDinosaur/MongoRex).

---

## 🎯 Get Started Today

MongoRex simplifies the complexity of interacting with MongoDB. Whether you’re building a quick prototype or scaling a large system, MongoRex provides the tools you need to work with MongoDB databases efficiently.

Get started now and explore the full range of MongoRex capabilities!
