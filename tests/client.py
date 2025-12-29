import aiohttp
import asyncio
import uuid
import json

def createGQLClient():
    """
    Vytvoří lokálního klienta s in-memory databází pro testování bez běžícího serveru.
    Vyžaduje dostupnost main.py a DBDefinitions.
    """
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
    # print(f"--- Getting Token for {username} ---")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(keyurl) as resp:
                if resp.status != 200:
                    print(f"Failed to fetch login page. Status: {resp.status}")
                    return None
                keyJson = await resp.json()

            payload = {"key": keyJson["key"], "username": username, "password": password}
            async with session.post(keyurl, json=payload) as resp:
                if resp.status != 200:
                    print(f"Login failed. Status: {resp.status}")
                    text = await resp.text()
                    print(text)
                    return None
                tokenJson = await resp.json()
        
        token = tokenJson.get("token", None)
        return token
    except Exception as e:
        print(f"Exception during getToken: {e}")
        return None
            

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
            if token is None:
                print("!!! WARNING: No authentication token obtained. Request usually fails without it. !!!")

        payload = {"query": query, "variables": variables}
        
        cookies = {}
        if token:
            cookies['authorization'] = token

        async with aiohttp.ClientSession() as session:
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    return {"errors": [{"message": f"Server Error {resp.status}", "detail": text, "extensions": {"code": resp.status}}]}
                else:
                    response = await resp.json()
                    return response
    return post 

def is_json(responsejson):
    assert isinstance(responsejson, dict), f"Response is not a JSON object\nResponse: \n{responsejson}"
    return True

def has_no_errors(responsejson):
    if "errors" in responsejson:
        print(f"!!! GraphQL Errors found:\n{json.dumps(responsejson['errors'], indent=2)}")
    assert "errors" not in responsejson, f"Response contains errors"
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
    print("--- Test: StudyPlacePage ---")
    query = """query StudyPlacePage {
      StudyPlacePage(limit: 10) {
        id
        name
        lastchange
      }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "StudyPlacePage")
    print("--- OK: StudyPlacePage ---\n")
    return result

async def test_user_study_place_page(client):
    print("--- Test: userStudyPlacePage ---")
    query = """query userStudyPlacePage {
        userStudyplacePage {
            id
            lastchange
            userId
            studyplaceId
        }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "userStudyplacePage")
    print("--- OK: userStudyPlacePage ---\n")
    return result

async def test_rank_page(client):
    print("--- Test: rankPage ---")
    query = """query rankPage {
      rankPage(limit: 10) {
        id
        name
      }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "rankPage")
    print("--- OK: rankPage ---\n")
    return result

async def test_user_rank_page(client):
    print("--- Test: userRankPage ---")
    query = """query userRankPage {
      userRankPage {
        id
        rank { id name }
        user { id }
      }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "userRankPage")
    print("--- OK: userRankPage ---\n")
    return result

