import asyncio
import aiohttp
import PyPDF2
import fitz
import trafilatura

from dataclasses import dataclass
from io import BytesIO
from tqdm import tqdm
from typing import List, Tuple

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import ssl
import certifi


@dataclass
class FastParserResult:
    url: str
    content: str


class YoutubeExtractor:

    @staticmethod
    def get_video_id(url):
        return url.split("?v=")[-1]

    @staticmethod
    def extract(urls: list):
        urls = [YoutubeExtractor.get_video_id(url) for url in urls]
        results = []
        formatter = TextFormatter()
        for url in urls:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(url)
                transcript = formatter.format_transcript(transcript)
                results.append(transcript)
            except:
                pass
        return results


class FastHTMLParserV3:

    async def _fetch_url(self, session, url, url_fetch_timeout=10):
        if self._is_avoid_urls(url):
            return ""
        try:
            async with session.get(url, timeout=url_fetch_timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._process_trafili_html(html)
                else:
                    # print(f"Error fetching {url}: HTTP status {response.status}")
                    return ""
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error for {url}: {str(e)}")
            return ""
        except asyncio.TimeoutError:
            print(f"Timeout error for {url}")
            return ""
        except Exception as e:
            print(f"Unexpected error fetching {url}: {str(e)}")
            return ""

    async def fetch_content(self, urls, url_fetch_timeout=10):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url, url_fetch_timeout) for url in urls]
            return await asyncio.gather(*tasks)
            # return [result for result in await asyncio.gather(*tasks) if result]

    def _is_avoid_urls(self, url):
        if "https://arxiv.org/pdf" in url.lower() or url.endswith(".pdf") or "youtube.com/watch" in url.lower():
            return True
        return False

    def _process_trafili_html(self, html):
        text = trafilatura.extract(html, include_formatting=True)
        return text


