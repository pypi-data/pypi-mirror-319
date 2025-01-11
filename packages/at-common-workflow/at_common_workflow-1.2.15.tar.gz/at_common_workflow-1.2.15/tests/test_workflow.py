import pytest
import asyncio
from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import Task
from at_common_workflow.types.meta import MetaWorkflow, TaskStatus
from typing import Dict, Any

# Test fixtures
async def task1_func(*, x: int) -> int:
    return x + 1

async def task2_func(y: int) -> int:
    return y * 2

async def task3_func(z: int) -> int:
    return z - 1

@pytest.fixture
def simple_task1():
    return Task(
        name="task1",
        description="Add 1",
        func=task1_func,
        fixed_args={},
        inputs={"task1_input": int},
        outputs={"output1": int},
        input_mappings={"task1_input": "x"},
        output_mappings={"output1": "ret"}
    )

@pytest.fixture
def simple_task2():
    return Task(
        name="task2",
        description="Multiply by 2",
        func=task2_func,
        fixed_args={},
        inputs={"input": int},
        outputs={"output2": int},
        input_mappings={"input": "y"},
        output_mappings={"output2": "ret"}
    )

@pytest.fixture
def simple_task3():
    return Task(
        name="task3",
        description="Subtract 1",
        func=task3_func,
        fixed_args={},
        inputs={"input": int},
        outputs={"output3": int},
        input_mappings={"input": "z"},
        output_mappings={"output3": "ret"}
    )

