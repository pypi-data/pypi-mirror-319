import random
import statistics
from typing import Sequence, Union, overload

from pydantic import BaseModel, Field

from cyantic import Blueprint, blueprint, CyanticModel


class SimpleModel(CyanticModel):
    """A simple model for testing hooks."""

    name: str


class CounterModel(CyanticModel):
    """A model for testing stateful hooks."""

    first: int
    second: int
    third: int


class Tensor(BaseModel):
    """A simple mock tensor class that wraps a list of numbers.

    We use this because we don't want to take torch as a dependency.
    """

    data: list[float]

    @classmethod
    def from_list(cls, values: Sequence[float]) -> "Tensor":
        return cls(data=list(values))

    def __len__(self) -> int:
        return len(self.data)

    def mean(self) -> float:
        return statistics.mean(self.data)

    def std(self) -> float:
        return statistics.stdev(self.data)

    @overload
    def __getitem__(self, idx: int) -> float: ...

    @overload
    def __getitem__(self, idx: slice) -> "Tensor": ...

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, "Tensor"]:
        if isinstance(idx, slice):
            return Tensor(data=self.data[idx])
        return self.data[idx]

    def __hash__(self) -> int:
        """Make Tensor hashable for use in sets."""
        return hash(tuple(self.data))

    def __eq__(self, other: object) -> bool:
        """Define equality for hash consistency."""
        if not isinstance(other, Tensor):
            return NotImplemented
        return self.data == other.data


@blueprint(Tensor)
class NormalTensor(Blueprint[Tensor]):
    """Blueprint for creating tensors from a normal distribution."""

    mean: float
    std_dev: float
    size: int = Field(gt=0, description="Size must be a positive integer")

    def build(self) -> Tensor:
        return Tensor(
            data=[random.gauss(self.mean, self.std_dev) for _ in range(self.size)]
        )


@blueprint(Tensor)
class UniformTensor(Blueprint[Tensor]):
    """Blueprint for creating tensors with values from a uniform distribution."""

    low: float
    high: float
    size: int = Field(gt=0, description="Size must be a positive integer")

    def build(self) -> Tensor:
        return Tensor(
            data=[random.uniform(self.low, self.high) for _ in range(self.size)]
        )


class DataContainer(CyanticModel):
    """Example model using cast-enabled tensor."""

    values: Tensor


def test_cast_build():
    """Test the cast building functionality."""
    # Test direct tensor assignment
    direct_tensor = Tensor.from_list([1.0, 2.0, 3.0])
    model1 = DataContainer(values=direct_tensor)
    assert len(model1.values) == 3
    assert list(model1.values.data) == [1.0, 2.0, 3.0]

    # Test normal distribution cast - verify only size and type
    cast_dict = {"values": {"mean": 0.0, "std_dev": 1.0, "size": 10}}
    model2 = DataContainer.model_validate(cast_dict)
    assert len(model2.values) == 10
    assert isinstance(model2.values, Tensor)
    assert all(isinstance(x, float) for x in model2.values.data)

    # Test validation error for missing required fields
    try:
        DataContainer.model_validate({"values": {"mean": 0.0}})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


class TensorContainers(CyanticModel):
    """A model containing tensors in various container types."""

    list_tensors: list[Tensor]
    dict_tensors: dict[str, Tensor]
    set_tensors: set[Tensor]
    tuple_tensors: tuple[Tensor, ...]


def test_container_of_blueprints():
    """Test handling various container types with blueprinted fields."""
    # Test data with different container types
    container_data = {
        "list_tensors": [
            {"mean": 0.0, "std_dev": 1.0, "size": 10},
            {"low": 0.0, "high": 1.0, "size": 20},
        ],
        "dict_tensors": {
            "normal": {"mean": 0.0, "std_dev": 1.0, "size": 15},
            "uniform": {"low": -1.0, "high": 1.0, "size": 25},
        },
        "set_tensors": [  # Sets can be initialized from lists
            {"mean": 1.0, "std_dev": 0.5, "size": 30},
            {"low": -2.0, "high": 2.0, "size": 40},
        ],
        "tuple_tensors": [  # Tuples can be initialized from lists
            {"mean": -1.0, "std_dev": 2.0, "size": 45},
            {"low": 0.0, "high": 5.0, "size": 55},
        ],
    }

    model = TensorContainers.model_validate(container_data)

    # Test list container
    assert isinstance(model.list_tensors, list)
    assert len(model.list_tensors) == 2
    assert all(isinstance(t, Tensor) for t in model.list_tensors)
    assert len(model.list_tensors[0]) == 10
    assert len(model.list_tensors[1]) == 20

    # Test dict container
    assert isinstance(model.dict_tensors, dict)
    assert set(model.dict_tensors.keys()) == {"normal", "uniform"}
    assert all(isinstance(t, Tensor) for t in model.dict_tensors.values())
    assert len(model.dict_tensors["normal"]) == 15
    assert len(model.dict_tensors["uniform"]) == 25

    # Test set container
    assert isinstance(model.set_tensors, set)
    assert len(model.set_tensors) == 2
    assert all(isinstance(t, Tensor) for t in model.set_tensors)
    assert any(len(t) == 30 for t in model.set_tensors)
    assert any(len(t) == 40 for t in model.set_tensors)

    # Test tuple container
    assert isinstance(model.tuple_tensors, tuple)
    assert len(model.tuple_tensors) == 2
    assert all(isinstance(t, Tensor) for t in model.tuple_tensors)
    assert len(model.tuple_tensors[0]) == 45
    assert len(model.tuple_tensors[1]) == 55

    # Test validation with invalid items
    invalid_data = {
        "list_tensors": [{"mean": 0.0}],  # Missing required fields
        "dict_tensors": {"bad": {"std_dev": 1.0}},  # Missing required fields
        "set_tensors": [{"size": -1}],  # Invalid size
        "tuple_tensors": [{"low": 1.0, "high": 0.0}],  # Invalid range
    }

    try:
        TensorContainers.model_validate(invalid_data)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test uniform distribution cast - verify size and types
    model3 = DataContainer.model_validate(
        {"values": {"low": -1.0, "high": 1.0, "size": 50}}
    )
    assert len(model3.values) == 50
    assert isinstance(model3.values, Tensor)
    assert all(isinstance(x, float) for x in model3.values.data)


