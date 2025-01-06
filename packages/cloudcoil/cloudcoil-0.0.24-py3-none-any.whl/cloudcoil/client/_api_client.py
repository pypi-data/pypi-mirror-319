from typing import Any, Generic, Literal, Type, TypeVar

import httpx

from cloudcoil.client.errors import APIError, ResourceAlreadyExists, ResourceNotFound
from cloudcoil.resources import DEFAULT_PAGE_LIMIT, Resource, ResourceList

T = TypeVar("T", bound="Resource")


class _BaseAPIClient(Generic[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
    ) -> None:
        self.api_version = api_version
        self.kind = kind
        self.resource = resource
        self.default_namespace = default_namespace
        self.namespaced = namespaced

    def _build_url(self, namespace: str | None = None, name: str | None = None) -> str:
        api_base = f"/api/{self.api_version}"
        if "/" in self.api_version:
            api_base = f"/apis/{self.api_version}"
        if not name and not namespace:
            return f"{api_base}/{self.resource}"
        # One of namespace or name exists
        # If name does not exist, then namespace must exist
        if not name:
            if self.namespaced:
                return f"{api_base}/namespaces/{namespace}/{self.resource}"
            return f"{api_base}/{self.resource}"
        # name exists
        if not namespace and self.namespaced:
            raise ValueError("namespace must be provided when name is provided")
        if self.namespaced:
            return f"{api_base}/namespaces/{namespace}/{self.resource}/{name}"
        return f"{api_base}/{self.resource}/{name}"

    def _handle_get_response(self, response: httpx.Response, namespace: str, name: str) -> T:
        if response.status_code == 404:
            raise ResourceNotFound(
                f"Resource kind='{self.kind.__name__}', {namespace=}, {name=} not found"
            )
        return self.kind.model_validate_json(response.content)  # type: ignore

    def _handle_create_response(self, response: httpx.Response) -> T:
        if response.status_code == 409:
            raise ResourceAlreadyExists(response.json()["details"])
        if not response.is_success:
            raise APIError(response.json())
        return self.kind.model_validate_json(response.content)  # type: ignore


class APIClient(_BaseAPIClient[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
        client: httpx.Client,
    ) -> None:
        super().__init__(api_version, kind, resource, default_namespace, namespaced)
        self._client = client

    def get(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = self._client.get(url)
        return self._handle_get_response(response, namespace, name)

    def create(self, body: T, dry_run: bool = False) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata must be set for {body=}")
        namespace = body.namespace or self.default_namespace
        url = self._build_url(namespace=namespace)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        response = self._client.post(
            url, json=body.model_dump(mode="json", by_alias=True), params=params
        )
        return self._handle_create_response(response)

    def update(self, body: T, dry_run: bool = False) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata must be set for {body=}")
        namespace = body.namespace or self.default_namespace
        name = body.name
        url = self._build_url(namespace=namespace, name=name)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        response = self._client.put(
            url, json=body.model_dump(mode="json", by_alias=True), params=params
        )
        return self._handle_create_response(response)

    def delete(
        self,
        name: str,
        namespace: str | None = None,
        dry_run: bool = True,
        propagation_policy: Literal["orphan", "background", "foreground"] | None = None,
        grace_period_seconds: int | None = None,
    ) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        if propagation_policy:
            params["propagationPolicy"] = propagation_policy.capitalize()
        if grace_period_seconds:
            params["gracePeriodSeconds"] = grace_period_seconds
        response = self._client.delete(url, params=params)
        return self._handle_get_response(response, namespace, name)

    def remove(
        self,
        body: T,
        dry_run: bool = True,
        propagation_policy: Literal["orphan", "background", "foreground"] | None = None,
        grace_period_seconds: int | None = None,
    ) -> T:
        if not (body.metadata and body.metadata.name):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = body.metadata.namespace or self.default_namespace
        name = body.metadata.name
        return self.delete(
            name,
            namespace,
            dry_run=dry_run,
            propagation_policy=propagation_policy,
            grace_period_seconds=grace_period_seconds,
        )

    def list(
        self,
        namespace: str | None = None,
        all_namespaces: bool = False,
        continue_: None | str = None,
        field_selector: str | None = None,
        label_selector: str | None = None,
        limit: int = DEFAULT_PAGE_LIMIT,
    ) -> ResourceList[T]:
        namespace = namespace or self.default_namespace
        if all_namespaces:
            namespace = None
        url = self._build_url(namespace=namespace)
        params: dict[str, str | int] = {}
        if continue_:
            params["continue"] = continue_
        if field_selector:
            params["fieldSelector"] = field_selector
        if label_selector:
            params["labelSelector"] = label_selector
        if limit:
            params["limit"] = limit
        response = self._client.get(url, params=params)
        if not response.is_success:
            raise APIError(response.json())
        output = ResourceList[self.kind].model_validate_json(response.content)  # type: ignore
        assert output.metadata
        output._next_page_params = {
            "namespace": namespace,
            "all_namespaces": all_namespaces,
            "continue_": output.metadata.continue_,
            "field_selector": field_selector,
            "label_selector": label_selector,
            "limit": limit,
        }
        return output


class AsyncAPIClient(_BaseAPIClient[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
        client: httpx.AsyncClient,
    ) -> None:
        super().__init__(api_version, kind, resource, default_namespace, namespaced)
        self._client = client

    async def get(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = await self._client.get(url)
        return self._handle_get_response(response, namespace, name)

    async def create(self, body: T, dry_run: bool = False) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = body.namespace or self.default_namespace
        url = self._build_url(namespace=namespace)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        response = await self._client.post(
            url, json=body.model_dump(mode="json", by_alias=True), params=params
        )
        return self._handle_create_response(response)

    async def update(self, body: T, dry_run: bool = False) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata must be set for {body=}")
        namespace = body.namespace or self.default_namespace
        name = body.name
        url = self._build_url(namespace=namespace, name=name)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        response = await self._client.put(
            url, json=body.model_dump(mode="json", by_alias=True), params=params
        )
        return self._handle_create_response(response)

    async def delete(
        self,
        name: str,
        namespace: str | None = None,
        dry_run: bool = True,
        propagation_policy: Literal["orphan", "background", "foreground"] | None = None,
        grace_period_seconds: int | None = None,
    ) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "All"
        if propagation_policy:
            params["propagationPolicy"] = propagation_policy.capitalize()
        if grace_period_seconds:
            params["gracePeriodSeconds"] = grace_period_seconds
        response = await self._client.delete(url, params=params)
        return self._handle_get_response(response, namespace, name)

    async def remove(
        self,
        body: T,
        dry_run: bool = True,
        propagation_policy: Literal["orphan", "background", "foreground"] | None = None,
        grace_period_seconds: int | None = None,
    ) -> T:
        if not (body.metadata and body.metadata.name):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = body.metadata.namespace or self.default_namespace
        name = body.metadata.name
        return await self.delete(
            name,
            namespace,
            dry_run=dry_run,
            propagation_policy=propagation_policy,
            grace_period_seconds=grace_period_seconds,
        )

    async def list(
        self,
        namespace: str | None = None,
        all_namespaces: bool = False,
        continue_: None | str = None,
        field_selector: str | None = None,
        label_selector: str | None = None,
        limit: int = DEFAULT_PAGE_LIMIT,
    ) -> ResourceList[T]:
        namespace = namespace or self.default_namespace
        if all_namespaces:
            namespace = None
        url = self._build_url(namespace=namespace)
        params: dict[str, str | int] = {}
        if continue_:
            params["continue"] = continue_
        if field_selector:
            params["fieldSelector"] = field_selector
        if label_selector:
            params["labelSelector"] = label_selector
        if limit:
            params["limit"] = limit
        response = await self._client.get(url, params=params)
        if not response.is_success:
            raise APIError(response.json())
        output = ResourceList[self.kind].model_validate_json(response.content)  # type: ignore
        assert output.metadata
        output._next_page_params = {
            "namespace": namespace,
            "all_namespaces": all_namespaces,
            "continue_": output.metadata.continue_,
            "field_selector": field_selector,
            "label_selector": label_selector,
            "limit": limit,
        }
        return output