class TestWorkflow:
    # Test initialization
    def test_init_basic(self, simple_task1):
        workflow = Workflow(
            name="test_workflow",
            description="Test workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        assert workflow.name == "test_workflow"
        assert len(workflow.tasks) == 1

    def test_init_validation(self):
        with pytest.raises(ValueError):
            Workflow(
                name="",  # Empty name
                description="Test workflow",
                tasks=[],
                inputs={"input": int},
                outputs={"output": int}
            )

    # Test dependency management
    def test_dependency_detection(self, simple_task1, simple_task2):
        task2_modified = Task(
            name="task2",
            description="Multiply by 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )
        
        workflow = Workflow(
            name="dependency_test",
            description="Test dependencies",
            tasks=[simple_task1, task2_modified],
            inputs={"task1_input": int},
            outputs={"output2": int}
        )
        assert len(workflow._dependency_graph) == 2

    def test_circular_dependency_detection(self):
        task1 = Task(
            name="circular1",
            description="Circular task 1",
            func=task1_func,
            fixed_args={},
            inputs={"output2": int},
            outputs={"output1": int},
            input_mappings={"output2": "x"},
            output_mappings={"output1": "ret"}
        )
        
        task2 = Task(
            name="circular2",
            description="Circular task 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )

        with pytest.raises(ValueError, match="Circular dependency detected"):
            Workflow(
                name="circular_workflow",
                description="Test circular dependencies",
                tasks=[task1, task2],
                inputs={"start": int},
                outputs={"output1": int}
            )

    # Test execution
    @pytest.mark.asyncio
    async def test_simple_execution(self, simple_task1):
        workflow = Workflow(
            name="simple_workflow",
            description="Simple workflow test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        result = await workflow.run({"task1_input": 5})
        assert result["output1"] == 6

    @pytest.mark.asyncio
    async def test_parallel_execution(self, simple_task1, simple_task2, simple_task3):
        workflow = Workflow(
            name="parallel_workflow",
            description="Parallel workflow test",
            tasks=[simple_task1, simple_task2, simple_task3],
            inputs={
                "task1_input": int,
                "input": int,
                "z": int
            },
            outputs={
                "output1": int,
                "output2": int,
                "output3": int
            }
        )
        
        result = await workflow.run({
            "task1_input": 5,
            "input": 10,
            "z": 15
        })
        
        assert result["output1"] == 6
        assert result["output2"] == 20
        assert result["output3"] == 9

    @pytest.mark.asyncio
    async def test_sequential_execution(self, simple_task1, simple_task2):
        task2_modified = Task(
            name="task2",
            description="Multiply by 2",
            func=task2_func,
            fixed_args={},
            inputs={"output1": int},
            outputs={"output2": int},
            input_mappings={"output1": "y"},
            output_mappings={"output2": "ret"}
        )
        
        workflow = Workflow(
            name="sequential_workflow",
            description="Sequential workflow test",
            tasks=[simple_task1, task2_modified],
            inputs={"task1_input": int},
            outputs={"output2": int}
        )
        
        result = await workflow.run({"task1_input": 5})
        assert result["output2"] == 12  # (5 + 1) * 2

    # Test error handling
    @pytest.mark.asyncio
    async def test_missing_input(self, simple_task1):
        workflow = Workflow(
            name="error_workflow",
            description="Error workflow test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        with pytest.raises(ValueError):
            await workflow.run({})

    @pytest.mark.asyncio
    async def test_task_execution_error(self):
        async def failing_task_func(dummy: int = 0) -> int:
            raise RuntimeError("Task failed")
        
        failing_task = Task(
            name="failing_task",
            description="Task that fails",
            func=failing_task_func,
            fixed_args={},
            inputs={"dummy": int},
            outputs={"output": int},
            input_mappings={"dummy": "dummy"},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="failing_workflow",
            description="Workflow with failing task",
            tasks=[failing_task],
            inputs={"dummy": int},
            outputs={"output": int}
        )
        
        with pytest.raises(RuntimeError):
            await workflow.run({"dummy": 0})

    # Test metadata conversion
    def test_to_meta(self, simple_task1):
        workflow = Workflow(
            name="meta_workflow",
            description="Metadata test workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        meta = workflow.to_meta()
        assert isinstance(meta, MetaWorkflow)
        assert meta.name == workflow.name
        assert meta.description == workflow.description

    def test_from_meta(self, simple_task1):
        original = Workflow(
            name="original_workflow",
            description="Original workflow",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        meta = original.to_meta()
        reconstructed = Workflow.from_meta(meta)
        
        assert reconstructed.name == original.name
        assert reconstructed.description == original.description
        assert len(reconstructed.tasks) == len(original.tasks)

    # Test cancellation
    @pytest.mark.asyncio
    async def test_workflow_cancellation(self):
        async def long_task_func(*args) -> int:
            try:
                await asyncio.sleep(10)
                return 42
            except asyncio.CancelledError:
                raise

        long_task = Task(
            name="long_task",
            description="Long-running task",
            func=long_task_func,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="cancellation_workflow",
            description="Cancellation test workflow",
            tasks=[long_task],
            inputs={},
            outputs={"output": int}
        )
        
        with pytest.raises((asyncio.CancelledError, TimeoutError)):
            async with asyncio.timeout(0.1):
                await workflow.run({})

    @pytest.mark.asyncio
    async def test_task_status_tracking(self, simple_task1):
        workflow = Workflow(
            name="status_workflow",
            description="Status tracking test",
            tasks=[simple_task1],
            inputs={"task1_input": int},
            outputs={"output1": int}
        )
        
        await workflow.run({"task1_input": 5})
        assert workflow._task_execution_info[simple_task1].status == TaskStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_invalid_output_type(self):
        async def bad_type_func(x: int) -> str:
            return "not an int"
        
        task = Task(
            name="bad_type",
            description="Returns wrong type",
            func=bad_type_func,
            fixed_args={},
            inputs={"input": int},
            outputs={"output": int},
            input_mappings={"input": "x"},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="type_error_workflow",
            description="Type error test",
            tasks=[task],
            inputs={"input": int},
            outputs={"output": int}
        )
        
        with pytest.raises(RuntimeError, match="Task execution failed: Output 'output' expected type <class 'int'>, got <class 'str'>"):
            await workflow.run({"input": 5})

    @pytest.mark.asyncio
    async def test_large_workflow(self):
        tasks = []
        for i in range(100):
            tasks.append(Task(
                name=f"task_{i}",
                description=f"Task {i}",
                func=lambda x: x,
                fixed_args={},
                inputs={"input": int},
                outputs={"output": int},
                input_mappings={"input": "x"},
                output_mappings={"output": "ret"}
            ))
        
        workflow = Workflow(
            name="large_workflow",
            description="Large workflow test",
            tasks=tasks,
            inputs={"input": int},
            outputs={"output": int}
        )
        
        result = await workflow.run({"input": 1})
        assert result["output"] == 1

    @pytest.mark.asyncio
    async def test_partial_workflow_completion(self):
        async def failing_task_func():
            raise RuntimeError("Task failed")
        
        # Create a Task instance for simple_task1
        task1 = Task(
            name="simple_task1",
            description="Simple task 1",
            func=task1_func,  # Changed from simple_task1 to task1_func
            fixed_args={},
            inputs={"task1_input": int},
            outputs={"output1": int},
            input_mappings={"task1_input": "x"},
            output_mappings={"output1": "ret"}
        )

        task2 = Task(
            name="failing_task",
            description="Failing task",
            func=failing_task_func,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )

        workflow = Workflow(
            name="partial_workflow",
            description="Partial completion test",
            tasks=[task1, task2],
            inputs={"task1_input": int},
            outputs={"output1": int, "output": int}
        )
        
        with pytest.raises(RuntimeError):
            await workflow.run({"task1_input": 5})
        
        # Check that task1 completed successfully
        assert workflow._task_execution_info[task1].status == TaskStatus.COMPLETED
        assert workflow._task_execution_info[task2].status == TaskStatus.FAILED

    @pytest.mark.asyncio
    async def test_workflow_timeout(self):
        async def slow_task():
            await asyncio.sleep(2)
            return 42
        
        task = Task(
            name="slow_task",
            description="Slow task",
            func=slow_task,
            fixed_args={},
            inputs={},
            outputs={"output": int},
            input_mappings={},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="timeout_workflow",
            description="Timeout test",
            tasks=[task],
            inputs={},
            outputs={"output": int}
        )
        
        with pytest.raises(asyncio.TimeoutError):
            async with asyncio.timeout(1):
                await workflow.run({})

    @pytest.mark.asyncio
    async def test_workflow_status_callback(self):
        callback_data = []
        
        def status_callback(task_name: str, status: TaskStatus, info: Dict[str, Any]):
            callback_data.append((task_name, status, info))
        
        async def simple_task(x: int) -> int:
            return x + 1
        
        task = Task(
            name="callback_task",
            description="Task with callback",
            func=simple_task,
            fixed_args={},
            inputs={"input": int},
            outputs={"output": int},
            input_mappings={"input": "x"},
            output_mappings={"output": "ret"}
        )
        
        workflow = Workflow(
            name="callback_test",
            description="Test callback functionality",
            tasks=[task],
            inputs={"input": int},
            outputs={"output": int},
            status_callback=status_callback
        )
        
        result = await workflow.run({"input": 5})
        
        # Verify callback was called for both RUNNING and COMPLETED states
        assert len(callback_data) == 2
        assert callback_data[0][0] == "callback_task"
        assert callback_data[0][1] == TaskStatus.RUNNING
        assert "start_time" in callback_data[0][2]
        
        assert callback_data[1][0] == "callback_task"
        assert callback_data[1][1] == TaskStatus.COMPLETED
        assert "start_time" in callback_data[1][2]
        assert "end_time" in callback_data[1][2]
        assert "duration" in callback_data[1][2]
        
        assert result["output"] == 6

    @pytest.mark.asyncio
    async def test_workflow_status_callback_failure(self):
        callback_data = []
        
        def status_callback(task_name: str, status: TaskStatus, info: Dict[str, Any]):
            callback_data.append((task_name, status, info))
        
        async def failing_task(x: int) -> int:
            raise ValueError("Task failed")
        
        task = Task(
            name="failing_task",
            description="Task that fails",
            func=failing_task,
            fixed_args={},
            inputs={"input": int},
            outputs={"ret": int},
            input_mappings={"input": "x"},
            output_mappings={"ret": "output"}
        )
        
        workflow = Workflow(
            name="failing_workflow",
            description="Test callback on failure",
            tasks=[task],
            inputs={"input": int},
            outputs={"output": int},
            status_callback=status_callback
        )
        
        with pytest.raises(RuntimeError):
            await workflow.run({"input": 5})
        
        # Verify callback was called for both RUNNING and FAILED states
        assert len(callback_data) == 2
        assert callback_data[0][0] == "failing_task"
        assert callback_data[0][1] == TaskStatus.RUNNING
        assert "start_time" in callback_data[0][2]
        
        assert callback_data[1][0] == "failing_task"
        assert callback_data[1][1] == TaskStatus.FAILED
        assert "start_time" in callback_data[1][2]
        assert "end_time" in callback_data[1][2]
        assert "duration" in callback_data[1][2]
        assert "error" in callback_data[1][2]
        assert "Task failed" in callback_data[1][2]["error"]

    @pytest.mark.asyncio
    async def test_workflow_status_callback_parallel_tasks(self):
        callback_data = []
        
        def status_callback(task_name: str, status: TaskStatus, info: Dict[str, Any]):
            callback_data.append((task_name, status, info))
        
        async def task_a(x: int) -> int:
            await asyncio.sleep(0.1)  # Small delay to ensure parallel execution
            return x + 1
        
        async def task_b(y: int) -> int:
            return y * 2
        
        task1 = Task(
            name="task_a",
            description="Task A",
            func=task_a,
            fixed_args={},
            inputs={"x": int},
            outputs={"out_a": int},
            input_mappings={"x": "x"},
            output_mappings={"out_a": "ret"}
        )
        
        task2 = Task(
            name="task_b",
            description="Task B",
            func=task_b,
            fixed_args={},
            inputs={"y": int},
            outputs={"out_b": int},
            input_mappings={"y": "y"},
            output_mappings={"out_b": "ret"}
        )
        
        workflow = Workflow(
            name="parallel_callback_test",
            description="Test callbacks with parallel tasks",
            tasks=[task1, task2],
            inputs={"x": int, "y": int},
            outputs={"out_a": int, "out_b": int},
            status_callback=status_callback
        )
        
        result = await workflow.run({"x": 5, "y": 3})
        
        # Verify results
        assert result["out_a"] == 6
        assert result["out_b"] == 6
        
        # Verify callbacks
        assert len(callback_data) == 4  # 2 tasks * 2 states (RUNNING, COMPLETED)
        
        # Group callbacks by task
        task_a_callbacks = [c for c in callback_data if c[0] == "task_a"]
        task_b_callbacks = [c for c in callback_data if c[0] == "task_b"]
        
        # Verify each task's callbacks
        for task_callbacks in [task_a_callbacks, task_b_callbacks]:
            assert len(task_callbacks) == 2
            running_cb = task_callbacks[0]
            completed_cb = task_callbacks[1]
            
            assert running_cb[1] == TaskStatus.RUNNING
            assert "start_time" in running_cb[2]
            
            assert completed_cb[1] == TaskStatus.COMPLETED
            assert "start_time" in completed_cb[2]
            assert "end_time" in completed_cb[2]
            assert "duration" in completed_cb[2]

    @pytest.mark.asyncio
    async def test_workflow_status_callback_sequential_tasks(self):
        callback_data = []
        
        def status_callback(task_name: str, status: TaskStatus, info: Dict[str, Any]):
            callback_data.append((task_name, status, info))
        
        async def first_task(x: int) -> int:
            return x + 1
        
        async def second_task(y: int) -> int:
            return y * 2
        
        task1 = Task(
            name="first",
            description="First task",
            func=first_task,
            fixed_args={},
            inputs={"input": int},
            outputs={"intermediate": int},
            input_mappings={"input": "x"},
            output_mappings={"intermediate": "ret"}
        )
        
        task2 = Task(
            name="second",
            description="Second task",
            func=second_task,
            fixed_args={},
            inputs={"intermediate": int},
            outputs={"final": int},
            input_mappings={"intermediate": "y"},
            output_mappings={"final": "ret"}
        )
        
        workflow = Workflow(
            name="sequential_callback_test",
            description="Test callbacks with sequential tasks",
            tasks=[task1, task2],
            inputs={"input": int},
            outputs={"final": int},
            status_callback=status_callback
        )
        
        result = await workflow.run({"input": 5})
        
        # Verify result
        assert result["final"] == 12  # (5 + 1) * 2
        
        # Verify callbacks
        assert len(callback_data) == 4  # 2 tasks * 2 states (RUNNING, COMPLETED)
        
        # Verify sequential execution through callback timestamps
        first_task_start = None
        first_task_end = None
        second_task_start = None
        
        for task_name, status, info in callback_data:
            if task_name == "first":
                if status == TaskStatus.RUNNING:
                    first_task_start = info["start_time"]
                elif status == TaskStatus.COMPLETED:
                    first_task_end = info["end_time"]
            elif task_name == "second" and status == TaskStatus.RUNNING:
                second_task_start = info["start_time"]
        
        # Verify sequential execution
        assert first_task_start < first_task_end
        assert first_task_end <= second_task_start

    @pytest.mark.asyncio
    async def test_workflow_status_callback_cancellation(self):
        callback_data = []
        
        def status_callback(task_name: str, status: TaskStatus, info: Dict[str, Any]):
            callback_data.append((task_name, status, info))
        
        async def long_running_task() -> int:
            try:
                await asyncio.sleep(10)
                return 42
            except asyncio.CancelledError:
                raise
        
        task = Task(
            name="long_task",
            description="Long running task",
            func=long_running_task,
            fixed_args={},
            inputs={},
            outputs={"result": int},
            input_mappings={},
            output_mappings={"result": "ret"}
        )
        
        workflow = Workflow(
            name="cancellation_callback_test",
            description="Test callbacks with task cancellation",
            tasks=[task],
            inputs={},
            outputs={"result": int},
            status_callback=status_callback
        )
        
        with pytest.raises((asyncio.CancelledError, TimeoutError)):
            async with asyncio.timeout(0.1):
                await workflow.run({})
        
        # Verify that we got at least the RUNNING status callback
        assert len(callback_data) >= 1
        assert callback_data[0][0] == "long_task"
        assert callback_data[0][1] == TaskStatus.RUNNING
        assert "start_time" in callback_data[0][2]