async def test_user_work_history_position_page(client):
    print("--- Test: userWorkHistoryPositionPage ---")
    query = """query userWorkHistoryPositionPage {
      userWorkhistorypositionPage {
        id
        userId
      }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "userWorkhistorypositionPage")
    print("--- OK: userWorkHistoryPositionPage ---\n")
    return result

async def test_work_history_position_page(client):
    print("--- Test: WorkHistoryPositionPage ---")
    query = """query WorkHistoryPositionPage {
      WorkHistoryPositionPage(limit: 10) {
        id
        name
      }
    }"""
    result = await client(query, {})
    basic_assertions(result)
    has_field(result, "WorkHistoryPositionPage")
    print("--- OK: WorkHistoryPositionPage ---\n")
    return result

async def test_study_place_mutations(client):
    """Testy pro StudyPlace Insert, Update, Delete."""
    print("--- Test: StudyPlace Mutations (Insert, Update, Delete) ---")
    
    sp_id = str(uuid.uuid4())
    sp_name = "New StudyPlace Test"
    
    # --- INSERT ---
    print(f"Insert StudyPlace id={sp_id}")
    query_insert = """
    mutation StudyPlaceInsert($id: UUID!, $name: String!) {
        StudyPlaceInsert(StudyPlace: {id: $id, name: $name}) {
            __typename
            ... on StudyPlaceGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_insert = {"id": sp_id, "name": sp_name}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print("Insert failed with errors.")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["StudyPlaceInsert"]
    
    if data_insert.get("__typename") != "StudyPlaceGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    sp_name_updated = "Updated StudyPlace Test"
    print(f"Update StudyPlace id={sp_id}")
    
    query_update = """
    mutation StudyPlaceUpdate($id: UUID!, $lastchange: DateTime!, $name: String!) {
        StudyPlaceUpdate(StudyPlace: {id: $id, lastchange: $lastchange, name: $name}) {
            __typename
            ... on StudyPlaceGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_update = {"id": sp_id, "lastchange": lastchange, "name": sp_name_updated}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print("Update failed with errors.")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["StudyPlaceUpdate"]
    
    if data_update.get("__typename") != "StudyPlaceGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete StudyPlace id={sp_id}")
    
    # Dotaz se ptá na __typename, ale je připraven, že odpověď bude null.
    # Použijeme inline fragmenty, kdyby se náhodou vrátil chybový objekt,
    # ale hlavní je kontrola 'None' v Pythonu.
    query_delete = """
    mutation StudyPlaceDelete($id: UUID!, $lastchange: DateTime!) {
        StudyPlaceDelete(StudyPlace: {id: $id, lastchange: $lastchange}) {
            __typename
        }
    }
    """
    
    variables_delete = {"id": sp_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    
    # Zde je klíčová úprava:
    data_delete = result_delete["data"]["StudyPlaceDelete"]
    
    if data_delete is None:
        # Server vrátil null, což podle vaší odpovědi znamená úspěch.
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        # Pokud vrátí objekt (např. chybu nebo model)
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            # Pokud by to vrátilo model (StudyPlaceGQLModel)
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: StudyPlace Mutations ---\n")

async def test_rank_mutations(client):
    """Testy pro Rank Insert, Update, Delete."""
    print("--- Test: Rank Mutations (Insert, Update, Delete) ---")
    
    rank_id = str(uuid.uuid4())
    rank_name = "New Rank Test"
    # --- INSERT ---
    print(f"Insert Rank id={rank_id}")
    query_insert = """
    mutation rankInsert($id: UUID!, $name: String!) {
        rankInsert(rank: {id: $id, name: $name}) {
            __typename
            ... on RankGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_insert = {"id": rank_id, "name": rank_name}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print("Insert failed with errors.")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["rankInsert"]
    
    if data_insert.get("__typename") != "RankGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    rank_name_updated = "Updated Rank Test"
    print(f"Update Rank id={rank_id}")

    query_update = """
    mutation rankUpdate($id: UUID!, $lastchange: DateTime!, $name: String!) {
        rankUpdate(rank: {id: $id, lastchange: $lastchange, name: $name}) {
            __typename
            ... on RankGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_update = {"id": rank_id, "lastchange": lastchange, "name": rank_name_updated}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print("Update failed with errors.")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["rankUpdate"]
    
    if data_update.get("__typename") != "RankGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete Rank id={rank_id}")
    
    # Dotaz se ptá na __typename, ale je připraven, že odpověď bude null.
    # Použijeme inline fragmenty, kdyby se náhodou vrátil chybový objekt,
    # ale hlavní je kontrola 'None' v Pythonu.
    query_delete = """
    mutation rankDelete($id: UUID!, $lastchange: DateTime!) {
        rankDelete(rank: {id: $id, lastchange: $lastchange}) {
            __typename
        }
    }
    """
    
    variables_delete = {"id": rank_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    
    # Zde je klíčová úprava:
    data_delete = result_delete["data"]["rankDelete"]
    
    if data_delete is None:
        # Server vrátil null, což podle vaší odpovědi znamená úspěch.
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        # Pokud vrátí objekt (např. chybu nebo model)
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            # Pokud by to vrátilo model (StudyPlaceGQLModel)
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: Rank Mutations ---\n")

async def work_history_position_mutations(client):
    """Testy pro WorkHistoryPosition Insert, Update, Delete."""
    print("--- Test: WorkHistoryPosition Mutations (Insert, Update, Delete) ---")
    
    wph_id = str(uuid.uuid4())
    wph_name = "New WorkHistoryPosition Test"
    # --- INSERT ---
    print(f"Insert id={wph_id}")
    query_insert = """
    mutation WorkHistoryPositionInsert($id: UUID!, $name: String!) {
        WorkHistoryPositionInsert(WorkHistoryPosition: {id: $id, name: $name}) {
            __typename
            ... on WorkHistoryPositionGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_insert = {"id": wph_id, "name": wph_name}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print("Insert failed with errors.")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["WorkHistoryPositionInsert"]
    
    if data_insert.get("__typename") != "WorkHistoryPositionGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    wph_name_updated = "Updated WorkHistoryPosition Test"
    print(f"Update WorkHistoryPosition id={wph_id}")
    
    query_update = """
    mutation WorkHistoryPositionUpdate($id: UUID!, $lastchange: DateTime!, $name: String!) {
        WorkHistoryPositionUpdate(WorkHistoryPosition: {id: $id, lastchange: $lastchange, name: $name}) {
            __typename
            ... on WorkHistoryPositionGQLModel {
                id
                name
                lastchange
            }
        }
    }
    """
    
    variables_update = {"id": wph_id, "lastchange": lastchange, "name": wph_name_updated}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print("Update failed with errors.")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["WorkHistoryPositionUpdate"]
    
    if data_update.get("__typename") != "WorkHistoryPositionGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete WorkHistoryPosition id={wph_id}")
    
    # Dotaz se ptá na __typename, ale je připraven, že odpověď bude null.
    # Použijeme inline fragmenty, kdyby se náhodou vrátil chybový objekt,
    # ale hlavní je kontrola 'None' v Pythonu.
    query_delete = """
    mutation WorkHistoryPositionDelete($id: UUID!, $lastchange: DateTime!) {
        WorkHistoryPositionDelete(WorkHistoryPosition: {id: $id, lastchange: $lastchange}) {
            __typename
        }
    }
    """
    
    variables_delete = {"id": wph_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    
    # Zde je klíčová úprava:
    data_delete = result_delete["data"]["WorkHistoryPositionDelete"]
    
    if data_delete is None:
        # Server vrátil null, což podle vaší odpovědi znamená úspěch.
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        # Pokud vrátí objekt (např. chybu nebo model)
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            # Pokud by to vrátilo model (StudyPlaceGQLModel)
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: WorkHistoryPosition Mutations ---\n")


# --- Main Execution ---

async def main():
    client = createFederationClient()
    
    #await test_study_place_page(client)
    #await test_user_study_place_page(client)
    #await test_rank_page(client)
    #await test_user_rank_page(client)
    #await test_work_history_position_page(client)
    #await test_user_work_history_position_page(client)
    
    #await test_study_place_mutations(client)

    #await test_rank_mutations(client)
    await work_history_position_mutations(client)

if __name__ == "__main__":
    asyncio.run(main())