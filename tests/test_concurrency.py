import pytest
from contextlib import contextmanager
from fastapi.concurrency import contextmanager_in_threadpool


class TestContextManagerInThreadpool:
    @pytest.mark.anyio
    async def test_successful_context_manager(self):
        @contextmanager
        def test_cm():
            yield "test_value"
        
        async with contextmanager_in_threadpool(test_cm()) as value:
            assert value == "test_value"

    @pytest.mark.anyio
    async def test_context_manager_with_exception_in_body(self):
        @contextmanager
        def test_cm():
            try:
                yield "test_value"
            except ValueError:
                raise
        
        with pytest.raises(ValueError):
            async with contextmanager_in_threadpool(test_cm()) as value:
                assert value == "test_value"
                raise ValueError("Test exception")

    @pytest.mark.anyio
    async def test_context_manager_exit_handling(self):
        exit_called = False
        
        @contextmanager
        def tracking_cm():
            nonlocal exit_called
            try:
                yield "test_value"
            finally:
                exit_called = True
        
        async with contextmanager_in_threadpool(tracking_cm()) as value:
            assert value == "test_value"
        
        assert exit_called is True

    @pytest.mark.anyio
    async def test_context_manager_with_enter_exception(self):
        @contextmanager
        def failing_enter_cm():
            raise RuntimeError("Enter failed")
            yield "never_reached"
        
        with pytest.raises(RuntimeError, match="Enter failed"):
            async with contextmanager_in_threadpool(failing_enter_cm()):
                pass

    @pytest.mark.anyio
    async def test_context_manager_with_exit_exception(self):
        @contextmanager
        def failing_exit_cm():
            try:
                yield "test_value"
            finally:
                raise RuntimeError("Exit failed")
        
        with pytest.raises(RuntimeError, match="Exit failed"):
            async with contextmanager_in_threadpool(failing_exit_cm()) as value:
                assert value == "test_value"

    @pytest.mark.anyio
    async def test_context_manager_suppresses_exception(self):
        @contextmanager
        def suppressing_cm():
            try:
                yield "test_value"
            except ValueError:
                pass
        
        async with contextmanager_in_threadpool(suppressing_cm()) as value:
            assert value == "test_value"
            raise ValueError("This should be suppressed")

    @pytest.mark.anyio
    async def test_context_manager_with_complex_state(self):
        state = {"entered": False, "exited": False, "value": None}
        
        @contextmanager
        def stateful_cm():
            state["entered"] = True
            state["value"] = "context_value"
            try:
                yield state["value"]
            finally:
                state["exited"] = True
        
        async with contextmanager_in_threadpool(stateful_cm()) as value:
            assert state["entered"] is True
            assert state["exited"] is False
            assert value == "context_value"
        
        assert state["exited"] is True
