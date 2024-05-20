from typing import List

from pydantic import Field

from openagi.actions.base import BaseAction


class MemoryRagAction(BaseAction):
    """RAG on Previous Observation"""

    name: str = Field(default="MemoryRagAction", description="Name of the action.")
    description: str = Field(
        default="Action class to get all the results from the previous tasks for the current objetive",
        description="Action class to get all the results from the previous tasks for the current objetive. This action is responsible to reading and not writing. Writing is done by default for every task.",
    )

    query: List[str] = Field(
        ...,
        description="List of queries to run to retrieve the data from the results of previous tasks. Returns an Array of the results.",
    )
    max_results: int = Field(
        default=10, description="Max results to be used by querying the memory."
    )

    def execute(self):
        if not isinstance(self.query, list):
            self.query = [self.query]
        resp = self.memory.search(query=self.query, n_results=self.max_results or 10)
        print(f"MEMORY DATA  -  {resp}")
        return resp