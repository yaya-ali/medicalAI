from typing import Any


class DOAJUtils:
    def parse_article(self, data: Any) -> list | dict:
        """
        Parse article metadata

        Args:
            data (list[dict[str | Any]] | str | Any): JSON data as a list of dictionaries,
                a string, or any other type.

        Returns:
            list[dict[str | Any]] | list | dict[str | str]: Extracted useful information
            as a list of dictionaries, a list, or a dictionary.

        Raises:
            None

        Examples:
            >>> parser = ArticleParser()
            >>> data = [
            ...     {
            ...         "results": [
            ...             {
            ...                 "id": "123",
            ...                 "bibjson": {
            ...                     "title": "Sample Title",
            ...                     "abstract": "Sample Abstract",
            ...                     "journal": {
            ...                         "title": "Sample Journal",
            ...                         "publisher": "Sample Publisher"
            ...                     },
            ...                     "author": [
            ...                         {"name": "Author 1"},
            ...                         {"name": "Author 2"}
            ...                     ],
            ...                     "year": "2022",
            ...                     "identifier": [
            ...                         {"id": "doi:123"},
            ...                         {"id": "pmid:456"}
            ...                     ],
            ...                     "link": [
            ...                         {"url": "https://sampleurl.com"}
            ...                     ]
            ...                 }
            ...             }
            ...         ]
            ...     }
            ... ]
            >>> parser.parse_article(data)
            [
                {
                    "timestamp": None,
                    "metadata": {
                        "id": "123",
                        "title": "Sample Title",
                        "abstract": "Sample Abstract",
                        "journal_title": "Sample Journal",
                        "journal_publisher": "Sample Publisher",
                        "authors": ["Author 1", "Author 2"],
                        "publication_year": "2022",
                        "doi": "doi:123",
                        "fulltext_url": "https://sampleurl.com"
                    }
                }
            ]
        """
        try:
            article_metadata_list = []

            for result in data["results"]:
                doi = None
                for identifier in result.get("bibjson", {}).get("identifier", []):
                    if str(identifier.get("type")).lower() == "doi":
                        doi = identifier.get("id")
                        break

                fulltext_url = None
                for link in result.get("bibjson", {}).get("link", []):
                    if link.get("type") == "fulltext":
                        fulltext_url = link.get("url")
                        break

                article_metadata = {
                    "timestamp": data.get("timestamp"),
                    "metadata": {
                        "id": result.get("id"),
                        "title": result.get("bibjson", {}).get("title"),
                        "abstract": result.get("bibjson", {}).get("abstract"),
                        "journal_title": result.get("bibjson", {})
                        .get("journal", {})
                        .get("title"),
                        "journal_publisher": result.get("bibjson", {})
                        .get("journal", {})
                        .get("publisher"),
                        "authors": [
                            author.get("name")
                            for author in result.get("bibjson", {}).get("author", [])
                        ],
                        "publication_year": result.get("bibjson", {}).get("year"),
                        "doi": doi,
                        "fulltext_url": fulltext_url,
                    },
                }
                article_metadata_list.append(article_metadata)

        except Exception as e:
            return {
                "status": "error",
                "detail": f"DOAJUtils::Exception:: {repr(e)}",
            }

        return article_metadata_list
