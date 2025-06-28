import pytest
from typing import List, Dict, Union, Optional
from fastapi._compat import (
    field_annotation_is_sequence,
    field_annotation_is_scalar,
    field_annotation_is_complex,
    field_annotation_is_scalar_sequence,
    value_is_sequence,
    is_bytes_or_nonable_bytes_annotation,
    is_uploadfile_or_nonable_uploadfile_annotation,
    is_bytes_sequence_annotation,
    is_uploadfile_sequence_annotation,
    _annotation_is_sequence,
    _annotation_is_complex,
    _regenerate_error_with_loc,
    _normalize_errors,
)
from pydantic import BaseModel
from starlette.datastructures import UploadFile
from tests.utils import needs_pydanticv1, needs_pydanticv2


class SampleModel(BaseModel):
    name: str
    value: int


class TestFieldAnnotationFunctions:
    def test_field_annotation_is_sequence(self):
        assert field_annotation_is_sequence(List[str]) is True
        assert field_annotation_is_sequence(list) is True
        assert field_annotation_is_sequence(tuple) is True
        assert field_annotation_is_sequence(set) is True
        assert field_annotation_is_sequence(str) is False
        assert field_annotation_is_sequence(int) is False

    def test_field_annotation_is_scalar(self):
        assert field_annotation_is_scalar(str) is True
        assert field_annotation_is_scalar(int) is True
        assert field_annotation_is_scalar(float) is True
        assert field_annotation_is_scalar(bool) is True
        assert field_annotation_is_scalar(List[str]) is False
        assert field_annotation_is_scalar(SampleModel) is False

    def test_field_annotation_is_complex(self):
        assert field_annotation_is_complex(SampleModel) is True
        assert field_annotation_is_complex(Dict[str, str]) is True
        assert field_annotation_is_complex(List[str]) is True
        assert field_annotation_is_complex(UploadFile) is True
        assert field_annotation_is_complex(str) is False
        assert field_annotation_is_complex(int) is False

    def test_field_annotation_is_scalar_sequence(self):
        assert field_annotation_is_scalar_sequence(List[str]) is True
        assert field_annotation_is_scalar_sequence(List[int]) is True
        assert field_annotation_is_scalar_sequence(List[SampleModel]) is False
        assert field_annotation_is_scalar_sequence(str) is False

    def test_union_annotations(self):
        union_type = Union[str, int]
        assert field_annotation_is_scalar(union_type) is True
        
        complex_union = Union[str, List[str]]
        assert field_annotation_is_complex(complex_union) is True

        optional_str = Optional[str]
        assert field_annotation_is_scalar(optional_str) is True

    def test_ellipsis_annotation(self):
        assert field_annotation_is_scalar(...) is True


class TestValueFunctions:
    def test_value_is_sequence(self):
        assert value_is_sequence([1, 2, 3]) is True
        assert value_is_sequence((1, 2, 3)) is True
        assert value_is_sequence({1, 2, 3}) is True
        assert value_is_sequence("string") is False
        assert value_is_sequence(b"bytes") is False
        assert value_is_sequence(123) is False
        assert value_is_sequence(None) is False


class TestBytesAnnotations:
    def test_is_bytes_annotation(self):
        assert is_bytes_or_nonable_bytes_annotation(bytes) is True
        assert is_bytes_or_nonable_bytes_annotation(Union[bytes, None]) is True
        assert is_bytes_or_nonable_bytes_annotation(Optional[bytes]) is True
        assert is_bytes_or_nonable_bytes_annotation(str) is False
        assert is_bytes_or_nonable_bytes_annotation(int) is False

    def test_is_bytes_sequence_annotation(self):
        assert is_bytes_sequence_annotation(List[bytes]) is True
        assert is_bytes_sequence_annotation(List[Union[bytes, None]]) is True
        assert is_bytes_sequence_annotation(List[str]) is False
        assert is_bytes_sequence_annotation(bytes) is False


class TestUploadFileAnnotations:
    def test_is_uploadfile_annotation(self):
        assert is_uploadfile_or_nonable_uploadfile_annotation(UploadFile) is True
        assert is_uploadfile_or_nonable_uploadfile_annotation(Union[UploadFile, None]) is True
        assert is_uploadfile_or_nonable_uploadfile_annotation(Optional[UploadFile]) is True
        assert is_uploadfile_or_nonable_uploadfile_annotation(str) is False
        assert is_uploadfile_or_nonable_uploadfile_annotation(bytes) is False

    def test_is_uploadfile_sequence_annotation(self):
        assert is_uploadfile_sequence_annotation(List[UploadFile]) is True
        assert is_uploadfile_sequence_annotation(List[Union[UploadFile, None]]) is True
        assert is_uploadfile_sequence_annotation(List[str]) is False
        assert is_uploadfile_sequence_annotation(UploadFile) is False


class TestPrivateAnnotationFunctions:
    def test_annotation_is_sequence(self):
        assert _annotation_is_sequence(list) is True
        assert _annotation_is_sequence(tuple) is True
        assert _annotation_is_sequence(set) is True
        assert _annotation_is_sequence(str) is False
        assert _annotation_is_sequence(bytes) is False
        assert _annotation_is_sequence(int) is False

    def test_annotation_is_complex(self):
        assert _annotation_is_complex(SampleModel) is True
        assert _annotation_is_complex(dict) is True
        assert _annotation_is_complex(UploadFile) is True
        assert _annotation_is_complex(list) is True
        assert _annotation_is_complex(str) is False
        assert _annotation_is_complex(int) is False


class TestErrorFunctions:
    def test_regenerate_error_with_loc(self):
        errors = [{"type": "missing", "loc": ("field",), "msg": "field required"}]
        loc_prefix = ("body",)
        
        result = _regenerate_error_with_loc(errors=errors, loc_prefix=loc_prefix)
        
        assert len(result) == 1
        assert result[0]["loc"] == ("body", "field")
        assert result[0]["type"] == "missing"

    def test_regenerate_error_with_empty_loc(self):
        errors = [{"type": "missing", "msg": "field required"}]
        loc_prefix = ("body",)
        
        result = _regenerate_error_with_loc(errors=errors, loc_prefix=loc_prefix)
        
        assert len(result) == 1
        assert result[0]["loc"] == ("body",)

    def test_normalize_errors_basic(self):
        errors = [{"type": "missing", "loc": ("field",), "msg": "field required"}]
        result = _normalize_errors(errors)
        assert result == errors


class TestCompatibilityEdgeCases:
    def test_none_annotations(self):
        assert field_annotation_is_scalar(None) is True
        assert field_annotation_is_complex(None) is False
        assert field_annotation_is_sequence(None) is False

    def test_nested_union_types(self):
        nested_union = Union[str, Union[int, float]]
        assert field_annotation_is_scalar(nested_union) is True

    def test_complex_nested_sequences(self):
        complex_sequence = List[Dict[str, Union[str, int]]]
        assert field_annotation_is_sequence(complex_sequence) is True
        assert field_annotation_is_complex(complex_sequence) is True
        assert field_annotation_is_scalar_sequence(complex_sequence) is False
