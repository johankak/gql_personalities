import aiohttp
def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    client = TestClient(main.app, raise_server_exceptions=False)
    return client


async def getToken(
    username, 
    password,
    keyurl = "http://localhost:33001/oauth/login3"
):
    
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            print(resp.status)
            keyJson = await resp.json()
            print(keyJson)

        payload = {"key": keyJson["key"], "username": username, "password": password}
        async with session.post(keyurl, json=payload) as resp:
            print(resp.status)
            tokenJson = await resp.json()
            print(tokenJson)
    return tokenJson.get("token", None)
            

def createFederationClient(
    username="john.newbie@world.com", 
    password="john.newbie@world.com",
    gqlurl="http://localhost:8000/gql"
):
    token = None
    async def post(query, variables):
        nonlocal token
        if token is None:
            token = await getToken(username, password)

        payload = {"query": query, "variables": variables}
        # headers = {"Authorization": f"Bearer {token}"}
        cookies = {'authorization': token}
        async with aiohttp.ClientSession() as session:
            # print(headers, cookies)
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                # print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return text
                else:
                    response = await resp.json()
                    return response
    return post 

def is_json(responsejson):
    assert isinstance(responsejson, dict), f"Response is not a JSON object\nResponse: \n{responsejson}"
    return True

def has_no_errors(responsejson):
    assert "errors" not in responsejson, f"Response contains errors: {responsejson['errors']}"
    return True

def has_data_field(responsejson):
    assert "data" in responsejson, "Response does not contain 'data' field"
    return True

def basic_assertions(responsejson):
    is_json(responsejson)
    has_no_errors(responsejson)
    has_data_field(responsejson)
    return True

def has_field(responsejson, fieldname):
    data = responsejson.get("data", {})
    assert fieldname in data, f"Response 'data' does not contain field '{fieldname}'"
    return True

async def main():
    client = createFederationClient()
    result = await client("""query StudyPlacePage {
  StudyPlacePage(limit: 100) {
    id
    name
    lastchange
  }
}
""", {})
    basic_assertions(result)
    has_field(result, "StudyPlacePage")
    print(result)

if __name__ == "__main__":
    
    import asyncio
    asyncio.run(main())
    