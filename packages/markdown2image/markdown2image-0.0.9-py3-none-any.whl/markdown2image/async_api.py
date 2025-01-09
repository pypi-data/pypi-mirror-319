from typing import Optional, TypedDict
from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page
from asyncio import Future
import markdown

# Init browser and context
class T_status_page(TypedDict):
    id: int
    busy: bool
    page: Page

class IdlePagesManager():
    def __init__(self) -> None:
        self.pages: list[T_status_page] = []
        self.futures: list[Future[T_status_page]] = []

    async def new_page(self) -> T_status_page:
        page = await _context.new_page()
        status_page: T_status_page = {
            'id': len(self.pages),
            'busy': False,
            'page': page
        }
        self.pages.append(status_page)
        return status_page

    async def get_idle_page(self) -> T_status_page:
        # Use existing idle page
        for status_page in self.pages:
            if not status_page['busy']:
                return status_page
        
        # No idle page available for now
        if len(self.pages) < max_pages:
            # create a new page
            status_page = await self.new_page()
            return status_page
        else:
            # reaching max_page limit
            status_page = await self.wait_for_page_idle()
            return status_page
    
    async def wait_for_page_idle(self) -> T_status_page:
        # create a Future and wait for self.set_page_status finishing it
        future: Future[T_status_page] = Future()
        self.futures.append(future)
        status_page = await future
        return status_page

    def set_page_status(self, page_id: int, status: bool):
        for status_page in self.pages:
            if status_page['id'] == page_id:
                status_page['busy'] = status
                if self.futures:
                    future = self.futures.pop(0)
                    future.set_result(status_page)
                return
        raise Exception(f'No page found with provided page_id {repr(page_id)}')

_playwright: Playwright
_browser: Browser
_context: BrowserContext
_manager: IdlePagesManager
initialized: bool = False

# config vars
max_pages: int = 5

async def _init():
    global _playwright, _browser, _context, _manager, initialized
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch()
    _context = await _browser.new_context(viewport={'width': 800, 'height': 1})
    _manager = IdlePagesManager()
    initialized = True

async def html2image(html: str, path: str, *, width: Optional[int] = None):
    if not initialized: await _init()
    
    # Get an idle page to render
    status_page = await _manager.get_idle_page()
    _manager.set_page_status(status_page['id'], True)
    page = status_page['page']
    
    # render & screenshot
    await page.reload(wait_until='commit')
    if width != None: await page.set_viewport_size({"width": width, "height": 1})
    await page.set_content(html=html, wait_until='load')
    await page.screenshot(path=path, full_page=True)
    
    # release page to idle pages
    _manager.set_page_status(status_page['id'], False)

async def markdown2image(md: str, path: str, width: Optional[int] = None):
    html = markdown.markdown(md)
    await html2image(html, path, width=width)