import asyncio
import logging
from typing import Dict, Set, Optional, List
from at_common_workflow.types.meta import TaskExecutionInfo, TaskStatusCallback, TaskStatus
from at_common_workflow.core.task import Task
from at_common_workflow.core.context import Context

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    @staticmethod
    async def _handle_status_callback(
        status_callback: TaskStatusCallback,
        task_name: str,
        status: TaskStatus,
        info: dict
    ) -> None:
        """Helper method to handle status callback execution."""
        if status_callback:
            await asyncio.get_event_loop().run_in_executor(
                None,
                status_callback,
                task_name,
                status,
                info
            )

    @staticmethod
    async def execute_workflow(
        workflow_name: str,
        tasks: list[Task],
        task_execution_info: Dict[Task, TaskExecutionInfo],
        reverse_dependency_graph: Dict[Task, set],
        dependency_graph: Dict[Task, set],
        ready_tasks: asyncio.Queue,
        completed_tasks: asyncio.Queue,
        context: Context,
        status_callback: Optional[TaskStatusCallback] = None
    ) -> None:
        running_tasks: Set[asyncio.Task] = set()
        completed_count = 0
        total_tasks = len(tasks)

        try:
            while completed_count < total_tasks:
                # Start new ready tasks
                while not ready_tasks.empty():
                    task = await ready_tasks.get()
                    info = task_execution_info[task]
                    info.status = TaskStatus.RUNNING
                    info.start_time = asyncio.get_running_loop().time()
                    
                    await WorkflowExecutor._handle_status_callback(
                        status_callback,
                        task.name,
                        TaskStatus.RUNNING,
                        {"start_time": info.start_time}
                    )
                    
                    running_tasks.add(asyncio.create_task(
                        WorkflowExecutor.execute_task(task, info, context, completed_tasks, status_callback)
                    ))

                if not running_tasks:
                    continue

                done, running_tasks = await asyncio.wait(
                    running_tasks, 
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for task_future in done:
                    try:
                        await task_future
                        completed_task = await completed_tasks.get()
                        completed_count += 1
                        
                        new_ready_tasks = WorkflowExecutor.get_ready_tasks(
                            completed_task,
                            reverse_dependency_graph,
                            dependency_graph,
                            task_execution_info
                        )
                        for new_task in new_ready_tasks:
                            await ready_tasks.put(new_task)
                        
                    except Exception as e:
                        logger.error(f"Task execution failed: {str(e)}", exc_info=True)
                        raise RuntimeError(f"Task execution failed: {str(e)}") from e

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}", exc_info=True)
            raise
        finally:
            for task in running_tasks:
                task.cancel()
            if running_tasks:
                await asyncio.gather(*running_tasks, return_exceptions=True)

    @staticmethod
    async def execute_task(
        task: Task,
        info: TaskExecutionInfo,
        context: Context,
        completed_tasks: asyncio.Queue,
        status_callback: Optional[TaskStatusCallback] = None
    ) -> None:
        try:
            await task.execute(context)
            info.end_time = asyncio.get_running_loop().time()
            info.status = TaskStatus.COMPLETED
            
            callback_info = {
                "start_time": info.start_time,
                "end_time": info.end_time,
                "duration": info.end_time - info.start_time
            }
            
            await WorkflowExecutor._handle_status_callback(
                status_callback,
                task.name,
                TaskStatus.COMPLETED,
                callback_info
            )
                
        except Exception as e:
            info.status = TaskStatus.FAILED
            info.error = e
            info.end_time = asyncio.get_running_loop().time()
            
            callback_info = {
                "start_time": info.start_time,
                "end_time": info.end_time,
                "duration": info.end_time - info.start_time,
                "error": str(e)
            }
            
            await WorkflowExecutor._handle_status_callback(
                status_callback,
                task.name,
                TaskStatus.FAILED,
                callback_info
            )
            raise
        finally:
            await completed_tasks.put(task)

    @staticmethod
    def get_ready_tasks(
        completed_task: Task,
        reverse_dependency_graph: Dict[Task, Set[Task]],
        dependency_graph: Dict[Task, Set[Task]],
        task_execution_info: Dict[Task, TaskExecutionInfo]
    ) -> List[Task]:
        """Get tasks that are ready to execute after a task completes."""
        ready_tasks = []
        for dependent_task in reverse_dependency_graph.get(completed_task, set()):
            # Check if all dependencies are completed
            all_deps_completed = all(
                task_execution_info[dep].status == TaskStatus.COMPLETED
                for dep in dependency_graph[dependent_task]
            )
            if all_deps_completed:
                task_execution_info[dependent_task].dependencies_met = True
                ready_tasks.append(dependent_task)
        return ready_tasks