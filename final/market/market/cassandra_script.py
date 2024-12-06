from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('my_keyspace')

session.default_consistency_level = ConsistencyLevel.ONE


# Insert data
session.execute("""
    INSERT INTO products (id, name, description, price, stock_quantity, category_id, created_at, updated_at)
    VALUES (uuid(), %s, %s, %s, %s, uuid(), toTimestamp(now()), toTimestamp(now()))
""", ('Product 2', 'Description 2', 20.99, 50))

rows = session.execute("SELECT * FROM products")
for row in rows:
    print(row)
