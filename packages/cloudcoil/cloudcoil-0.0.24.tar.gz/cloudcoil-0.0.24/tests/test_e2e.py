"""Tests for cloudcoil package."""

import pytest

import cloudcoil.models.kubernetes as k8s
from cloudcoil.apimachinery import ObjectMeta


@pytest.mark.configure_test_cluster(cluster_name="test-cloudcoil-v1.31", remove=False)
def test_e2e(test_config):
    with test_config:
        assert k8s.core.v1.Service.get("kubernetes", "default").metadata.name == "kubernetes"
        output = k8s.core.v1.Namespace(metadata=ObjectMeta(generate_name="test-")).create()
        name = output.metadata.name
        assert k8s.core.v1.Namespace.get(name).metadata.name == name
        output.metadata.annotations = {"test": "test"}
        output = output.update()
        assert output.metadata.annotations == {"test": "test"}
        assert output.remove(dry_run=True).metadata.name == name
        assert (
            k8s.core.v1.Namespace.delete(name, grace_period_seconds=0).status.phase == "Terminating"
        )
        assert len(k8s.core.v1.Pod.list(all_namespaces=True, limit=1)) > 1
        assert len(k8s.core.v1.Pod.list(all_namespaces=True, limit=1).items) == 1


@pytest.mark.configure_test_cluster(
    cluster_name="test-cloudcoil-v1.29", remove=True, version="v1.29.12"
)
def test_e2e_traditional(test_config):
    with test_config:
        assert k8s.core.v1.Service.get("kubernetes", "default").metadata.name == "kubernetes"
        output = k8s.core.v1.Namespace(metadata=ObjectMeta(generate_name="test-")).create()
        name = output.metadata.name
        assert k8s.core.v1.Namespace.get(name).metadata.name == name
        output.metadata.annotations = {"test": "test"}
        output = output.update()
        assert output.metadata.annotations == {"test": "test"}
        assert output.remove(dry_run=True).metadata.name == name
        assert (
            k8s.core.v1.Namespace.delete(name, grace_period_seconds=0).status.phase == "Terminating"
        )
        assert len(k8s.core.v1.Pod.list(all_namespaces=True, limit=1)) > 1
        assert len(k8s.core.v1.Pod.list(all_namespaces=True, limit=1).items) == 1


@pytest.mark.configure_test_cluster(
    cluster_name="test-cloudcoil-v1.30", remove=False, version="v1.30.8"
)
async def test_async_e2e(test_config):
    with test_config:
        assert (
            await k8s.core.v1.Service.async_get("kubernetes", "default")
        ).metadata.name == "kubernetes"
        output = await k8s.core.v1.Namespace(
            metadata=ObjectMeta(generate_name="test-")
        ).async_create()
        name = output.metadata.name
        assert (await k8s.core.v1.Namespace.async_get(name)).metadata.name == name
        output.metadata.annotations = {"test": "test"}
        output = await output.async_update()
        assert output.metadata.annotations == {"test": "test"}
        assert (await output.async_remove(dry_run=True)).metadata.name == name
        assert (
            await k8s.core.v1.Namespace.async_delete(name, grace_period_seconds=0)
        ).status.phase == "Terminating"
        assert len(await k8s.core.v1.Pod.async_list(all_namespaces=True, limit=1)) > 1
        assert len((await k8s.core.v1.Pod.async_list(all_namespaces=True, limit=1)).items) == 1
