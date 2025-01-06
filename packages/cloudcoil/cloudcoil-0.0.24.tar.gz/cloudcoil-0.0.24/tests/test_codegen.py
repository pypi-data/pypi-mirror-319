import re

import pytest

from cloudcoil.codegen.generator import ModelConfig, Substitution, generate, process_definitions

K8S_OPENAPI_URL = (
    "https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json"
)


@pytest.fixture
def sample_schema():
    return {
        "definitions": {
            "io.k8s.api.apps.v1.Deployment": {
                "x-kubernetes-group-version-kind": [
                    {"group": "apps", "kind": "Deployment", "version": "v1"}
                ],
                "properties": {
                    "apiVersion": {"type": "string"},
                    "kind": {"type": "string"},
                    "metadata": {
                        "$ref": "#/definitions/io.k8s.apimachinery.pkg.apis.meta.v1.ObjectMeta"
                    },
                },
            }
        }
    }


@pytest.fixture
def model_config(tmp_path):
    return ModelConfig(
        namespace="test.k8s",
        input_=K8S_OPENAPI_URL,
        substitutions=[
            Substitution(
                from_=r"^io\.k8s\.apimachinery\..*\.(.+)",
                to=r"apimachinery.\g<1>",
                namespace="cloudcoil",
            ),
            Substitution(
                from_=r"^io\.k8s\.apiextensions-apiserver\.pkg\.apis\.apiextensions\.(.+)$",
                to=r"apiextensions.\g<1>",
            ),
            Substitution(from_=r"^io\.k8s\.api\.(.+)$", to=r"\g<1>"),
            Substitution(from_=r"^io\.k8s\.kube-aggregator\.pkg\.apis\.(.+)$", to=r"\g<1>"),
        ],
    )


def test_substitution():
    subs = Substitution(from_="io.k8s.api.(.+)", to="k8s.\\1")
    assert isinstance(subs.from_, re.Pattern)
    assert subs.to == "k8s.\\1"


def test_model_config_validation():
    config = ModelConfig(
        namespace="test",
        input_="test.json",
        substitutions=[
            Substitution(from_="test", to="replaced"),
        ],
    )
    assert config.namespace == "test"
    assert config.input_ == "test.json"
    assert len(config.transformations) == 2
    assert config.transformations[0].match_.pattern == "test"
    assert config.transformations[0].replace == "replaced"
    assert config.transformations[0].namespace == "test"
    assert config.transformations[1].match_.pattern == "^(.*)$"
    assert config.transformations[1].replace == r"\g<1>"
    assert config.transformations[1].namespace == "test"


def test_process_definitions(sample_schema):
    process_definitions(sample_schema)
    deployment = sample_schema["definitions"]["io.k8s.api.apps.v1.Deployment"]
    assert deployment["properties"]["apiVersion"]["enum"] == ["apps/v1"]
    assert deployment["properties"]["kind"]["enum"] == ["Deployment"]
    assert "metadata" not in deployment.get("required", [])


def test_generate_k8s_models(model_config, tmp_path):
    model_config.output = tmp_path
    generate(model_config)
    output_dir = tmp_path / "test" / "k8s"

    # Check if output directory exists and contains py.typed file
    assert output_dir.exists()
    assert (output_dir / "py.typed").exists()

    # Verify generated Python files
    python_files = list(output_dir.glob("**/*.py"))
    assert python_files, "No Python files were generated"

    # Check for specific model files and their content
    apps_v1_file = next((f for f in python_files if "apps/v1" in str(f)), None)
    assert apps_v1_file is not None, "apps/v1 models not found"

    # Verify file content
    content = apps_v1_file.read_text()
    assert "class Deployment(" in content, "Deployment model not found"
    assert "from cloudcoil.resources import Resource" in content, "Base class import missing"
    assert "from cloudcoil import apimachinery" in content, "Apimachinery import missing"

    # Verify imports are correct (no relative imports for apimachinery)
    assert "from .. import apimachinery" not in content
    assert "from ... import apimachinery" not in content


