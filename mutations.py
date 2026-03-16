import strawberry
import uuid
from datetime import datetime
from database import driver
from models import CreateOrderInput, CreateOrderPayload, OrderStatusPayload, Order

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_order(self, input: CreateOrderInput) -> CreateOrderPayload:
        async with driver.session() as session:
            menu_item_ids = [item.menuItemId for item in input.items]
            
            check_result = await session.run(
                "MATCH (m:MenuItem) WHERE m.id IN $ids RETURN m.id AS id, m.isAvailable AS isAvailable, m.price AS price, m.restaurantId AS restaurantId",
                ids=[str(i) for i in menu_item_ids]
            )
            data = await check_result.data()
            menu_items = {record["id"]: record for record in data}
                
            if len(menu_items) != len(menu_item_ids):
                return CreateOrderPayload(order=None, error="Some items do not exist.")
                
            total_amount = 0.0
            for item in input.items:
                str_item_id = str(item.menuItemId)
                mi = menu_items[str_item_id]
                if not mi["isAvailable"]:
                    return CreateOrderPayload(order=None, error=f"Item {str_item_id} is not available.")
                if str(mi["restaurantId"]) != str(input.restaurantId):
                    return CreateOrderPayload(order=None, error="Items must belong to the specified restaurant.")
                total_amount += mi["price"] * item.quantity

            order_id = str(uuid.uuid4())
            ordered_time = datetime.now().isoformat()
            status = "placed"

            query = """
            MATCH (c:Customer {id: $customerId})
            MATCH (r:Restaurant {id: $restaurantId})
            CREATE (o:Order {
                id: $orderId,
                customerId: $customerId,
                restaurantId: $restaurantId,
                totalAmount: $totalAmount,
                status: $status,
                orderedTime: $orderedTime
            })
            CREATE (c)-[:PLACED]->(o)
            CREATE (o)-[:AT_RESTAURANT]->(r)
            WITH o
            UNWIND $items AS item
            MATCH (m:MenuItem {id: item.menuItemId})
            CREATE (o)-[:CONTAINS {quantity: item.quantity, price: item.price}]->(m)
            RETURN o
            """
            
            items_for_query = [{"menuItemId": str(i.menuItemId), "quantity": i.quantity, "price": menu_items[str(i.menuItemId)]["price"]} for i in input.items]
            
            try:
                res = await session.run(
                    query,
                    customerId=str(input.customerId),
                    restaurantId=str(input.restaurantId),
                    orderId=order_id,
                    totalAmount=total_amount,
                    status=status,
                    orderedTime=ordered_time,
                    items=items_for_query
                )
                record = await res.single()
                if not record:
                    return CreateOrderPayload(order=None, error="Failed to create order. Check customer/restaurant existence.")
                
                node = record["o"]
                order = Order(
                    id=node["id"],
                    customerId=node["customerId"],
                    restaurantId=node["restaurantId"],
                    totalAmount=node["totalAmount"],
                    status=node["status"],
                    orderedTime=node["orderedTime"]
                )
                return CreateOrderPayload(order=order, error=None)
            except Exception as e:
                return CreateOrderPayload(order=None, error=str(e))

    @strawberry.mutation
    async def update_order_status(self, order_id: strawberry.ID, status: str) -> OrderStatusPayload:
        valid_statuses = ["placed", "preparing", "out_for_delivery", "delivered", "cancelled"]
        if status not in valid_statuses:
            return OrderStatusPayload(order=None, error="Invalid status.")
            
        async with driver.session() as session:
            result = await session.run("""
            MATCH (o:Order {id: $order_id})
            SET o.status = $status
            RETURN o
            """, order_id=str(order_id), status=status)
            record = await result.single()
            if not record:
                return OrderStatusPayload(order=None, error="Order not found.")
                
            node = record["o"]
            order = Order(
                id=node["id"],
                customerId=node["customerId"],
                restaurantId=node["restaurantId"],
                totalAmount=node["totalAmount"],
                status=node["status"],
                orderedTime=node["orderedTime"]
            )
            return OrderStatusPayload(order=order, error=None)
