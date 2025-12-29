import aiohttp
import asyncio
import uuid
import json
import os

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

async def user_study_place_mutations(client):
    """Testy pro UserStudyPlace Insert, Update, Delete."""
    print("--- Test: UserStudyPlace Mutations (Insert, Update, Delete) ---")
    
    # Fixní User ID dle zadání
    usp_user_id = "14702c35-b0c1-4902-8e3b-722a9615466b"
    
    # Načtení všech dostupných StudyPlace ID ze souboru systemdata.json
    available_studyplace_ids = []
    try:
        if os.path.exists("systemdata.json"):
            with open("systemdata.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                studyplaces = data.get("studyplaces", [])
                for sp in studyplaces:
                    if sp.get("id"):
                        available_studyplace_ids.append(sp.get("id"))
                
                if available_studyplace_ids:
                    print(f"Loaded {len(available_studyplace_ids)} StudyPlace IDs from systemdata.json")
                else:
                    print("Warning: 'studyplaces' found but no IDs loaded")
        else:
            print("Warning: systemdata.json not found")
    except Exception as e:
        print(f"Error loading systemdata.json: {e}")

    # Fallback pokud se nepodařilo načíst žádná data
    if not available_studyplace_ids:
        print("Fallback: Using random StudyPlace ID (Expect Failure if ID doesn't exist in DB)")
        available_studyplace_ids.append(str(uuid.uuid4()))

    # ID pro insert (použijeme první dostupné)
    usp_studyplace_id = available_studyplace_ids[0]
    
    # --- INSERT ---
    print(f"Insert UserStudyPlace user_id={usp_user_id} studyplace_id={usp_studyplace_id}")
    
    # Dle moje_pomucka.txt a UserStudyPlaceGQLModel.py
    query_insert = """
    mutation UserStudyPlaceInsert($userId: UUID!, $studyplaceId: UUID!) {
        userStudyplaceInsert(userStudyplace: {userId: $userId, studyplaceId: $studyplaceId}) {
            __typename
            ... on UserStudyPlaceGQLModel {
                id
                lastchange
                userId
                studyplaceId
            }
        }
    }
    """
    
    variables_insert = {"userId": usp_user_id, "studyplaceId": usp_studyplace_id}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print(f"Insert failed with errors: {result_insert['errors']}")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["userStudyplaceInsert"]
    
    if data_insert.get("__typename") != "UserStudyPlaceGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    usp_id = data_insert["id"]
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    # Změníme studyplaceId. Musíme použít platné ID.
    # Pokud máme více ID, použijeme druhé. Pokud jen jedno, použijeme znovu to první.
    # Použití náhodného ID způsobí ForeignKeyViolationError.
    
    if len(available_studyplace_ids) > 1:
        new_studyplace_id = available_studyplace_ids[1]
    else:
        # Fallback: nemáme jiné validní ID, použijeme to samé, aby test prošel
        print("Warning: Only one StudyPlace ID available. Reusing it for Update test.")
        new_studyplace_id = available_studyplace_ids[0]

    print(f"Update UserStudyPlace id={usp_id} -> new studyplaceId={new_studyplace_id}")
    
    query_update = """
    mutation UserStudyPlaceUpdate($id: UUID!, $lastchange: DateTime!, $studyplaceId: UUID!) {
        userStudyplaceUpdate(userStudyplace: {id: $id, lastchange: $lastchange, studyplaceId: $studyplaceId}) {
            __typename
            ... on UserStudyPlaceGQLModel {
                id
                lastchange
                studyplaceId
            }
        }
    }
    """
    
    variables_update = {"id": usp_id, "lastchange": lastchange, "studyplaceId": new_studyplace_id}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print(f"Update failed with errors: {result_update['errors']}")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["userStudyplaceUpdate"]
    
    if data_update.get("__typename") != "UserStudyPlaceGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete UserStudyPlace id={usp_id}")
    
    query_delete = """
    mutation UserStudyPlaceDelete($id: UUID!, $lastchange: DateTime!) {
        userStudyplaceDelete(userStudyplace: {id: $id, lastchange: $lastchange}) {
            __typename
        }
    }
    """
    
    variables_delete = {"id": usp_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    
    data_delete = result_delete["data"]["userStudyplaceDelete"]
    
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: UserStudyPlace Mutations ---\n")

async def user_rank_mutations(client):
    """Testy pro UserRank Insert, Update, Delete."""
    print("--- Test: UserRank Mutations (Insert, Update, Delete) ---")
    
    # Fixní User ID dle zadání
    ur_user_id = "14702c35-b0c1-4902-8e3b-722a9615466b"
    # Načtení všech dostupných Rank ID ze souboru systemdata.json
    available_rank_ids = []
    try:
        if os.path.exists("systemdata.json"):
            with open("systemdata.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                ranks = data.get("ranks", [])
                for r in ranks:
                    if r.get("id"):
                        available_rank_ids.append(r.get("id"))

                if available_rank_ids:
                    print(f"Loaded {len(available_rank_ids)} Rank IDs from systemdata.json")
                else:
                    print("Warning: 'ranks' found but no IDs loaded")
        else:
            print("Warning: systemdata.json not found")
    except Exception as e:
        print(f"Error loading systemdata.json: {e}")

    # Fallback pokud se nepodařilo načíst žádná data
    if not available_rank_ids:
        print("Fallback: Using random Rank ID (Expect Failure if ID doesn't exist in DB)")
        available_rank_ids.append(str(uuid.uuid4()))

    # ID pro insert (použijeme první dostupné)
    user_rank_id = available_rank_ids[0]
    
    # --- INSERT ---
    print(f"Insert UserRank user_id={ur_user_id} rank_id={user_rank_id}")
    
    query_insert = """
    mutation UserRankInsert($userId: UUID!, $rankId: UUID!) {
        userRankInsert(userRank: {userId: $userId, rankId: $rankId}) {
            __typename
            ... on UserRankGQLModel {
                id
                lastchange
                userId
                rankId
            }
        }
    }
    """
    
    variables_insert = {"userId": ur_user_id, "rankId": user_rank_id}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print(f"Insert failed with errors: {result_insert['errors']}")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["userRankInsert"]
    
    if data_insert.get("__typename") != "UserRankGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    user_rank_id = data_insert["id"]
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    # Změníme studyplaceId. Musíme použít platné ID.
    # Pokud máme více ID, použijeme druhé. Pokud jen jedno, použijeme znovu to první.
    # Použití náhodného ID způsobí ForeignKeyViolationError.
    
    if len(available_rank_ids) > 1:
        new_rank_id = available_rank_ids[1]
    else:
        # Fallback: nemáme jiné validní ID, použijeme to samé, aby test prošel
        print("Warning: Only one Rank ID available. Reusing it for Update test.")
        new_rank_id = available_rank_ids[0]

    print(f"Update UserStudyPlace id={user_rank_id} -> new studyplaceId={new_rank_id}")
    
    query_update = """
    mutation UserRankUpdate($id: UUID!, $lastchange: DateTime!, $rankId: UUID!) {
        userRankUpdate(userRank: {id: $id, lastchange: $lastchange, rankId: $rankId}) {
            __typename
            ... on UserRankGQLModel {
                id
                lastchange
                rankId
            }
        }
    }
    """
    
    variables_update = {"id": user_rank_id, "lastchange": lastchange, "rankId": new_rank_id}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print(f"Update failed with errors: {result_update['errors']}")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["userRankUpdate"]
    
    if data_update.get("__typename") != "UserRankGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete UserStudyPlace id={user_rank_id}")
    
    query_delete = """
    mutation UserRankDelete($id: UUID!, $lastchange: DateTime!) {
        userRankDelete(userRank: {id: $id, lastchange: $lastchange}) {
            __typename
        }
    }
    """
    
    variables_delete = {"id": user_rank_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    
    data_delete = result_delete["data"]["userRankDelete"]
    
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: UserRank Mutations ---\n")


# --- Main Execution ---

async def main():
    client = createFederationClient()
    
    #await test_study_place_page(client)
    #await test_user_study_place_page(client)
    #await test_rank_page(client)
    #await test_user_rank_page(client)
    #await test_user_work_history_position_page(client)
    #await test_work_history_position_page(client)
    
    #await test_study_place_mutations(client)

    #await test_rank_mutations(client)
    #await work_history_position_mutations(client)

    #await user_study_place_mutations(client)
    await user_rank_mutations(client)

if __name__ == "__main__":
    asyncio.run(main())