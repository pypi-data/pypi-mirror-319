import asyncio
from llq import GraphQLClient, UpdateJobMutation
from llq.schema import PostStatusEnum, ID


async def run():
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2xlbGFicXVhbnRpcXVlLmNvbSIsImlhdCI6MTczNjEwMzMxOCwibmJmIjoxNzM2MTAzMzE4LCJleHAiOjE3MzY3MDgxMTgsImRhdGEiOnsidXNlciI6eyJpZCI6IjExIn19fQ.bzct6XLxyNmv_1eGhmi1OglRNvJQRiNW7ZRjc83wjWg"
    }
    client = GraphQLClient(endpoint_url="https://lelabquantique.com/graphql") 
    await client.connect()
    client.headers = headers
    update = UpdateJobMutation()
    response = await client.execute(update.get(job_id=5182, status=PostStatusEnum.TRASH, contract_kinds={}, occupation_kinds={}, job_modes={}))
    await client.close() 
    print(update.parse(response))
    print("HELLO")
   


if __name__ == "__main__":
    asyncio.run(run())
