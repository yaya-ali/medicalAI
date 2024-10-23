from typing import Any
from db.models.common import FilterRequest, PaginateRequest
from db.pipeline.utils.filter import DataFilter
from db.pipeline.utils.paginate import Pagination
from medpub.doaj.core.doaj_core import DOAJCore
from medpub.doaj.schema.req import DOAJArticleRequest


class DOAJArticlesPipeline(DOAJCore):
    """
    Pipeline for retrieving articles from the DOAJ database.

    This pipeline provides methods to retrieve articles based on various parameters such as diseases,
    filters, and pagination.

    Attributes:
        None

    Methods:
        article: Retrieves articles based on the provided request, filter, and pagination parameters.

    """

    def __init__(self) -> None:
        super().__init__()

    def article(
        self,
        req: DOAJArticleRequest,
        filter: FilterRequest,
        paginate: PaginateRequest,
    ) -> list[dict[str, Any]]:
        """
        Retrieves articles based on the provided request, filter, and pagination parameters.

        Args:
            req (DOAJArticleRequest): The request object containing the parameters for article retrieval.
            filter (FilterRequest): The filter object containing the filter parameters.
            paginate (PaginateRequest): The pagination object containing the pagination parameters.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the retrieved articles.

        Raises:
            None

        Examples:
            Example usage of the `article` method:

            ```
            req = DOAJArticleRequest(...)
            filter = FilterRequest(...)
            paginate = PaginateRequest(...)
            articles = await article(req, filter, paginate)
            print(articles)
            ```

        """

        final_result = []

        if isinstance(req.diseases, list):
            for d in req.diseases:
                query = [
                    {
                        "$match": {
                            "metadata.disease": {
                                "$regex": d,
                                "$options": "i",
                            }
                        }
                    },
                    {"$project": {"_id": 0}},
                ]

                if paginate.limit or paginate.skip:
                    query = Pagination().paginate(
                        query=query,
                        skip=paginate.skip,
                        limit=paginate.limit,
                    )

                result = [result for result in self.cursor["ARTICLES"].aggregate(query)]  # type: ignore[arg-type]

                if filter.fields and filter.conditions:
                    result = DataFilter().filter(
                        fields=filter.fields,
                        conditions=filter.conditions,
                        data=result,
                    )
                final_result.extend(result)
        else:
            query = [
                {"$project": {"_id": 0}},
            ]

            if paginate.limit or paginate.skip:
                query = Pagination().paginate(
                    query=query,
                    skip=paginate.skip,
                    limit=paginate.limit,
                )

            result = [result for result in self.cursor["ARTICLES"].aggregate(query)]

            if filter.fields and filter.conditions:
                result = DataFilter().filter(
                    fields=filter.fields,
                    conditions=filter.conditions,
                    data=result,
                )

            final_result.extend(result)

        return final_result
