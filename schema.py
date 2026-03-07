import strawberry
from typing import List, Optional
from database import driver
from models import Restaurant, Customer
from mutations import Mutation

@strawberry.type
class Query:
    @strawberry.field
    async def open_restaurants(self) -> List[Restaurant]:
        async with driver.session() as session:
            result = await session.run("MATCH (r:Restaurant {isOpen: true}) RETURN r")
            data = await result.data()
            return [Restaurant(
                id=record["r"]["id"],
                name=record["r"]["name"],
                cuisineType=record["r"]["cuisineType"],
                isOpen=record["r"]["isOpen"]
            ) for record in data]

    @strawberry.field
    async def customer(self, id: strawberry.ID) -> Optional[Customer]:
        async with driver.session() as session:
            result = await session.run("MATCH (c:Customer {id: $id}) RETURN c", id=str(id))
            record = await result.single()
            if not record:
                return None
            node = record["c"]
            return Customer(
                id=node["id"],
                name=node["name"],
                email=node["email"],
                phone=node["phone"],
                address=node["address"]
            )

schema = strawberry.Schema(query=Query, mutation=Mutation)
