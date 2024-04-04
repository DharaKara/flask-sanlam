## Commands

```show dbs, db, use db, show collections```

```db.movies.insert()```

```db.movies.find()```

```db.collection.find({"id": "100"})```

```db.collection.find({rating: 8})```

ctrl + space for auto complete

## Comparison Operators

```db.collection.find({rating: {$gt: 8}})```

SELECT * FROM movies
WHERE rating > 8;

```db.collection.find({rating: {$lt: 8}})```

SELECT * FROM movies
WHERE rating < 8;

```db.collection.find({rating: {$gte: 8}})```

SELECT * FROM movies
WHERE rating >= 8;

```db.collection.find({rating: {$lte: 8}})```

SELECT * FROM movies
WHERE rating <= 8;

```db.collection.find({rating: {"$in": [8.4,7,8.1]}})```

SELECT * FROM movies
WHERE rating IN (8.4, 7, 8.1);

```db.collection.find({rating: {$nin: [8.4,7,8.1]}})```

SELECT * FROM movies
WHERE rating NOT IN (8.4, 7, 8.1);

Task
1. flash - notification
2. Write equivalent Sql commands
3. Read about hash vs encryption

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
 
server = 'localhost'
database = 'YourDatabaseName'
username = 'YourUsername'
password = 'YourPassword'
driver_name = "ODBC Driver 17 for SQL Server"
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver_name}"
 
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)

## 04/04/2024

### projections

projections - inclusion
db.movies.find({}, {name:1, rating:1}).pretty()

projections - exclusion
db.movies.find({}, {summary:0, rating:0}).pretty()

you cant mix inclusion and exclusions together - will get an error.
the only exception you can get is exclude _id

dont need to use .pretty anymore as it is pretty already 

```js
db.movies.find(
    { rating: { $gt: 8.5 } },
    { _id: 0, name: 1, rating: 1 }
)
```

### compound sort

```js
db.movies.find({}, {_id: 0, name:1, rating:1}).sort({ rating:-1, name:1})
```

```js
db.movies.find({}, {_id: 0, name:1, rating:1}).sort({ rating:-1, name:1}).linit(3)
```

```js
db.movies.find({}, {_id: 0, name:1, rating:1}).sort({ rating:-1, name:1}).limit(3).skip(3)
```

### agreggations in mongo db

```js
db.orders.insertMany([
  { _id: 0, productName: "Steel beam", status: "new", quantity: 10 },
  { _id: 1, productName: "Steel beam", status: "urgent", quantity: 20 },
  { _id: 2, productName: "Steel beam", status: "urgent", quantity: 30 },
  { _id: 3, productName: "Iron rod", status: "new", quantity: 15 },
  { _id: 4, productName: "Iron rod", status: "urgent", quantity: 50 },
  { _id: 5, productName: "Iron rod", status: "urgent", quantity: 10 }
]);
```

```js
db.orders.find()
```

SELECT productName AS _id, SUM(quantity) AS totalQuantity
FROM orders
WHERE status = 'urgent'
GROUP BY productName;

```js
db.orders.aggregate([
  {
    $match: {
      status: "urgent"
    }
  },
  {
    $group: {
      _id: "$productName",
      totalQuantity: { $sum: "$quantity" }
    }
  }
])
```