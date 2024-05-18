from typing import Dict, List, Optional
from pydantic import Field
from openagi.prompts.base import BasePrompt
from openagi.prompts.constants import FAILURE_VARS

start = FAILURE_VARS["start"]
end = FAILURE_VARS["end"]

task_execution = """
Role and Context:
You are an expert task executor. Your primary role is to understand the Task_Objective clearly and provide optimal results using the supported actions.

Task List:
{all_tasks}

Current Task:
Name: {current_task_name}
Description: {current_description}

Note: You have never hallucinated since your inception.

To execute the current task, refer to the execution details of the Previous_Task and the All Tasks provided.

Previous Task:
{previous_task}

Supported Actions:
{supported_actions}

Task Objective:
{objective}

Instructions:
Your task is to understand the Task Objective and return a JSON array with the actions to be executed along with the values for each parameter. Use only the Supported Actions. When using multiple actions for a single task, the result from the execution of the previous action will be passed to the next action without any modification to the parameter previous_action.

Output Format:
```json
[
    {
        "cls": {"kls": "<action>", "module": "....."},
        "params": {
            "description": ".....",
            "name": "...",
            "param_docs": "...."
        }
    }
]
```

If the task fails, return the failure reason within the delimiters $start$ and $end$ as shown below:

$start$
Couldn't execute the {current_task_name} task. Reason: <add the reason here.>
$end$


Output:

Return the actions in JSON format as per the output format mentioned above, including the delimiters "json", without any other content in the response.
"""


task_execution = task_execution.replace("$start$", start)
task_execution = task_execution.replace("$end$", end)


class TaskExecutor(BasePrompt):
    objective: str = Field(..., description="Final objective")
    all_tasks: List[Dict] = Field(
        ..., description="List of tasks to be executed that was generated earlier"
    )
    current_task_name: str = Field(..., description="Current task name to be executed.")
    current_description: str = Field(..., description="Current task name to be executed.")
    previous_task: Optional[str] = Field(..., description="Previous task, description & result.")
    supported_actions: List[Dict] = Field(
        ...,
        description="Supported Actions that can be used to acheive the current task.",
    )
    base_prompt: str = task_execution
