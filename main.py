from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema
from database import driver

app = FastAPI(title="Online Food Delivery API")

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("shutdown")
async def shutdown_event():
    await driver.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the online food delivery system API. Path over to /graphql for the playground format."}
