import pandas as pd
import numpy as np
import pulp
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Generate Dummy Data (50 customers, 10 agents)
np.random.seed(42)
num_customers = 50
num_agents = 10

# Create random coordinates for customers and agents (simulating locations across India)
customer_data = pd.DataFrame({
    'customer_id': range(1, num_customers + 1),
    'latitude': np.random.uniform(8, 37, num_customers),   # Approx Lat range of India
    'longitude': np.random.uniform(68, 97, num_customers)  # Approx Lon range of India
})

agent_data = pd.DataFrame({
    'agent_id': range(1, num_agents + 1),
    'latitude': np.random.uniform(8, 37, num_agents),
    'longitude': np.random.uniform(68, 97, num_agents)
})

# Step 2: Compute Distance Matrix (Euclidean Distance as Proxy for Travel Cost)
def compute_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)  # Approximate Euclidean distance

distance_matrix = pd.DataFrame(index=customer_data['customer_id'], columns=agent_data['agent_id'])

for i, cust in customer_data.iterrows():
    for j, agent in agent_data.iterrows():
        distance_matrix.at[cust['customer_id'], agent['agent_id']] = compute_distance(
            cust['latitude'], cust['longitude'], agent['latitude'], agent['longitude']
        )

distance_matrix = distance_matrix.astype(float)  # Convert to numeric

# Step 3: Define Optimization Model
model = pulp.LpProblem("Field_Collection_Optimization", pulp.LpMinimize)

# Step 4: Define Decision Variables (Binary)
assignments = pulp.LpVariable.dicts("Assign", 
                                    [(i, j) for i in customer_data['customer_id'] for j in agent_data['agent_id']], 
                                    cat='Binary')

# Step 5: Define Objective Function (Minimize Total Travel Distance)
model += pulp.lpSum([distance_matrix.at[i, j] * assignments[(i, j)] 
                     for i in customer_data['customer_id'] for j in agent_data['agent_id']])

# Step 6: Add Constraints
# Each customer is assigned to exactly one agent
for i in customer_data['customer_id']:
    model += pulp.lpSum(assignments[(i, j)] for j in agent_data['agent_id']) == 1

# Each agent can serve at most a certain number of customers
max_customers_per_agent = num_customers // num_agents  # Balanced assignment
for j in agent_data['agent_id']:
    model += pulp.lpSum(assignments[(i, j)] for i in customer_data['customer_id']) <= max_customers_per_agent

# Step 7: Solve the Optimization Problem
model.solve()

# Step 8: Extract Results
assignments_result = [(i, j) for i in customer_data['customer_id'] for j in agent_data['agent_id'] 
                      if pulp.value(assignments[(i, j)]) == 1]

result_df = pd.DataFrame(assignments_result, columns=['customer_id', 'agent_id'])
result_df.to_csv("optimized_field_collections.csv", index=False)

# Step 9: Visualization - Heatmap of Agent Assignments
pivot_table = result_df.pivot_table(index='customer_id', columns='agent_id', aggfunc='size', fill_value=0)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table, cmap='Blues', linewidths=0.5)
plt.title("Customer-Agent Assignment Heatmap")
plt.xlabel("Agent ID")
plt.ylabel("Customer ID")
plt.show()

print(f"Optimization Complete! Results saved to 'optimized_field_collections.csv'.")
