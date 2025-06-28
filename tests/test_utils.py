import pytest
from fastapi import FastAPI
from fastapi.utils import (
    is_body_allowed_for_status_code,
    get_path_param_names,
    create_model_field,
    create_cloned_field,
    generate_unique_id,
    deep_dict_update,
    get_value_or_default,
)
from fastapi.datastructures import DefaultPlaceholder
from fastapi.routing import APIRoute
from pydantic import BaseModel
from tests.utils import needs_pydanticv1, needs_pydanticv2


class TestIsBodyAllowedForStatusCode:
    def test_none_status_code(self):
        assert is_body_allowed_for_status_code(None) is True

    def test_default_status_code(self):
        assert is_body_allowed_for_status_code("default") is True

    def test_pattern_status_codes(self):
        for pattern in ["1XX", "2XX", "3XX", "4XX", "5XX"]:
            assert is_body_allowed_for_status_code(pattern) is True

    def test_success_status_codes(self):
        for code in [200, 201, 202, 203]:
            assert is_body_allowed_for_status_code(code) is True

    def test_no_body_status_codes(self):
        for code in [204, 205, 304]:
            assert is_body_allowed_for_status_code(code) is False

    def test_informational_status_codes(self):
        for code in [100, 101, 102]:
            assert is_body_allowed_for_status_code(code) is False

    def test_string_status_codes(self):
        assert is_body_allowed_for_status_code("200") is True
        assert is_body_allowed_for_status_code("204") is False


class TestGetPathParamNames:
    def test_no_params(self):
        assert get_path_param_names("/users") == set()

    def test_single_param(self):
        assert get_path_param_names("/users/{user_id}") == {"user_id"}

    def test_multiple_params(self):
        assert get_path_param_names("/users/{user_id}/posts/{post_id}") == {"user_id", "post_id"}

    def test_complex_params(self):
        assert get_path_param_names("/api/v1/{version}/users/{user_id:int}") == {"version", "user_id:int"}


class TestCreateModelField:
    def test_basic_field_creation(self):
        field = create_model_field("test_field", str, default="default_value")
        assert field.name == "test_field"
        assert field.type_ == str

    def test_required_field(self):
        field = create_model_field("required_field", int, required=True)
        assert field.required is True

    def test_field_with_alias(self):
        field = create_model_field("field_name", str, alias="fieldAlias")
        assert field.alias == "fieldAlias"

    def test_field_creation_with_none_type(self):
        field = create_model_field("none_field", type(None))
        assert field.name == "none_field"


class TestCreateClonedField:
    @needs_pydanticv2
    def test_clone_field_pydantic_v2(self):
        original_field = create_model_field("original", str, default="test")
        cloned_field = create_cloned_field(original_field)
        assert cloned_field.name == original_field.name
        assert cloned_field.type_ == original_field.type_

    @needs_pydanticv1
    def test_clone_field_pydantic_v1(self):
        original_field = create_model_field("original", str, default="test")
        cloned_field = create_cloned_field(original_field)
        assert cloned_field.name == original_field.name
        assert cloned_field.type_ == original_field.type_


class TestDeepDictUpdate:
    def test_simple_update(self):
        main_dict = {"a": 1, "b": 2}
        update_dict = {"c": 3}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"a": 1, "b": 2, "c": 3}

    def test_nested_dict_update(self):
        main_dict = {"a": {"x": 1, "y": 2}, "b": 3}
        update_dict = {"a": {"z": 3}, "c": 4}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"a": {"x": 1, "y": 2, "z": 3}, "b": 3, "c": 4}

    def test_list_concatenation(self):
        main_dict = {"items": [1, 2]}
        update_dict = {"items": [3, 4]}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"items": [1, 2, 3, 4]}

    def test_value_replacement(self):
        main_dict = {"a": 1}
        update_dict = {"a": 2}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"a": 2}

    def test_empty_dicts(self):
        main_dict = {}
        update_dict = {"a": 1}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"a": 1}

    def test_none_values(self):
        main_dict = {"a": None}
        update_dict = {"a": "value"}
        deep_dict_update(main_dict, update_dict)
        assert main_dict == {"a": "value"}


class TestGetValueOrDefault:
    def test_first_non_default_returned(self):
        placeholder = DefaultPlaceholder(value="default")
        result = get_value_or_default(placeholder, "value1", "value2")
        assert result == "value1"

    def test_all_defaults_returns_first(self):
        placeholder1 = DefaultPlaceholder(value="default1")
        placeholder2 = DefaultPlaceholder(value="default2")
        result = get_value_or_default(placeholder1, placeholder2)
        assert result == placeholder1

    def test_single_value(self):
        result = get_value_or_default("single_value")
        assert result == "single_value"

    def test_no_values(self):
        result = get_value_or_default("first_value")
        assert result == "first_value"

    def test_mixed_values(self):
        placeholder = DefaultPlaceholder(value="default")
        result = get_value_or_default("first", placeholder, "third")
        assert result == "first"


class TestGenerateUniqueId:
    def test_basic_route_id(self):
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint():
            return {"test": "value"}
        
        route = app.routes[0]
        unique_id = generate_unique_id(route)
        assert isinstance(unique_id, str)
        assert len(unique_id) > 0

    def test_route_with_path_params(self):
        app = FastAPI()
        
        @app.get("/users/{user_id}")
        def get_user(user_id: int):
            return {"user_id": user_id}
        
        route = app.routes[0]
        unique_id = generate_unique_id(route)
        assert isinstance(unique_id, str)
        assert len(unique_id) > 0

    def test_different_methods_different_ids(self):
        app = FastAPI()
        
        @app.get("/test")
        def get_test():
            return {"method": "GET"}
        
        @app.post("/test")
        def post_test():
            return {"method": "POST"}
        
        get_route = app.routes[0]
        post_route = app.routes[1]
        
        get_id = generate_unique_id(get_route)
        post_id = generate_unique_id(post_route)
        
        assert get_id != post_id
