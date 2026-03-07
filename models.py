import strawberry
from typing import List, Optional
from database import driver

@strawberry.type
class MenuItem:
    id: strawberry.ID
    restaurantId: strawberry.ID
    name: str
    price: float
    category: str
    isAvailable: bool

@strawberry.type
class OrderItem:
    menuItemId: strawberry.ID
    quantity: int
    price: float

@strawberry.type
class Order:
    id: strawberry.ID
    customerId: strawberry.ID
    restaurantId: strawberry.ID
    totalAmount: float
    status: str
    orderedTime: str

@strawberry.type
class Customer:
    id: strawberry.ID
    name: str
    email: str
    phone: str
    address: str
    
    @strawberry.field
    async def orders(self) -> List[Order]:
        async with driver.session() as session:
            result = await session.run(
                "MATCH (c:Customer {id: $id})-[:PLACED]->(o:Order) RETURN o ORDER BY o.orderedTime DESC",
                id=self.id
            )
            data = await result.data()
            orders = [Order(
                id=record["o"]["id"],
                customerId=record["o"]["customerId"],
                restaurantId=record["o"]["restaurantId"],
                totalAmount=record["o"]["totalAmount"],
                status=record["o"]["status"],
                orderedTime=record["o"]["orderedTime"]
            ) for record in data]
            return orders

@strawberry.type
class Restaurant:
    id: strawberry.ID
    name: str
    cuisineType: str
    isOpen: bool
    
    @strawberry.field
    async def rating(self) -> float:
        async with driver.session() as session:
            result = await session.run("""
            MATCH (r:Restaurant {id: $id})
            OPTIONAL MATCH (:Customer)-[rev:REVIEWED]->(r)
            RETURN avg(rev.rating) as avg_rating, r.rating as default_rating
            """, id=self.id)
            record = await result.single()
            if record and record["avg_rating"] is not None:
                return round(record["avg_rating"], 2)
            elif record and record["default_rating"] is not None:
                return round(record["default_rating"], 2)
            return 0.0

@strawberry.input
class OrderItemInput:
    menuItemId: strawberry.ID
    quantity: int

@strawberry.input
class CreateOrderInput:
    customerId: strawberry.ID
    restaurantId: strawberry.ID
    items: List[OrderItemInput]

@strawberry.type
class CreateOrderPayload:
    order: Optional[Order]
    error: Optional[str]

@strawberry.type
class OrderStatusPayload:
    order: Optional[Order]
    error: Optional[str]