class NestedConfig(BaseModel):
    """A regular Pydantic model for configuration."""

    name: str
    scale: float


class NestedTensorContainer(CyanticModel):
    """A CyanticModel that will be nested inside another CyanticModel."""

    config: NestedConfig
    tensor: Tensor


class ComplexDataContainer(CyanticModel):
    """A CyanticModel containing both regular fields and nested CyanticModels."""

    name: str
    primary: Tensor
    secondary: NestedTensorContainer


def test_nested_blueprint_models():
    """Test nested CyanticModels with mixed BaseModel types."""
    # Test nested structure with both normal and blueprint fields

    nested_data = {
        "name": "test_complex",
        "primary": {"mean": 0.0, "std_dev": 1.0, "size": 50},
        "secondary": {
            "config": {"name": "nested", "scale": 2.0},
            "tensor": {"low": -1.0, "high": 1.0, "size": 30},
        },
    }

    model = ComplexDataContainer.model_validate(nested_data)

    # Verify top level fields
    assert model.name == "test_complex"
    assert len(model.primary) == 50

    # Verify nested structure
    assert model.secondary.config.name == "nested"
    assert model.secondary.config.scale == 2.0
    assert len(model.secondary.tensor) == 30


def test_mixed_model_validation():
    """Test validation behavior with mixed model types."""
    # Test validation with missing nested fields
    invalid_data = {
        "name": "test_invalid",
        "primary": {"mean": 0.0, "std_dev": 1.0, "size": 50},
        "secondary": {
            "config": {"name": "nested"},  # Missing scale
            "tensor": {"low": -1.0, "high": 1.0, "size": 30},
        },
    }

    try:
        ComplexDataContainer.model_validate(invalid_data)
        assert False, "Should have raised ValueError for missing scale"
    except ValueError:
        pass

    # Test validation with invalid parameters
    invalid_data = {
        "name": "test_invalid",
        "primary": {"mean": 0.0, "std_dev": 1.0, "size": -50},  # Invalid size
        "secondary": {
            "config": {"name": "nested", "scale": 2.0},
            "tensor": {"low": -1.0, "high": 1.0, "size": 30},
        },
    }

    try:
        ComplexDataContainer.model_validate(invalid_data)
        assert False, "Should have raised ValueError for negative size"
    except ValueError:
        pass


def test_blueprint_type_inference():
    """Test that we correctly infer and apply different blueprints."""
    # Test that both NormalTensor and UniformTensor blueprints work in the same model
    mixed_data = {
        "name": "test_mixed",
        "primary": {"mean": 0.0, "std_dev": 1.0, "size": 100},
        "secondary": {
            "config": {"name": "nested", "scale": 2.0},
            "tensor": {"low": 0.0, "high": 1.0, "size": 100},
        },
    }

    model = ComplexDataContainer.model_validate(mixed_data)

    # Verify that different blueprints were correctly applied
    assert len(model.primary) == 100
    assert len(model.secondary.tensor) == 100

    # Verify types and sizes only
    assert isinstance(model.primary, Tensor)
    assert isinstance(model.secondary.tensor, Tensor)
    assert len(model.primary) == 100
    assert len(model.secondary.tensor) == 100
    assert all(isinstance(x, float) for x in model.primary.data)
    assert all(isinstance(x, float) for x in model.secondary.tensor.data)


class TensorWrapper(CyanticModel):
    """A simple CyanticModel that will be nested in a BaseModel."""

    tensor: Tensor


class ConfigWithTensor(BaseModel):
    """A BaseModel that contains a CyanticModel."""

    name: str
    description: str | None = None
    data: TensorWrapper


def test_cyanticmodel_in_basemodel():
    """Test a CyanticModel nested inside a regular Pydantic BaseModel."""
    config_data = {
        "name": "test_config",
        "description": "Testing CyanticModel inside BaseModel",
        "data": {"tensor": {"mean": 0.0, "std_dev": 1.0, "size": 50}},
    }

    model = ConfigWithTensor.model_validate(config_data)

    # Verify BaseModel fields
    assert model.name == "test_config"
    assert model.description == "Testing CyanticModel inside BaseModel"

    # Verify the nested CyanticModel types and sizes
    assert isinstance(model.data.tensor, Tensor)
    assert len(model.data.tensor) == 50
    assert all(isinstance(x, float) for x in model.data.tensor.data)

    # Test validation with invalid nested blueprint
    invalid_data = {
        "name": "test_invalid",
        "data": {
            "tensor": {
                "mean": 0.0,
                "std_dev": 1.0,
                "size": -10,  # Invalid negative size
            }
        },
    }

    try:
        ConfigWithTensor.model_validate(invalid_data)
        assert False, "Should have raised ValueError for negative size"
    except ValueError:
        pass
