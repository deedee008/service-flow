# ServiceFlow

**Restaurant Seating & Server Workload Optimization**

ServiceFlow is a Python-based restaurant seating recommendation system designed to support efficient and balanced seating decisions.
The project addresses a common challenge in restaurant operations: assigning incoming parties to suitable tables while balancing server workload, table capacity, and sales distribution.
Instead of relying solely on table availability or server rotation, ServiceFlow uses a rule-based scoring algorithm to evaluate seating options and recommend a table-server combination.

**Project status:** In development. Core recommendation logic and initial seating workflow are implemented and tested.

## Why ServiceFlow?

Traditional restaurant seating workflows often rely on guest counts (covers), table availability, and server rotation to distribute incoming parties. While these metrics are useful, they don't always reflect a server's actual workload.

For example, a server managing 12 guests who are already eating may have fewer immediate responsibilities than another server handling 6 guests who have just been seated or are ready to order.

ServiceFlow takes a more dynamic approach by evaluating multiple factors:

-**Service stages:** Recognizes that different stages of dining require different levels of attention.

-**Party size:** Accounts for additional workload associated with larger groups.

-**Table capacity:** Helps avoid assigning small parties to unnecessarily large tables.

-**Server sales:** Uses current sales as a tie-breaker to support fairer distribution.

Instead of requiring hosts to manually evaluate these factors and determine the next seating assignment, ServiceFlow generates a recommendation using a consistent, rule-based scoring algorithm.

The goal is to **reduce manual decision-making, support server workloads, and improve host efficiency**, while keeping the final seating decision in the hands of restaurant staff.

## Key Features

### Workload-Aware Seating
- Calculates server workload based on active tables and their current service stages.
- Assigns different workload weights to dining stages, such as newly seated, ready to order, and eating.
- Accounts for party size when estimating workload during high-attention service stages.

### Smart Table Selection
- Filters tables based on party size and seating capacity.
- Excludes occupied tables, temporarily closed tables, and closed sections.
- Prioritize efficient table utilization by considering unused seats.

### Shift and Section Management
- Supports assigning servers to sections for each shift.
- Allows section assignments to change between shifts.
- Resets server workload-related data when starting a new shift.

### Automated Testing
- Uses pytest for unit and integration testing.
- Follows Test-Driven Development (TDD) practices.
- Covers core functionality, seating decisions, and edge cases.

## How It Works

ServiceFlow uses a rule-based scoring algorithm to evaluate seating options based on server workload and table capacity.

### 1. Calculate Server Workload

Each active table contributes to a server's workload based on its current service stage.

Different stages receive different weights depending on the level of attention they typically require.

For example:
- **Just Seated:** 5 points
- **Ready to Order:** 5 points
- **Waiting for Food:** 1 point
- **Eating:** 1 point
- **Closing:** 3 points

For larger parties, additional workload points are applied during high-attention stages.

The total workload score is calculated by summing the scores of all active table sessions assigned to a server.

### 2. Find Suitable Tables

The table selection module identifies tables that can accommodate the arriving party. 

It also supports filtering out:
- Occupied tables
- Temporarily closed tables
- Tables in closed sections

These additional availability filters are implemented in the table selection module but are not yet fully integrated into the main seating workflow.

### 3. Evaluate Seating Options

For each suitable table, ServiceFlow identifies the server assigned to its section and calculates a recommendation score:

`score = server_workload + unused_seats`

Where: 
- `server_workload` is the server's current workload score.
- `unused_seats` is the difference between table capacity and party size.

The table-server combination with the lowest score is preferred.

### 4. Apply Sales Tie-Breaker

If multiple seating options have the same score, the algorithm prioritizes the server with lower current sales.

This provides an additional way to support balanced sales distribution without overriding workload-based decisions.

### 5. Return the Recommendation

The algorithm returns the selected table and server as a recommendation.

If no eligible table-server combination is found, it returns `None` rather than forcing an assignment.

### Current Development Status

The workload calculation, table selection logic, scoring algorithm, sales tie-breaker, and initial seating recommendation workflow are implemented and tested.

Integration of all table availability constraints into the main workflow is still in progress. A user interface for the restaurant hosts is planned for a future development stage.

## Tech Stack

- **Language:** Python 3
- **Testing:** pytest
- **Architecture:** Modular, object-oriented design using Python dataclasses and type hints
- **Version Control:** Git & GitHub
- **Development Environment:** PyCharm


