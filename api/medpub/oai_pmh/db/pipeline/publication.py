from typing import Any
from db.pipeline.utils.filter import DataFilter
from db.pipeline.utils.paginate import Pagination
from medpub.oai_pmh.db.pipeline.publisher import PublisherPipeline
from medpub.oai_pmh.schema.req import (
    GetPublicationRequest,
    GetPublisherRequest,
)


class PublicationPipeline(PublisherPipeline):
    def __init__(self, **kwargs):
        self.collection = "MedicalPublication"
        self.req = kwargs.get(
            "req",
            GetPublicationRequest(
                fields=[],
                conditions=[],
            ),
        )

    @property
    def run(self):
        return self.get_publication(self.req)

    def get_publication(self, req: GetPublicationRequest) -> list[dict[str, Any]]:
        """
        Get publication by disease category

        Args:
            req (GetPublicationRequest): An instance of GetPublicationRequest class.
                - diseases (List[str], optional): A list of diseases. Defaults to None.

        returns:
            list: A list of publications
        """

        if req.diseases is None:
            query = [
                {"$unwind": "$OAI-PMH.ListRecords.record"},
                {
                    "$addFields": {
                        "metadata": {
                            "articleType": "$OAI-PMH.ListRecords.record.metadata.article.@article-type",
                            "header": "$OAI-PMH.ListRecords.record.header",
                            "journal": "$OAI-PMH.ListRecords.record.metadata.article.front.journal-meta",
                        },
                        "articleTitle": "$OAI-PMH.ListRecords.record.metadata.article.front.article-meta.title-group",
                        "publisher": "$OAI-PMH.ListRecords.record.metadata.article.front.journal-meta.publisher",
                        "doi": "$OAI-PMH.ListRecords.record.metadata.article.front.article-meta.article-id",
                    }
                },
                {
                    "$lookup": {
                        "from": "Publisher",
                        "localField": "_id",
                        "foreignField": "set_code",
                        "as": "publisherInfo",
                    }
                },
                {"$unwind": "$publisherInfo"},
                {
                    "$project": {
                        "articleMetadata": "$metadata",
                        "diseaseCategory": "$publisherInfo.disease_category",
                        "articleTitle": "$articleTitle",
                        "publisher": "$publisher",
                        "doi": "$doi",
                    }
                },
            ]

            if req.limit or req.skip:
                query = Pagination().paginate(
                    query=query,
                    skip=req.skip,
                    limit=req.limit,
                )

            result = [
                result
                for result in self.cursor[self.collection].aggregate(query)  # type: ignore[arg-type]
            ]

            if req.conditions and req.fields:
                result = DataFilter().filter(
                    fields=req.fields,
                    conditions=req.conditions,
                    data=result,
                )

            return result

        else:
            set_codes = []
            for disease in req.diseases:
                publishers = self.get_publisher(
                    GetPublisherRequest(
                        diseases=[disease],
                        fields=[],
                        conditions=[],
                    ),
                )
                for publisher in publishers:
                    set_codes.append(publisher["set_code"])  # type: ignore[call-overload]

            result = []
            for set_code in set_codes:
                query = [
                    {"$match": {"_id": set_code}},
                    {"$unwind": "$OAI-PMH.ListRecords.record"},
                    {
                        "$addFields": {
                            "metadata": {
                                "articleType": "$OAI-PMH.ListRecords.record.metadata.article.@article-type",
                                "header": "$OAI-PMH.ListRecords.record.header",
                                "journal": "$OAI-PMH.ListRecords.record.metadata.article.front.journal-meta",
                            },
                            "articleTitle": "$OAI-PMH.ListRecords.record.metadata.article.front.article-meta.title-group",
                            "publisher": "$OAI-PMH.ListRecords.record.metadata.article.front.journal-meta.publisher",
                            "doi": "$OAI-PMH.ListRecords.record.metadata.article.front.article-meta.article-id",
                        }
                    },
                    {
                        "$lookup": {
                            "from": "Publisher",
                            "localField": "_id",
                            "foreignField": "set_code",
                            "as": "publisherInfo",
                        }
                    },
                    {"$unwind": "$publisherInfo"},
                    {
                        "$project": {
                            "articleMetadata": "$metadata",
                            "diseaseCategory": "$publisherInfo.disease_category",
                            "articleTitle": "$articleTitle",
                            "publisher": "$publisher",
                            "doi": "$doi",
                        }
                    },
                ]
                result.append(
                    [result for result in self.cursor["Publication"].aggregate(query)]  # type: ignore[arg-type]
                )

            if req.conditions and req.fields:
                result = DataFilter().filter(
                    fields=req.fields,
                    conditions=req.conditions,
                    data=result,
                )
            return result
