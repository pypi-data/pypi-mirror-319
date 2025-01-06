from contextlib import nullcontext

import httpx


async def start_profile(
    uuid: str,
    debug_port: bool | int = True,
    headless: bool = False,
    timeout: int = 120,
    flags: list[str] | None = None,
    only_local: bool | None = None,
    password: str | None = None,
    *,
    client: httpx.AsyncClient | None = None,
    **kwargs,
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

    if client:
        ctx = nullcontext()
    else:
        client = ctx = httpx.AsyncClient(base_url="http://localhost:58888", timeout=timeout)

    async with ctx:
        return await client.post("/api/profiles/start", json=payload)
