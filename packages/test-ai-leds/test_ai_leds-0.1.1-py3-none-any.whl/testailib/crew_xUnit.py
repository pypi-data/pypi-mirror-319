from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, DirectoryReadTool
from typing import Dict, List
from .utils import (
    init_task,
    init_agent,
    init_llm, 
    get_yaml_config,
)
from concurrent.futures import ThreadPoolExecutor
from .extract_endpoints import extract_endpoints
import os
from pathlib import Path
from dotenv import load_dotenv


llm_low_temp: LLM = init_llm()

def get_configs():
    config_path = Path(__file__).parent / 'config'
    yaml_config = get_yaml_config(base_path=config_path, files=["agents", "tasks", "output_examples"])
    agents_config = yaml_config["agents"]
    tasks_config = yaml_config["tasks"]
    outputs_examples = yaml_config["output_examples"]
    return agents_config, tasks_config, outputs_examples

def crew_xunit_debate(feature: str, strings: Dict[str, str]) -> str:
    
    agents_dict: Dict[str, str] = strings["agents"]
    tasks_dict: Dict[str, str] = strings["tasks"]
    
    tasks: List[Task] = []
    agents: List[Agent] = []

    gemini_llm: LLM = init_llm(temp=0.2)

    csharp_xunit_writer_agent: Agent = init_agent(
        agents_dict["csharp_xunit_writer"],
        gemini_llm
    )

    tasks_dict["xunit_code_proposal"]["description"] = tasks_dict["xunit_code_proposal"]["description"].format(feature=feature)
    xunit_code_proposal: Task = init_task(tasks_dict["xunit_code_proposal"], agent=csharp_xunit_writer_agent)
    
    agents.append(csharp_xunit_writer_agent)
    tasks.append(xunit_code_proposal)

    for i in range(1,4):
        xunit_solution_discussion_agent: Agent = init_agent(agents_dict["xunit_solution_discussion"], gemini_llm)

        tasks_dict["debate"]["description"] = tasks_dict["debate"]["description"].format(feature=feature)
        debate: Task = init_task(tasks_dict["debate"], agent=xunit_solution_discussion_agent)

        agents.append(xunit_solution_discussion_agent)
        tasks.append(debate)
    
    result_analysis_manager_agent: Agent = init_agent(agents_dict["result_analysis_manager"], llm=gemini_llm)

    tasks_dict["manager_xunit_task"]["description"] = tasks_dict["manager_xunit_task"]["description"].format(feature=feature)
    manager_xunit_task: Task = init_task(
        tasks_dict["manager_xunit_task"],
        output_file=f"modalidade_bolsa_crew.cs",
        agent=result_analysis_manager_agent,
        context=[tasks[-1]],
    )

    crew: Crew = Crew(
        agents=agents + [result_analysis_manager_agent],
        tasks=tasks + [manager_xunit_task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff().raw

def info_gatherer_crew(feature: str, swagger_path: str, dto_source: str) -> tuple[str, str]:
    agents_config, tasks_config, output_examples = get_configs()

    endpoints = extract_endpoints(swagger_path)

    crew_agents: dict[str, str] = agents_config["info_gatherer_crew"]
    crew_tasks: dict[str, str] = tasks_config["info_gatherer_tasks"]

    crew_tasks["api_url_find"]["description"] = crew_tasks["api_url_find"]["description"].format(feature=feature, api_endpoints=endpoints)
    crew_tasks["dto_file_find"]["description"] = crew_tasks["dto_file_find"]["description"].format(feature=feature, dto_source=dto_source)

    #api find
    agent_api_finder = init_agent(
        config=crew_agents["agent_api_finder"],
        llm=llm_low_temp,
        tools=[FileReadTool()],
    )
    api_url_find = init_task(
        config=crew_tasks["api_url_find"],
        agent=agent_api_finder,
    )
    #

    #dto find
    agent_file_searcher = init_agent(
        config=crew_agents["agent_file_searcher"],
        llm=llm_low_temp,
        tools=[DirectoryReadTool(), FileReadTool()]
    )
    dto_file_find = init_task(
        config=crew_tasks["dto_file_find"],
        agent=agent_file_searcher,
    )
    #

    crew = Crew(
        agents=[agent_api_finder, agent_file_searcher],
        tasks=[dto_file_find, api_url_find],
        verbose=False,
        process=Process.sequential
    )

    crew.kickoff()

    return dto_file_find.output.raw, api_url_find.output.raw

def crew_xunit_generation(feature: str, api_url: str, dto_code: str) -> Crew:
    gemini_llm: LLM = init_llm(temp=0.2)
    agents_config, tasks_config, outputs_examples = get_configs()
    
    crew_agents: dict[str, str] = agents_config["xunit_crew"]
    crew_tasks: dict[str, str] = tasks_config["xunit_tasks"]

    ###
    #bind das features e concantenacao com o output de exemplo
    crew_tasks["xunit_write"]["description"] = \
        crew_tasks["xunit_write"]["description"] \
        .format(feature, dto_code, api_url) + \
        outputs_examples[crew_tasks["xunit_write"]["output_example"]]

    crew_tasks["xunit_review"]["description"] = \
        crew_tasks["xunit_review"]["description"] \
        .format(feature) + \
        outputs_examples[crew_tasks["xunit_review"]["output_example"]]
    ###
    
    #write xunit
    xunit_writer: Agent = init_agent(
        config=crew_agents["xunit_writer"],
        llm=gemini_llm
        )
    xunit_write: Task = init_task(
        config=crew_tasks["xunit_write"],
        agent=xunit_writer
        )

    #xunit review
    xunit_reviewer: Agent = init_agent(
        config=crew_agents["xunit_reviewer"],
        llm=gemini_llm
    )
    xunit_review: Task = init_task(
        config=crew_tasks["xunit_review"],
        agent=xunit_reviewer,
        context=[xunit_write],
        )
    

    return Crew(
        agents=[xunit_writer, xunit_reviewer],
        tasks=[xunit_write, xunit_review],
        output_log_file="crew_log.txt",
        process=Process.sequential,
        verbose=False
        )

def manager_crew(reviews: tuple[str]) -> Crew:
    agents_config, tasks_config, outputs_examples = get_configs()

    crew_agents: dict[str, str] = agents_config["xunit_crew"]
    crew_tasks : dict[str, str] = tasks_config["xunit_tasks"]

    #bind da feature e output example
    crew_tasks["manager_xunit_task"]["description"] = \
        crew_tasks["manager_xunit_task"]["description"].format(reviews[0], reviews[1], reviews[2]) + \
        outputs_examples[crew_tasks["manager_xunit_task"]["output_example"]]
    #

    #manager
    manager: Agent = init_agent(
        config=crew_agents["result_analysis_manager"],
        llm=llm_low_temp
    )
    manager_task: Task = init_task(
        config=crew_tasks["manager_xunit_task"],
        agent=manager,
        output_file="xUnit/codigo.cs"
    )
    #

    return Crew(
        agents=[manager],
        tasks=[manager_task],
        process=Process.sequential,
        verbose=False
    )

def xunit_generation(feature: str, swagger_path: str, dto_source: str) -> str:
    dto_code, api_url = info_gatherer_crew(feature, swagger_path, dto_source)
    crew_xunit: Crew = crew_xunit_generation(feature, api_url, dto_code)
    with ThreadPoolExecutor() as executor:
        runs = [executor.submit(crew_xunit.kickoff) for _ in range(3)]
        results = [run.result() for run in runs]
    print(manager_crew(results).kickoff().raw)
