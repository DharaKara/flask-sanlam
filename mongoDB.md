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

```js
db.movies.find(
    {}, { _id: 0, name: 1, rating: 1 }.sort({rating: -1})
)
```
