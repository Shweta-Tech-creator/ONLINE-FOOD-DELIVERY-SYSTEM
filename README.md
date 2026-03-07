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
