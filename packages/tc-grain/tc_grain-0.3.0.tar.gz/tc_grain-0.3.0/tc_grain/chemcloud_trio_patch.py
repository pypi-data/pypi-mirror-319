"""Asyncify ChemCloud
Asyncified components:
    - Output request
    - Output polling sleep
    - Compute request
TODO:
    - Refresh token?
"""
from chemcloud.models import (
    FutureOutput,
    FutureOutputBase,
    FutureOutputGroup,
    QCIOInputsOrList,
    QCIOInputs,
    QCIOOutputsOrList,
)
from chemcloud.http_client import _RequestsClient, json_dumps
from chemcloud.client import CCClient

import trio
import httpx
from time import time
from typing import Any


async def aget(
    self: FutureOutput | FutureOutputGroup,
    timeout: float | None = None,
    interval: float = 1.0,
) -> QCIOOutputsOrList:
    if self.result:
        return self.result

    start_time = time()
    tid = self.task_id

    while True:
        _, self.result = await self.client.aoutput(tid)
        if self.result:
            break
        if timeout:
            if (time() - start_time) > timeout:
                raise TimeoutError(
                    f"Your timeout limit of {timeout} seconds was exceeded"
                )
        await trio.sleep(interval)

    return self.result


FutureOutputBase.aget = aget


async def _arequest(
    self: _RequestsClient,
    method: str,
    route: str,
    *,
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    api_call: bool = True,
):
    """Make HTTP request"""
    url = (
        f"{self._chemcloud_domain}"
        f"{self._settings.chemcloud_api_version_prefix if api_call else ''}{route}"
    )
    request = httpx.Request(
        method,
        url,
        headers=headers,
        data=data,
        params=params,
    )
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=20.0)) as client:
        response = await client.send(request)
    response.raise_for_status()
    return response.json()


async def _authenticated_arequest(
    self: _RequestsClient, method: str, route: str, **kwargs
):
    """Make authenticated HTTP request"""
    kwargs["headers"] = kwargs.get("headers", {})
    access_token = self._get_access_token()
    kwargs["headers"]["Authorization"] = f"Bearer {access_token}"
    return await self._arequest(
        method,
        route,
        **kwargs,
    )


async def acompute(
    self: _RequestsClient,
    inp_obj: QCIOInputs,
    params: dict[str, Any] | None = None,
) -> FutureOutput | FutureOutputGroup:
    """Submit a computation to ChemCloud"""
    result_id = await self._authenticated_arequest(
        "post",
        "/compute",
        data=json_dumps(inp_obj),
        params=params or {},
    )
    return self._result_id_to_future_result(inp_obj, result_id)


async def aoutput(
    self: _RequestsClient,
    task_id: str,
) -> tuple[str, Any | list[Any] | None]:
    response = await self._authenticated_arequest("get", f"/compute/output/{task_id}")
    return response["status"], response["program_output"]


_RequestsClient._arequest = _arequest
_RequestsClient._authenticated_arequest = _authenticated_arequest
_RequestsClient.acompute = acompute
_RequestsClient.aoutput = aoutput


async def cc_acompute(
    self: CCClient,
    program: str,
    inp_obj: QCIOInputsOrList,
    **kwargs,
) -> FutureOutput | FutureOutputGroup:
    if self.supported_programs is not None:
        assert (
            program in self.supported_programs
        ), f"Please use one of the following programs: {self.supported_programs}"

    compute_params = dict(
        program=program,
        **kwargs,
    )
    return await self._client.acompute(inp_obj, compute_params)


CCClient.acompute = cc_acompute
