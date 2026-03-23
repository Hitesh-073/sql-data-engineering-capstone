📄 Normalisation in EcommerceAnalytics Database
🔹 Overview

Normalisation is the process of structuring a relational database to:

reduce data redundancy
improve data integrity
ensure consistency
optimise storage and performance

👉 The EcommerceAnalytics database has been designed using normalisation principles up to Third Normal Form (3NF).

🔸 First Normal Form (1NF)

A table is in 1NF if:

all columns contain atomic (indivisible) values
each column contains values of a single data type
each row is uniquely identifiable using a primary key
there are no repeating groups or arrays
✅ Implementation in EcommerceAnalytics
Customers Table
CustomerID (PK)
FirstName (NOT NULL)
LastName (NOT NULL)
Email (NOT NULL, UNIQUE)
CreatedDate (NOT NULL)
Products Table
ProductID (PK)
ProductName (NOT NULL)
Category (NOT NULL)
Price (NOT NULL, CHECK ≥ 0)
Orders Table
OrderID (PK)
CustomerID (FK, NOT NULL)
OrderDate (NOT NULL)
TotalAmount (NOT NULL, CHECK ≥ 0)
OrderItems Table
OrderItemID (PK, IDENTITY)
OrderID (FK, NOT NULL)
ProductID (FK, NOT NULL)
Quantity (NOT NULL, CHECK > 0)
UnitPrice (NOT NULL, CHECK ≥ 0)

👉 All values are atomic
👉 No repeating columns such as Product1, Product2, etc.

🎯 Therefore, the schema satisfies 1NF

🔸 Second Normal Form (2NF)

A table is in 2NF if:

it is already in 1NF
there are no partial dependencies
🔍 Partial Dependency Explained

A partial dependency occurs when:

👉 A non-key attribute depends on only part of a composite key

❌ Example (Not in 2NF)
OrderID	ProductID	ProductName	Quantity

👉 If (OrderID, ProductID) is the primary key:

Quantity depends on both columns ✅
ProductName depends only on ProductID ❌

👉 This creates a partial dependency

✅ After Applying 2NF

To resolve this, product-related attributes are separated into the Products table.

Products Table
ProductID (PK)
ProductName
Category
Price
OrderItems Table
OrderItemID (PK)
OrderID (FK)
ProductID (FK)
Quantity
UnitPrice

👉 Product details are stored separately
👉 Order line details are stored in OrderItems

🎯 This reduces redundancy and resolves partial dependency issues

👉 Although OrderItems uses a surrogate key (OrderItemID) instead of a composite primary key, the design still follows 2NF principles by separating product data from order line data

🔸 Third Normal Form (3NF)

A table is in 3NF if:

it is already in 2NF
there are no transitive dependencies
🔍 Transitive Dependency Explained

A transitive dependency occurs when:

👉 A non-key column depends on another non-key column

❌ Example (Not in 3NF)
Suppose the Customers table is designed as:

CustomerID (PK)
FirstName
LastName
Email
Postcode
City

👉 If:

Postcode → City

Then:

CustomerID → Postcode → City

👉 This is a transitive dependency

✅ After Applying 3NF

To fix this, postcode data is separated into a lookup table.

Customers Table
CustomerID (PK)
FirstName
LastName
Email
Postcode
Postcodes Table
Postcode (PK)
City

👉 Now, each non-key attribute depends only on the primary key of its own table

🎯 This removes the transitive dependency

🔹 Keys and Constraints in OrderItems Table

The OrderItems table includes the following key design elements:

OrderItemID → Primary Key (surrogate key)
OrderID → Foreign Key referencing Orders(OrderID)
ProductID → Foreign Key referencing Products(ProductID)

👉 A unique constraint is defined:

UNIQUE (OrderID, ProductID)

👉 This ensures:

the same product cannot appear multiple times within the same order
the combination of OrderID and ProductID is unique

🎯 Therefore:

(OrderID, ProductID) forms a composite candidate key
OrderItemID remains the primary (surrogate) key
✅ 3NF in OrderItems Table

The OrderItems table satisfies 3NF because:

Quantity depends on the order item row
UnitPrice depends on the order item row
product attributes (ProductName, Category, Price) are stored in the Products table

👉 No non-key column depends on another non-key column

🎯 Therefore, OrderItems satisfies 3NF

🎯 Final Design Summary

The EcommerceAnalytics database achieves:

1NF → atomic columns with no repeating groups
2NF → no partial dependencies through separation of product and order data
3NF → no transitive dependencies through proper table design and lookup separation
🚀 Final Note

👉 This schema design follows best practices for OLTP systems and:

improves data consistency
reduces redundancy
supports scalability
enables efficient querying