from typing import Optional

from blacksmith.domain.typing import AsyncMiddleware
from blacksmith.typing import Proxies


class AsyncAbstractTransport(AsyncMiddleware):
    verify_certificate: bool
    proxies: Optional[Proxies]

    def __init__(
        self, verify_certificate: bool = True, proxies: Optional[Proxies] = None
    ):
        self.verify_certificate = verify_certificate
        self.proxies = proxies
