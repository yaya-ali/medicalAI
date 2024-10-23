import warnings
from httpcore import ConnectError
from medpub.doaj.core.doaj_core import DOAJCore
from medpub.doaj.utils.doaj_article_parser import DOAJUtils


class TestDOAJ:
    async def test_init_db(self):
        try:
            result = await DOAJCore().init_db()
        except ConnectError:
            warnings.warn(UserWarning("Connection Error:: rate limit exceeded"))

        assert result["status"] == "success"

    async def test_parse(self):
        dummy = {
            "total": 1,
            "page": 1,
            "pageSize": 20,
            "timestamp": "2024-03-15T08:17:35.250083Z",
            "query": "00007b4ea5c54ed18f451c98133aeef9",
            "results": [
                {
                    "last_updated": "2022-12-21T17:34:13Z",
                    "bibjson": {
                        "identifier": [{"id": "0036-3634", "type": "pissn"}],
                        "journal": {
                            "volume": "53",
                            "number": "5",
                            "country": "MX",
                            "issns": ["0036-3634"],
                            "publisher": "Instituto Nacional de Salud Pública",
                            "language": ["EN", "ES"],
                            "title": "Salud Pública de México",
                        },
                        "month": "10",
                        "end_page": "419",
                        "keywords": [
                            "neoplasias de la mama",
                            "genética",
                            "BRCA1",
                            "BRCA2",
                            "oncogenes",
                            "México",
                            "breast neoplasms",
                            "genetics",
                            "BRCA1",
                            "BRCA2",
                            "oncogenes",
                            "Mexico",
                        ],
                        "year": "2011",
                        "start_page": "415",
                        "subject": [
                            {
                                "code": "RA1-1270",
                                "scheme": "LCC",
                                "term": "Public aspects of medicine",
                            }
                        ],
                        "author": [{"name": "Elad Ziv"}],
                        "link": [
                            {
                                "type": "fulltext",
                                "url": "http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0036-36342011000500009",
                            }
                        ],
                        "abstract": "Breast cancer research has yielded several important results including the strong susceptibility genes,BRCA1 and BRCA2 and more recently 19 genes and genetic loci that confer a more moderate risk.The pace of discovery is accelerating as genetic technology and computational methods improve. These discoveries will change the way that breast cancer risk is understood in Mexico over the next few decades.<br>La investigación en cáncer de mama ha dado varios resultados importantes incluyendo los genes fuertemente susceptibles, BRCA1 y BRCA2, y más recientemente 19 genes y loci genéticos que confieren un riesgo moderado. El ritmo de los descubrimientos se acelera conforme mejora la tecnología y métodos computacionales.Estosdescubrimientoscambiarán la forma en que la investigación del cáncer es comprendida en México en las próximas décadas.",
                        "title": "Genetics of breast cancer: Applications to the Mexican population",
                    },
                    "created_date": "2013-09-04T07:00:14Z",
                    "id": "00007b4ea5c54ed18f451c98133aeef9",
                }
            ],
            "last": "https://doaj.org/api/v3/search/articles/00007b4ea5c54ed18f451c98133aeef9?page=1&pageSize=20",
        }
        result = DOAJUtils().parse_article(data=dummy)
        assert isinstance(result, list) and len(result) >= 1, "not instance of list"
        assert "doi" in result[0]["metadata"], "doi cant be empty"
        assert "title" in result[0]["metadata"], "title cant be emtpy"
        assert "fulltext_url" in result[0]["metadata"], "fulltext_url cant be emtpy"
