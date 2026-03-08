# Online Food Delivery System - GraphQL API

A GraphQL API built with Python, Strawberry, and Neo4j to manage restaurants, customers, and food orders. This system supports complex relations and validations, such as preventing orders for unavailable items and auto-calculating total amounts.

## 🚀 Features

- **Store Management**: Track restaurants, their availability, cuisine types, and statuses.
- **Menu Hierarchy**: Each restaurant has multiple menu items with categories and availability status.
- **Order Lifecycle**: Complete order management with statuses: `placed`, `preparing`, `out_for_delivery`, `delivered`, `cancelled`.
- **Validation & Logic**:
  - Prevent ordering items that are not available.
  - Automatic calculation of order total amounts based on item prices and quantities.
  - Restaurant ratings calculated dynamically from customer reviews.
- **Customer History**: Easy access to a customer's order history and details.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **GraphQL Framework**: [Strawberry](https://strawberry.rocks/)
- **Database**: [Neo4j](https://neo4j.com/) (Graph Database)
- **Web Server**: [FastAPI](https://fastapi.tiangolo.com/) / [Uvicorn](https://www.uvicorn.org/)

## 📊 Database Models

- **Customer**: `id`, `name`, `email`, `phone`, `address`
- **Restaurant**: `id`, `name`, `cuisine_type`, `rating`, `is_open`
- **MenuItem**: `id`, `restaurant_id`, `name`, `price`, `category`, `is_available`
- **Order**: `id`, `customer_id`, `restaurant_id`, `total_amount`, `status`, `ordered_time`
- **OrderItem**: `id`, `order_id`, `menu_item_id`, `quantity`, `price`

## 🧪 Testing Queries & Mutations

### Get Open Restaurants
```graphql
query {
  openRestaurants {
    id
    name
    cuisineType
    rating
  }
}
```

### Get Customer Orders
```graphql
query {
  customer(id: "1") {
    name
    orders {
      id
      totalAmount
      status
    }
  }
}
```

### Place Order
```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    restaurantId: "2"
    items: [{ menuItemId: "1", quantity: 2 }]
  }) {
    order {
      id
      totalAmount
      status
    }
    error
  }
}
```

## 📋 Expected Test Cases

1. **Restaurants filtered by status**: Query only returns restaurants where `is_open` is true.
2. **Menu availability validation**: Mutation fails if a `MenuItem` is marked as unavailable.
3. **Order total calculation**: The `totalAmount` is automatically calculated as `sum(price * quantity)`.
4. **Order status updates**: Ability to transition orders through their lifecycle.
5. **Customer order history**: Efficiently retrieve all past orders for a specific customer.
6. **Restaurant rating calculation**: Dynamics calculation of average ratings from reviews.
## 📸 Screenshots

### 1. Neo4j Aura Instance
![Neo4j Aura Instance](/Users/swetapopatkadam/Desktop/cloud_ss/s1.png)

**Description:**
This screenshot shows the **Neo4j Aura database instance running**. The instance contains nodes and relationships for the Online Food Delivery System and is ready to execute graph queries.

---

### 2. Complete Graph View
**Query:**
```cypher
MATCH p=()-[]->() RETURN p LIMIT 25;
```
![Complete Graph View](image-link-placeholder)

**Description:**
This query displays the **complete graph structure**, showing all nodes (Customer, Restaurant, MenuItem, Order) and their relationships in the system.

---

### 3. Order and Restaurant Relationship
**Query:**
```cypher
MATCH p=()-[:AT_RESTAURANT]->() RETURN p LIMIT 25;
```
![Order and Restaurant Relationship](image-link-placeholder)

**Description:**
This query shows the **AT_RESTAURANT relationship**, which connects an **Order** to the **Restaurant** where the order was placed.

---

### 4. Order and Menu Item Relationship
**Query:**
```cypher
MATCH p=()-[:CONTAINS]->() RETURN p LIMIT 25;
```
![Order and Menu Item Relationship](image-link-placeholder)

**Description:**
This query displays the **CONTAINS relationship**, showing which **Menu Items are included in an Order**.

---

### 5. Restaurant and Menu Item Relationship
**Query:**
```cypher
MATCH p=()-[:HAS_MENU_ITEM]->() RETURN p LIMIT 25;
```
![Restaurant and Menu Item Relationship](image-link-placeholder)

**Description:**
This query shows the **HAS_MENU_ITEM relationship**, representing which **menu items belong to a restaurant**.

---

### 6. Customer Order Placement
**Query:**
```cypher
MATCH p=()-[:PLACED]->() RETURN p LIMIT 25;
```
![Customer Order Placement](image-link-placeholder)

**Description:**
This query shows the **PLACED relationship**, where a **Customer places an Order**.

---

### 7. Customer Review Relationship
**Query:**
```cypher
MATCH p=()-[:REVIEWED]->() RETURN p LIMIT 25;
```
![Customer Review Relationship](image-link-placeholder)

**Description:**
This query shows the **REVIEWED relationship**, where a **Customer gives a review to a Restaurant**, which helps calculate restaurant ratings.

---

## ⚙️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shweta-Tech-creator/-ONLINE-FOOD-DELIVERY-SYSTEM.git
   cd -ONLINE-FOOD-DELIVERY-SYSTEM
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file with your Neo4j credentials:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

4. **Run the API**:
   ```bash
   uvicorn main:app --reload
   ```
