from db.models.common import FilterRequest, PaginateRequest
from medpub.doaj.db.pipeline.articles import DOAJArticlesPipeline
from medpub.doaj.schema.req import DOAJArticleRequest


class Test_Articles:
    async def test_get_articles(self):
        article_req = DOAJArticleRequest(diseases=["Cancer"])
        paginate = PaginateRequest()
        filter = FilterRequest(conditions=[], fields=[])

        result = DOAJArticlesPipeline().article(
            req=article_req,
            filter=filter,
            paginate=paginate,
        )
        assert result is not None, "Result is None"
        assert len(result) > 0, "Result is empty"