def test_int_or_string_conversion(sample_schema):
    sample_schema["definitions"]["TestType"] = {
        "properties": {"value": {"type": "string", "format": "int-or-string"}}
    }
    process_definitions(sample_schema)
    assert sample_schema["definitions"]["TestType"]["properties"]["value"]["type"] == [
        "integer",
        "string",
    ]
    assert "format" not in sample_schema["definitions"]["TestType"]["properties"]["value"]


def test_process_definitions_with_lists(sample_schema):
    sample_schema["definitions"]["io.k8s.api.apps.v1.DeploymentList"] = {
        "properties": {
            "apiVersion": {"type": "string"},
            "kind": {"type": "string"},
            "metadata": {"$ref": "#/definitions/io.k8s.apimachinery.pkg.apis.meta.v1.ListMeta"},
            "items": {
                "type": "array",
                "items": {"$ref": "#/definitions/io.k8s.api.apps.v1.Deployment"},
            },
        }
    }
    process_definitions(sample_schema)
    deployment_list = sample_schema["definitions"]["io.k8s.api.apps.v1.DeploymentList"]
    assert "metadata" not in deployment_list.get("required", [])
    assert "items" in deployment_list["properties"]


def test_generate_with_exclusions(tmp_path):
    config = ModelConfig(
        namespace="test.k8s",
        input_=K8S_OPENAPI_URL,
        output=tmp_path,
        transformations=[
            {"match": r"io\.k8s\.api\.apps\.v1\.DaemonSet.*", "exclude": True},
            {"match": r"io\.k8s\.api\.(.+)", "replace": r"\1"},
        ],
    )
    generate(config)

    output_dir = tmp_path / "test" / "k8s"
    assert output_dir.exists()

    # Check that DaemonSet is excluded
    for py_file in output_dir.rglob("*.py"):
        content = py_file.read_text()
        assert "class DaemonSet(" not in content
        assert "class DaemonSetList(" not in content


def test_generate_init_files(tmp_path):
    config = ModelConfig(
        namespace="test.k8s",
        input_=K8S_OPENAPI_URL,
        output=tmp_path,
        transformations=[
            {"match": r"io\.k8s\.api\.(.+)", "replace": r"\1"},
        ],
        generate_init=True,
    )
    generate(config)

    output_dir = tmp_path / "test" / "k8s"
    assert (output_dir / "__init__.py").exists()

    # Check that __init__.py contains appropriate imports
    init_content = (output_dir / "__init__.py").read_text()
    assert "from . import" in init_content
    assert "# Generated by cloudcoil-model-codegen" in init_content


def test_generate_without_init_files(tmp_path):
    config = ModelConfig(
        namespace="test.k8s",
        input_=K8S_OPENAPI_URL,
        output=tmp_path,
        transformations=[
            {"match": r"io\.k8s\.api\.(.+)", "replace": r"\1"},
        ],
        generate_init=False,
    )
    generate(config)

    output_dir = tmp_path / "test" / "k8s"
    assert not (output_dir / "__init__.py").exists()


def test_model_config_validation_errors():
    with pytest.raises(ValueError, match="Only transformations can be used"):
        ModelConfig(
            namespace="test",
            input_="test.json",
            substitutions=[Substitution(from_="test", to="replaced")],
            transformations=[{"match": "test", "replace": "other"}],
        )

    with pytest.raises(ValueError, match="replace is required"):
        ModelConfig(
            namespace="test",
            input_="test.json",
            transformations=[{"match": "test"}],
        )


def test_model_config_with_additional_args(tmp_path):
    config = ModelConfig(
        namespace="test.k8s",
        input_=K8S_OPENAPI_URL,
        output=tmp_path,
        additional_datamodel_codegen_args=["--collapse-root-models"],
    )
    generate(config)

    output_dir = tmp_path / "test" / "k8s"
    assert output_dir.exists()

    # Verify generated files include field constraints
    for py_file in output_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        content = py_file.read_text()
        assert "RootModel" not in content
