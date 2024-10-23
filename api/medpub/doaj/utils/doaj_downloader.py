import os
from typing import Union, List
from scidownl import scihub_download


class DownloadDOI:
    """
    Class for downloading articles based on their DOIs.
    """

    def __init__(self):
        self.out_dir = os.getenv("DOAJ_ARTICLES_DIR") or "/tmp/doaj_articles"

    def download(self, dois: Union[str, List[str]]):
        """
        Download articles based on their DOIs.

        Args:
            dois (Union[str, List[str]]): The DOIs of the articles to download.
                It can be a single DOI as a string or a list of DOIs.

        Returns:
            None
        """
        if isinstance(dois, str):
            dois = [dois]

        for doi in dois:
            file_path = os.path.join(self.out_dir, f"{doi.replace('/', '_')}.pdf")
            if not os.path.exists(file_path):
                scihub_download(keyword=doi, out=file_path)  # default is doi
            return file_path
