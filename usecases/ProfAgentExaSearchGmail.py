from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.azure import AzureChatOpenAIModel
from openagi.tools.integrations import ExaSearchTool, GmailSearchTool

if __name__ == "__main__":
    agent_names = ["RESEARCHER", "WRITER", "EMAILER", "GMAILER"]

    agent_list = [
        Agent(
            agentName=agent_names[0],  # name
            role="RESEARCHER",  # role
            goal="search for latest trends in COVID-19 and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool and keep it within context length",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent=[agent_names[1]],  # the consumer agent after executing task
            tools_list=[ExaSearchTool],
        ),
        Agent(
            agentName=agent_names[1],
            role="SUMMARISER",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent=[agent_names[2]],
        ),
        Agent(
            agentName=agent_names[2],
            role="EMAILER",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent=[agent_names[3]],
        ),
        Agent(
            agentName=agent_names[3],
            role="GMAILER",
            goal="Send the email using GmailSearchTool",
            backstory="Good in sending emails to the given context.",
            capability="llm_task_executor",
            task="send emails to the receipient tanish@aiplanet.com",
            output_consumer_agent=["HGI"],
            tools_list=[GmailSearchTool],
        ),
    ]
    config = AzureChatOpenAIModel.load_from_env_config()
    azure_chat_model = AzureChatOpenAIModel(config=config)
    kickOffAgents(agent_list, [agent_list[0]], llm=azure_chat_model)
