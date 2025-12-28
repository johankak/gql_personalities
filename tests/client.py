import aiohttp
import asyncio

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
    async def post(query, variables={}):
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

# --- Test Functions ---

async def test_study_place_page(client):
    """Testy pro StudyPlacePage query."""
    print("--- Test: StudyPlacePage ---")
    
    query = """query StudyPlacePage {
      StudyPlacePage(limit: 100) {
        id
        name
        lastchange
      }
    }
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "StudyPlacePage")
    
    print("Result:", result)
    print("--- OK: StudyPlacePage ---\n")
    return result

async def test_user_study_place_page(client):
    """Testy pro userStudyPlacePage query."""
    print("--- Test: userStudyPlacePage ---")
    
    query = """query userStudyPlacePage {
        userStudyplacePage {
        id
        lastchange
        rbacobjectId
        userId
        studyplaceId
        }
    }
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "userStudyplacePage")
    
    print("Result:", result)
    print("--- OK: userStudyPlacePage ---\n")
    return result

async def test_rank_page(client):
    """Testy pro rankPage query."""
    print("--- Test: rankPage ---")
    
    query = """query rankPage {
      rankPage(limit: 100) {
        id
        name
        lastchange
      }
    }
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "rankPage")
    
    print("Result:", result)
    print("--- OK: rankPage ---\n")
    return result

async def test_user_rank_page(client):
    """Testy pro userRankPage query."""
    print("--- Test: userRankPage ---")
    
    query = """query userRankPage {
  userRankPage {
    id
    rbacobjectId
    lastchange
    rank {
      name
      id
    }
    user {
      id
    }
  }
}
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "userRankPage")
    
    print("Result:", result)
    print("--- OK: userRankPage ---\n")
    return result

async def test_user_work_history_position_page(client):
    """Testy pro userWorkHistoryPositionPage query."""
    print("--- Test: userWorkHistoryPositionPage ---")
    
    query = """query userWorkHistoryPositionPage {
  userWorkhistorypositionPage {
    id
    lastchange
    rbacobjectId
    userId
  }
}
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "userWorkhistorypositionPage")
    
    print("Result:", result)
    print("--- OK: userWorkHistoryPositionPage ---\n")
    return result

async def test_work_history_position_page(client):
    """Testy pro WorkHistoryPositionPage query."""
    print("--- Test: WorkHistoryPositionPage ---")
    
    query = """query WorkHistoryPositionPage {
      WorkHistoryPositionPage(limit: 100) {
        id
        name
        lastchange
      }
    }
    """
    
    # Provedeni dotazu
    result = await client(query, {})
    
    # Assertions
    basic_assertions(result)
    has_field(result, "WorkHistoryPositionPage")
    
    print("Result:", result)
    print("--- OK: WorkHistoryPositionPage ---\n")
    return result
# --- Main Execution ---

async def main():
    # Inicializace klienta
    client = createFederationClient()
    
    # Spousteni jednotlivych testu
    await test_study_place_page(client)
    await test_user_study_place_page(client)
    await test_rank_page(client)
    await test_user_rank_page(client)
    await test_work_history_position_page(client)
    await test_user_work_history_position_page(client)
    
    # Zde muzes pridat dalsi testy, napriklad:
    # await test_user_page(client)
    # await test_group_page(client)

if __name__ == "__main__":
    asyncio.run(main())