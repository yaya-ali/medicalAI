import json
import os

from datetime import datetime
from pymongo import MongoClient
from core.config import settings


class Cursor:
    try:
        connection: MongoClient = MongoClient(
            f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASS}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/?authMechanism=DEFAULT"
        )
        cursor = connection[settings.FHIR_DB]
    except Exception as e:
        raise e


class SyntheaParser(Cursor):
    def __init__(self, data: dict, patientId: str):
        self.data = data
        self.patientId = patientId

    def parser(self, collection: str):
        result = []
        for entry in self.data["entry"]:
            if entry["resource"]["resourceType"] == collection:
                result.append(entry)

        template = {
            "_id": f"{self.patientId}",
            "entry": result,
            "link": [
                {
                    "relation": "self",
                    "url": f"https://{settings.MONGO_HOST}:9300/apis/default/fhir/{collection}",
                }
            ],
            "meta": {"lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            "resourceType": "Bundle",
            "total": len(result),
            "type": "collection",
        }

        self.cursor[collection].update_one(
            {"_id": self.patientId},
            {"$set": template},
            upsert=True,
        )

        return template

    def drop_all(self, collections):
        for collection in collections:
            self.cursor[collection].drop()


collections = [
    "Condition",
    "DiagnosticReport",
    "DocumentReference",
    "Encounter",
    "Immunization",
    "Observation",
    "Procedure",
    "Patient",
    "MedicationRequest",
]


def init():
    # get all .json files in current dir
    file = [f for f in os.listdir() if f.endswith(".json")]

    assert file, "No .json files found in current directory"

    for f in file:
        patientId = f.split("_")[-1].split(".")[0]
        with open(f, "r") as Iof:
            data = json.load(Iof)
            for c in collections:
                # create folder with patientId
                if not os.path.exists(patientId):
                    os.makedirs(patientId)
                with open(f"{patientId}/{patientId}_{c}.json", "w") as w:
                    w.write(
                        json.dumps(
                            SyntheaParser(data=data, patientId=patientId).parser(c)
                        )
                    )


def drop_all():
    SyntheaParser({}, "").drop_all(collections)