class FastParser:
    def __init__(self, extract_pdf=True,
                 allow_youtube_urls_extraction=False,
                 arxiv_html_flag=False,
                 llm=True):
        self.llm = llm
        self.extract_pdf = extract_pdf
        self.allow_youtube_urls_extraction = allow_youtube_urls_extraction
        self.arxiv_html_flag = arxiv_html_flag
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def _fetch_url(self, session, url, url_fetch_timeout=10):
        try:
            # Use SSL context in the request
            async with session.get(url, timeout=url_fetch_timeout, ssl=self.ssl_context) as response:
                if response.status == 200:
                    return await response.text()
                return ""
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error for {url}: {str(e)}")
            return ""
        except asyncio.TimeoutError:
            print(f"Timeout error for {url}")
            return ""
        except aiohttp.ClientConnectorCertificateError as e:
            print(f"SSL Certificate error for {url}: {str(e)}")
            return ""
        except Exception as e:
            print(f"Unexpected error fetching {url}: {str(e)}")
            return ""

    async def fetch_batch(self, urls: List[str]) -> List[FastParserResult]:
        # Configure client session with SSL context
        conn = aiohttp.TCPConnector(ssl=self.ssl_context)
        async with aiohttp.ClientSession(connector=conn) as session:
            tasks = [self._fetch_url(session, url) for url in urls]
            contents = await asyncio.gather(*tasks)
            return [FastParserResult(url=url, content=content)
                    for url, content in zip(urls, contents)]

    def fetch(self, url: str):
        res = self.fetch_batch([url])
        return FastParserResult(url=url, content=res[0].content if res else "")

    async def afetch_batch(self, urls: list) -> List[FastParserResult]:
        return await self._async_html_parser(urls)

    async def afetch(self, url: str):
        res = await self.afetch_batch([url])
        return FastParserResult(url=url, content=res[0][1] if res else "")

    async def aparse(self, urls: str | list, *args, **kwargs) -> FastParserResult | List[FastParserResult]:
        if isinstance(urls, str):
            return await self.afetch(urls)
        return await self.afetch_batch(urls)

    def __call__(self, urls: str | List[str]) -> List[FastParserResult] | FastParserResult:
        if isinstance(urls, str):
            urls = [urls]
        results = asyncio.run(self.fetch_batch(urls))
        return results[0] if len(urls) == 1 else results

    async def _async_html_parser(self, urls) -> List[FastParserResult]:
        html_urls = []
        pdf_urls = []
        yt_urls = []
        for url in tqdm(urls, desc="processing urls", unit='url'):
            url = self._arxiv_url_fix(url)
            if '/pdf' in url or url.lower().endswith('.pdf'):
                pdf_urls.append(url)
            elif 'youtube' in url:
                yt_urls.append(url)
            else:
                html_urls.append(url)

        results: List = []

        html_urls = list(dict.fromkeys(html_urls))
        pdf_urls = list(dict.fromkeys(pdf_urls))
        yt_urls = list(dict.fromkeys(yt_urls))

        if html_urls:
            fetcher = FastHTMLParserV3()
            html_results = await fetcher.fetch_content(urls=html_urls)
            results.extend(list(zip(html_urls, html_results)))

        if pdf_urls and self.extract_pdf:
            pdf_results = await self._fetch_pdf_content(pdf_urls)
            results.extend(list(zip(pdf_urls, pdf_results)))

        if self.allow_youtube_urls_extraction:
            yt_results = YoutubeExtractor.extract(urls=yt_urls)
            results.extend(list(zip(yt_urls, yt_results)))

        result_v1 = [FastParserResult(url=u, content=c) for u, c in results]
        return result_v1

    async def _fetch_pdf_content(self, pdf_urls):
        async def fetch_pdf(session, url):
            async with session.get(url) as response:
                if response.status == 200:
                    pdf_bytes = await response.read()
                    if self.llm:
                        return self.pymupdfllm_process(pdf_bytes)
                    else:
                        return self.pymupdf_process(pdf_bytes)
                else:
                    return ""

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_pdf(session, url) for url in pdf_urls]
            results = await asyncio.gather(*tasks)
            return results

    def _arxiv_url_fix(self, url):
        if 'https://arxiv.org/abs/' in url and self.extract_pdf:
            return url.replace('https://arxiv.org/abs/', 'https://arxiv.org/pdf/')
        elif 'http://arxiv.org/html/' in url:
            if self.arxiv_html_flag:  # default False
                return url.replace('http://arxiv.org/html/', 'https://arxiv.org/abs/')
            else:
                return url.replace('http://arxiv.org/html/', 'https://arxiv.org/pdf/')
        else:
            return url

    def pymupdf_process(self, pdf_bytes):
        # Open directly with fitz using the binary stream
        pdf_file = BytesIO(pdf_bytes)
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page in doc:
            # You can use different text extraction options here
            text += page.get_text() + "\n"  # Adding newline between pages
        doc.close()
        return text

    def pymupdfllm_process(self, pdf_bytes):
        import pymupdf4llm
        import tempfile
        import os

        # Create a temporary file with .pdf extension
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            # Write the bytes to the temp file
            temp_pdf.write(pdf_bytes)
            temp_path = temp_pdf.name

        try:
            # Use the temporary file path
            md_text = pymupdf4llm.to_markdown(temp_path)
            return md_text
        finally:
            # Clean up by removing the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def parse(urls: list | str, allow_pdf_extraction=True,
          allow_youtube_urls_extraction=False, arxiv_html_flag=False, llm=True) -> List[
                                                                                       FastParserResult] | FastParserResult:
    parser = FastParser(extract_pdf=allow_pdf_extraction,
                        allow_youtube_urls_extraction=allow_youtube_urls_extraction,
                        arxiv_html_flag=arxiv_html_flag,
                        llm=llm)
    return parser(urls)


async def aparse(urls: list | str, allow_pdf_extraction=True,
                 allow_youtube_urls_extraction=False, arxiv_html_flag=False, llm=True) -> List[
                                                                                              FastParserResult] | FastParserResult:
    parser = FastParser(extract_pdf=allow_pdf_extraction,
                        allow_youtube_urls_extraction=allow_youtube_urls_extraction,
                        arxiv_html_flag=arxiv_html_flag,
                        llm=llm)
    return await parser.aparse(urls)
