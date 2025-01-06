from types import TracebackType

import httpx


class OctobrowserClient:
    def __init__(
        self,
        *,
        local_url: str = "http://localhost:58888",
        api_url: str = "https://api.octobrowser.net",
        api_token: str | None = None,
    ) -> None:
        self.local_url = local_url.strip("/")
        self.api_url = api_url.strip("/")

        self.client = httpx.AsyncClient(timeout=120)

    async def __aenter__(self) -> "OctobrowserClient":
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self.client.__aexit__()

    async def start_profile(
        self,
        uuid: str,
        debug_port: bool | int = True,
        headless: bool = False,
        timeout: int = 120,
        flags: list[str] | None = None,
        only_local: bool | None = None,
        password: str | None = None,
    ) -> httpx.Response:
        payload = {
            "uuid": uuid,
            "headless": headless,
            "timeout": timeout,
            "debug_port": debug_port,
        }
        if flags:
            payload["flags"] = flags
        if only_local:
            payload["only_local"] = only_local
        if password:
            payload["password"] = password
        return await self.client.post(
            self.local_url + "/api/profiles/start", json=payload
        )
