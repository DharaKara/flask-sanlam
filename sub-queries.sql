CREATE TABLE salesman (
    salesman_id INT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(255),
    commission DECIMAL(4, 2)
);
 
 
INSERT INTO salesman (salesman_id, name, city, commission) VALUES
(5001, 'James Hoog', 'New York', 0.15),
(5002, 'Nail Knite', 'Paris', 0.13),
(5005, 'Pit Alex', 'London', 0.11),
(5006, 'Mc Lyon', 'Paris', 0.14),
(5003, 'Lauson Hen', NULL, 0.12),
(5007, 'Paul Adam', 'Rome', 0.13);

CREATE TABLE orders (
    ord_no INT PRIMARY KEY,
    purch_amt DECIMAL(10, 2),
    ord_date DATE,
    customer_id INT,
    salesman_id INT
);
 
INSERT INTO orders (ord_no, purch_amt, ord_date, customer_id, salesman_id) VALUES
(70001, 150.5, '2012-10-05', 3005, 5002),
(70009, 270.65, '2012-09-10', 3001, 5005),
(70002, 65.26, '2012-10-05', 3002, 5001),
(70004, 110.5, '2012-08-17', 3009, 5003),
(70007, 948.5, '2012-09-10', 3005, 5002),
(70005, 2400.6, '2012-07-27', 3007, 5001),
(70008, 5760, '2012-09-10', 3002, 5001),
(70010, 1983.43, '2012-10-10', 3004, 5006),
(70003, 2480.4, '2012-10-10', 3009, 5003),
(70012, 250.45, '2012-06-27', 3008, 5002),
(70011, 75.29, '2012-08-17', 3003, 5007),
(70013, 3045.6, '2012-04-25', 3002, 5001);
 
 
Select * from Orders

--1. Sub query - write a query to display all the orders from the orders table issued by the salesman 'Paul Adam'
SELECT *
FROM orders
WHERE salesman_id = (
    SELECT salesman_id
    FROM salesman
    WHERE name = 'Paul Adam'
);

--2. Write a query to display all the orders which values are greater than the average order value for 10th October 2012.
SELECT *
FROM orders
WHERE purch_amt > (
	SELECT AVG(purch_amt)
    FROM orders
    WHERE ord_date = '2012-10-10'
);

-- 3. Write a query to find all orders with order amounts which are above-average amounts for their customers.
SELECT *
FROM orders o
WHERE purch_amt > (
    SELECT AVG(purch_amt)
    FROM orders
    WHERE customer_id = o.customer_id
);

--4. Write a query to find all orders attributed to a salesman in New York.
SELECT *
FROM orders
WHERE salesman_id IN (SELECT salesman_id FROM salesman WHERE city = 'New York');


--ragav gave this to us to do the following queries
CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    cust_name VARCHAR(255),
    city VARCHAR(255),
    grade INT NULL,
    salesman_id INT
);
 
 
INSERT INTO customer (customer_id, cust_name, city, grade, salesman_id) VALUES
(3002, 'Nick Rimando', 'New York', 100, 5001),
(3005, 'Graham Zusi', 'California', 200, 5002),
(3001, 'Brad Guzan', 'London', NULL, 5005),
(3004, 'Fabian Johns', 'Paris', 300, 5006),
(3007, 'Brad Davis', 'New York', 200, 5001),
(3009, 'Geoff Camero', 'Berlin', 100, 5003),
(3008, 'Julian Green', 'London', 300, 5002),
(3003, 'Jozy Altidor', 'Moscow', 200, 5007);

--5. Write a query to find the name and numbers of all salesmen who had more than one customer.
Select * 
from salesman 
where salesman_id 
In (Select salesman_id from customer 
	group by salesman_id
	having count(customer_id) > 1)

--All and any
--Find all the orders where purch_amt is more than gemma purch_amt
SELECT * FROM   orders where purch_amt > All (SELECT purch_amt FROM  orders where customer_id = 3005);
 
SELECT * FROM   orders where purch_amt > Any (SELECT purch_amt FROM  orders where customer_id = 3005);

--6.  Write a query to display only those customers whose grade are, in fact, higher than every customer in New York.
SELECT *
FROM customer
WHERE grade > ALL (
    SELECT grade
    FROM customer
    WHERE city = 'New York'
);

--7. Write a query to find all orders with an amount smaller than any amount for a customer in London.
SELECT *
FROM orders
WHERE purch_amt < ANY (
    SELECT purch_amt
    FROM orders
    WHERE customer_id IN (
        SELECT customer_id
        FROM customer
        WHERE city = 'London'
    )
);