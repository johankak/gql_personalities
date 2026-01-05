import aiohttp
import asyncio
import uuid
import json
import os

# ==================================================================================
# Client Setup & Helpers
# ==================================================================================

def createGQLClient():
    """
    Vytvoří instanci FastAPI TestClient s in-memory SQLite databází.
    
    Slouží pro izolované integrační testy bez nutnosti spouštět externí DB server.
    Provádí monkey-patching connection stringu v DBDefinitions.
    """
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import DBDefinitions

    # Lokální override pro připojení k in-memory SQLite (pro rychlé testy)
    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    # Monkey-patching: Přepíšeme funkci pro tvorbu connection stringu
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    # Vytvoření klienta bez zachytávání serverových výjimek (chceme vidět traceback)
    client = TestClient(main.app, raise_server_exceptions=False)
    return client


async def getToken(
    username, 
    password,
    keyurl = "http://localhost:33001/oauth/login3"
):
    """
    Získá JWT token z autentizační služby.
    
    Implementuje dvoukrokový proces přihlášení (fetch salt/key -> post credentials).
    Vrací raw token string nebo None v případě chyby.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # 1. Krok: Získání unikátního klíče/saltu pro přihlášení
            async with session.get(keyurl) as resp:
                if resp.status != 200:
                    print(f"Failed to fetch login page. Status: {resp.status}")
                    return None
                keyJson = await resp.json()

            # 2. Krok: Odeslání credentials s klíčem
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
    """
    Factory funkce vracející asynchronní `post` metodu pro GraphQL dotazy.
    
    Zajišťuje:
    - Lazy loading autentizačního tokenu (získá se až při prvním volání).
    - Automatické vkládání Authorization headeru (Cookies).
    - Základní error handling HTTP statusů.
    """
    token = None
    
    async def post(query, variables={}):
        nonlocal token
        # Lazy auth: Pokud nemáme token, získáme ho před prvním requestem
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
                # Pokud server vrátí chybu (5xx, 4xx), zabalíme ji do formátu GraphQL erroru
                if resp.status != 200:
                    text = await resp.text()
                    return {"errors": [{"message": f"Server Error {resp.status}", "detail": text, "extensions": {"code": resp.status}}]}
                else:
                    response = await resp.json()
                    return response
    return post 

# ==================================================================================
# Assertions & Utilities
# ==================================================================================

def is_json(responsejson):
    """Ověří, že odpověď je validní dictionary."""
    assert isinstance(responsejson, dict), f"Response is not a JSON object\nResponse: \n{responsejson}"
    return True

def has_no_errors(responsejson):
    """Ověří, že GQL odpověď neobsahuje klíč 'errors'."""
    if "errors" in responsejson:
        print(f"!!! GraphQL Errors found:\n{json.dumps(responsejson['errors'], indent=2)}")
    assert "errors" not in responsejson, f"Response contains errors"
    return True

def has_data_field(responsejson):
    """Ověří přítomnost klíče 'data'."""
    assert "data" in responsejson, "Response does not contain 'data' field"
    return True

def basic_assertions(responsejson):
    """Sdružuje základní kontroly formátu odpovědi."""
    is_json(responsejson)
    has_no_errors(responsejson)
    has_data_field(responsejson)
    return True

def has_field(responsejson, fieldname):
    """Ověří přítomnost konkrétního pole v 'data' objektu."""
    data = responsejson.get("data", {})
    assert fieldname in data, f"Response 'data' does not contain field '{fieldname}'"
    return True

# ==================================================================================
# Query Tests (Read-only operace)
# ==================================================================================

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

# ==================================================================================
# Mutation Tests (CUD operace)
# ==================================================================================

async def test_study_place_mutations(client):
    """
    Komplexní test životního cyklu entity StudyPlace (Insert -> Update -> Delete).
    Ověřuje správnost návratových typů (__typename) a práci s optimistickým zamykáním (lastchange).
    """
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
    
    # Validace, že jsme dostali správný GQL model a ne chybu
    if data_insert.get("__typename") != "StudyPlaceGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    # Uchováme lastchange pro optimistické zamykání při update
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
    
    # Očekáváme __typename nebo null (pokud je smazání úspěšné a server vrací null)
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
    data_delete = result_delete["data"]["StudyPlaceDelete"]
    
    # Úspěšný delete obvykle vrací None nebo objekt s informací o úspěchu
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: StudyPlace Mutations ---\n")

async def test_rank_mutations(client):
    """CRUD testy pro entitu Rank."""
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
    data_delete = result_delete["data"]["rankDelete"]
    
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: Rank Mutations ---\n")

async def work_history_position_mutations(client):
    """CRUD testy pro entitu WorkHistoryPosition."""
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
    data_delete = result_delete["data"]["WorkHistoryPositionDelete"]
    
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: WorkHistoryPosition Mutations ---\n")

async def user_study_place_mutations(client):
    """
    CRUD testy pro vazební tabulku UserStudyPlace.
    POZOR: Vyžaduje existující ID (Foreign Keys) v `systemdata.json`.
    """
    print("--- Test: UserStudyPlace Mutations (Insert, Update, Delete) ---")
    
    usp_user_id = "14702c35-b0c1-4902-8e3b-722a9615466b"
    
    # Načtení validních ID pro cizí klíče, aby test nespadl na FK constraint
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

    # Fallback pokud nejsou data, použijeme random (pravděpodobně failne v DB)
    if not available_studyplace_ids:
        print("Fallback: Using random StudyPlace ID (Expect Failure if ID doesn't exist in DB)")
        available_studyplace_ids.append(str(uuid.uuid4()))

    usp_studyplace_id = available_studyplace_ids[0]
    
    # --- INSERT ---
    print(f"Insert UserStudyPlace user_id={usp_user_id} studyplace_id={usp_studyplace_id}")
    
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
    # Pro update zkusíme změnit vazbu na jiné ID, pokud je k dispozici
    if len(available_studyplace_ids) > 1:
        new_studyplace_id = available_studyplace_ids[1]
    else:
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
    """CRUD testy pro vazební tabulku UserRank."""
    print("--- Test: UserRank Mutations (Insert, Update, Delete) ---")
    
    ur_user_id = "14702c35-b0c1-4902-8e3b-722a9615466b"
    available_rank_ids = []
    
    # Načtení dat ze systemdata.json pro validní FK
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

    if not available_rank_ids:
        print("Fallback: Using random Rank ID (Expect Failure if ID doesn't exist in DB)")
        available_rank_ids.append(str(uuid.uuid4()))

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
    if len(available_rank_ids) > 1:
        new_rank_id = available_rank_ids[1]
    else:
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

async def user_work_history_position_mutations(client):
    """
    CRUD testy pro UserWorkHistoryPosition.
    Testuje také specifické chybové návratové typy (InsertError, UpdateError).
    """
    print("--- Test: UserWorkHistoryPosition Mutations (Insert, Update, Delete) ---")
    
    uwhp_user_id = "14702c35-b0c1-4902-8e3b-722a9615466b"

    # Načítání FK IDs
    available_whp_ids = []
    try:
        if os.path.exists("systemdata.json"):
            with open("systemdata.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                whps = data.get("workhistorypositions", [])
                for w in whps:
                    if w.get("id"):
                        available_whp_ids.append(w.get("id"))

                if available_whp_ids:
                    print(f"Loaded {len(available_whp_ids)} WorkHistoryPosition IDs from systemdata.json")
                else:
                    print("Warning: 'workhistorypositions' found but no IDs loaded")
        else:
            print("Warning: systemdata.json not found")
    except Exception as e:
        print(f"Error loading systemdata.json: {e}")

    if not available_whp_ids:
        print("Fallback: Using random WorkHistoryPosition ID (Expect Failure if ID doesn't exist in DB)")
        available_whp_ids.append(str(uuid.uuid4()))

    current_whp_id = available_whp_ids[0]
    
    # --- INSERT ---
    print(f"Insert UserWorkHistoryPosition user_id={uwhp_user_id} workhistoryposition_id={current_whp_id}")
    
    # Fragmenty pro Union typy - ošetření úspěchu i erroru
    query_insert = """
    mutation userWorkhistorypositionInsert($userId: UUID!, $workhistorypositionId: UUID!) {
        userWorkhistorypositionInsert(userWorkhistoryposition: {userId: $userId, workhistorypositionId: $workhistorypositionId}) {
            __typename
            ... on UserWorkHistoryPositionGQLModel {
                id
                lastchange
                userId
                workhistorypositionId
            }
            ... on UserWorkHistoryPositionGQLModelInsertError {
                code
                location
                msg
            }
        }
    }
    """
    
    variables_insert = {"userId": uwhp_user_id, "workhistorypositionId": current_whp_id}
    result_insert = await client(query_insert, variables_insert)
    
    if "errors" in result_insert:
        print(f"Insert failed with errors: {result_insert['errors']}")
        return

    basic_assertions(result_insert)
    data_insert = result_insert["data"]["userWorkhistorypositionInsert"]
    
    # Kontrola, zda návratový typ není chyba (logická chyba aplikace, ne GraphQL chyba)
    if data_insert.get("__typename") == "UserWorkHistoryPositionGQLModelInsertError":
        print(f"Insert returned logic error: {data_insert}")
        return
    
    if data_insert.get("__typename") != "UserWorkHistoryPositionGQLModel":
        print(f"Insert returned unexpected type: {data_insert}")
        return

    print("Insert OK")
    uwhp_id = data_insert["id"]
    lastchange = data_insert["lastchange"]
    
    # --- UPDATE ---
    if len(available_whp_ids) > 1:
        new_whp_id = available_whp_ids[1]
    else:
        print("Warning: Only one WorkHistoryPosition ID available. Reusing it for Update test.")
        new_whp_id = available_whp_ids[0]

    print(f"Update UserWorkHistoryPosition id={uwhp_id} -> new workhistorypositionId={new_whp_id}")
    
    query_update = """
    mutation userWorkhistorypositionUpdate($id: UUID!, $lastchange: DateTime!, $workhistorypositionId: UUID!) {
        userWorkhistorypositionUpdate(userWorkhistoryposition: {id: $id, lastchange: $lastchange, workhistorypositionId: $workhistorypositionId}) {
            __typename
            ... on UserWorkHistoryPositionGQLModel {
                id
                lastchange
                workhistorypositionId
            }
            ... on UserWorkHistoryPositionGQLModelUpdateError {
                code
                location
                msg
            }
        }
    }
    """
    
    variables_update = {"id": uwhp_id, "lastchange": lastchange, "workhistorypositionId": new_whp_id}
    result_update = await client(query_update, variables_update)
    
    if "errors" in result_update:
        print(f"Update failed with errors: {result_update['errors']}")
        return

    basic_assertions(result_update)
    data_update = result_update["data"]["userWorkhistorypositionUpdate"]
    
    if data_update.get("__typename") == "UserWorkHistoryPositionGQLModelUpdateError":
        print(f"Update returned logic error: {data_update}")
        return

    if data_update.get("__typename") != "UserWorkHistoryPositionGQLModel":
        print(f"Update returned unexpected type: {data_update}")
        return

    print("Update OK")
    lastchange_updated = data_update["lastchange"]

    # --- DELETE ---
    print(f"Delete UserWorkHistoryPosition id={uwhp_id}")
    
    query_delete = """
    mutation userWorkhistorypositionDelete($id: UUID!, $lastchange: DateTime!) {
        userWorkhistorypositionDelete(userWorkhistoryposition: {id: $id, lastchange: $lastchange}) {
            __typename
            ... on UserWorkHistoryPositionGQLModelDeleteError {
                code
                location
                msg
            }
        }
    }
    """
    
    variables_delete = {"id": uwhp_id, "lastchange": lastchange_updated}
    result_delete = await client(query_delete, variables_delete)
    
    if "errors" in result_delete:
        print(f"Delete failed with errors: {result_delete['errors']}")
        return

    basic_assertions(result_delete)
    data_delete = result_delete["data"]["userWorkhistorypositionDelete"]
    
    if data_delete is None:
        print("Delete OK (returned null)")
    elif isinstance(data_delete, dict):
        if data_delete.get("__typename") == "UserWorkHistoryPositionGQLModelDeleteError":
             print(f"Delete failed with logic error: {data_delete}")
        elif data_delete.get("failed"):
            print(f"Delete failed: {data_delete}")
        else:
            print(f"Delete OK (returned object: {data_delete.get('__typename')})")
    else:
        print(f"Delete returned unexpected value: {data_delete}")
             
    print("--- Finished: UserWorkHistoryPosition Mutations ---\n")

# ==================================================================================
# Main Loop
# ==================================================================================

async def main():
    # Inicializace klienta (výchozí user john.newbie)
    client = createFederationClient()
    
    # 1. Čtení (Queries)
    await test_study_place_page(client)
    await test_user_study_place_page(client)
    await test_rank_page(client)
    await test_user_rank_page(client)
    await test_user_work_history_position_page(client)
    await test_work_history_position_page(client)
    
    # 2. Zápisy (Mutations)
    await test_study_place_mutations(client)
    await test_rank_mutations(client)
    await work_history_position_mutations(client)

    # 3. Zápisy pro vazební entity
    await user_study_place_mutations(client)
    await user_rank_mutations(client)
    await user_work_history_position_mutations(client)

if __name__ == "__main__":
    asyncio.run(main())