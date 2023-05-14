from neo4j import GraphDatabase
import pandas as pd
from dotenv import load_dotenv
import os
import secrets
import string
# For Neo4j Connection
load_dotenv("my.env")
password = os.getenv("NEO_PASS")


def get_databaseProperties_list():
    q_lineage = "MATCH (n:Lineage) RETURN DISTINCT n.lineage"
    q_protein = "MATCH (n:Protein) RETURN DISTINCT n.protein"
    q_location = "MATCH (n:Location) RETURN DISTINCT n.location"
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        results_location = session.run(q_location)
        location_list = [record['n.location'] for record in results_location]
        results_protein = session.run(q_protein)
        protein_list = [record['n.protein'] for record in results_protein]
        results_lineage = session.run(q_lineage)
        record_lineage_lt = [record['n.lineage'].split(
            '.')[0] for record in results_lineage]
        lineage_list = list(set(record_lineage_lt))

    location_lt = [item for item in location_list if item is not None]
    protein_lt = [item for item in protein_list if item is not None]
    lineage_lt = [item for item in lineage_list if item is not None]
    return location_lt, protein_lt, lineage_lt
# -----------Neo4j query function------------------------------


def queryToDataframe(query, col_name_lt):
    # Execute the Cypher query
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        # session = driver.session()
        results = session.run(query)
    # Transform the results to a DataFrame
        df = pd.DataFrame(results, columns=col_name_lt)
    return df


def getNucleoIdFromSamplesFilter(df):
    accession_lt = []
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    rows_as_dicts = df.to_dict(orient='records')
    for row in rows_as_dicts:
        lineage = row['lineage']
        theDate = row['earliest_date']
        location = row['most_common_country']
        query = """
            MATCH (n:Nucleotide)-[:COLLECTED_IN]->(l:Location)<-[:IN_MOST_COMMON_COUNTRY]-(m:Lineage)
            WHERE l.location = $location AND m.lineage = $lineage AND n.collection_date >= datetime($theDate)
            RETURN n.accession
            ORDER BY n.collection_date
            LIMIT 1
        """
        params = {"location": location, "lineage": lineage, "theDate": theDate}
        with driver.session() as session:
            # session = driver.session()
            results = session.run(query, params)
            record = results.single()
            # print(record)
            if record:
                accession = record["n.accession"]
                accession_lt.append(accession)
    return accession_lt


def getProteinIdFromSamplesFilter(df, protein_name):
    accession_lt = []
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    rows_as_dicts = df.to_dict(orient='records')
    for row in rows_as_dicts:
        lineage = row['lineage']
        theDate = row['earliest_date']
        location = row['most_common_country']
        query = """
            MATCH (n:Protein)-[:COLLECTED_IN]->(l:Location)<-[:IN_MOST_COMMON_COUNTRY]-(m:Lineage)
            WHERE l.location = $location AND m.lineage = $lineage AND n.protein = $protein_name AND n.collection_date >= datetime($theDate)
            RETURN n.accession
            ORDER BY n.collection_date
            LIMIT 1
        """
        params = {"location": location, "lineage": lineage,
                  "protein_name": protein_name, "theDate": theDate}
        with driver.session() as session:
            # session = driver.session()
            results = session.run(query, params)
            record = results.single()
            # print(record)
            if record:
                accession = record["n.accession"]
                accession_lt.append(accession)
    return accession_lt

# ---------Create Input Node and relations based on users sample filter------------------------------------------
# Function to generate a unique random name


def generate_short_id(length=8):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(secrets.choice(characters) for _ in range(length))
    return short_id


def generate_unique_name():
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        random_name = generate_short_id()

        result = session.run(
            "MATCH (u:User {name: $name}) RETURN COUNT(u)", name=random_name)
        count = result.single()[0]

        while count > 0:
            random_name = generate_short_id()
            result = session.run(
                "MATCH (u:User {name: $name}) RETURN COUNT(u)", name=random_name)
            count = result.single()[0]

        return random_name


def addInputNeo(nodesLabel, inputNode_name, id_list):
    # Execute the Cypher query
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))

    # Create a new node for the user
    with driver.session() as session:
        session.run(
            "CREATE (userInput:Input {name: $name})", name=inputNode_name)

    # Perform MATCH query to retrieve nodes
    with driver.session() as session:
        result = session.run(
            "MATCH (n:" + nodesLabel + ") WHERE n.accession IN $id_lt RETURN n",
            nodesLabel=nodesLabel,
            id_lt=id_list)

        # Create relationship with properties for each matched node
        with driver.session() as session:
            for record in result:
                other_node = record["n"]
                session.run("MATCH (u:Input {name: $name}), (n:" + nodesLabel + " {accession: $id}) "
                            "CREATE (n)-[r:IN_INPUT]->(u)",
                            name=inputNode_name, nodesLabel=nodesLabel, id=other_node["accession"])
    print("An Input Node is Added in Neo4j Database!")

# ----------------------------------------------------
