# Field-Collection-Route-Optimization-using-PuLP-Library-Python

![alt text](https://github.com/gaptab/Field-Collection-Route-Optimization-using-PuLP-Library-Python/blob/main/472.png)

**Generating Data**

50 customers and 10 field collection agents are randomly placed across the country.

Each customer and agent is assigned a latitude and longitude to simulate real-world locations.

**Computing Distance Matrix**

We calculate the travel distance between each customer and agent using the Euclidean distance formula (as a proxy for real-world travel costs).

This results in a distance matrix showing how far each customer is from each agent.

**Defining the Optimization Problem**

The problem is set up as a Linear Programming (LP) minimization problem where the total travel distance is minimized.

**Decision Variables**

A binary variable (0 or 1) is assigned to each customer-agent pair.

1 → If the agent is assigned to that customer.

0 → Otherwise.

**Constraints to Ensure Feasibility**

Each customer is assigned to exactly one agent → Ensuring all customers are covered.

Each agent can handle a maximum number of customers → Avoiding overloading any single agent.

**Solving the Optimization Problem**

PuLP’s solver optimally assigns customers to agents while minimizing travel distance.
