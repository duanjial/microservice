from downloader import Downloader


class DownloadService:
    def __init__(self):
        self.downloader = Downloader()

    def download_with_url(self, url):
        return self.downloader.download(url=url)
