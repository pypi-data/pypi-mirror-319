# BUSINESS SCIENCE UNIVERSITY
# AI DATA SCIENCE TEAM
# ***
# * Agents: Data Cleaning Agent

# Libraries
from typing import TypedDict, Annotated, Sequence, Literal
import operator

from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage

from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.state import CompiledStateGraph

import os
import io
import pandas as pd

from ai_data_science_team.templates import(
    node_func_execute_agent_code_on_data, 
    node_func_human_review,
    node_func_fix_agent_code, 
    node_func_explain_agent_code, 
    create_coding_agent_graph
)
from ai_data_science_team.tools.parsers import PythonOutputParser
from ai_data_science_team.tools.regex import relocate_imports_inside_function, add_comments_to_top, format_agent_name
from ai_data_science_team.tools.metadata import get_dataframe_summary
from ai_data_science_team.tools.logging import log_ai_function

# Setup
AGENT_NAME = "data_cleaning_agent"
LOG_PATH = os.path.join(os.getcwd(), "logs/")



# Class
class DataCleaningAgent(CompiledStateGraph):
    
    def __init__(
        self, 
        model, 
        n_samples=30, 
        log=False, 
        log_path=None, 
        file_name="data_cleaner.py", 
        overwrite=True, 
        human_in_the_loop=False, 
        bypass_recommended_steps=False, 
        bypass_explain_code=False
    ):
        self._params = {
            "model": model,
            "n_samples": n_samples,
            "log": log,
            "log_path": log_path,
            "file_name": file_name,
            "overwrite": overwrite,
            "human_in_the_loop": human_in_the_loop,
            "bypass_recommended_steps": bypass_recommended_steps,
            "bypass_explain_code": bypass_explain_code,
        }
        self._compiled_graph = self._make_compiled_graph()
        self.response = None

    def _make_compiled_graph(self):
        self.response = None
        return make_data_cleaning_agent(**self._params)

    def update_params(self, **kwargs):
        """
        Update one or more parameters at once, then rebuild the compiled graph.
        e.g. agent.update_params(model=new_llm, n_samples=100)
        """
        self._params.update(kwargs)
        self._compiled_graph = self._make_compiled_graph()

    def __getattr__(self, name: str):
        """
        Delegate attribute access to `_compiled_graph` if `name` is not
        found in this instance. This 'inherits' methods from the compiled graph.
        """
        return getattr(self._compiled_graph, name)
    
    def ainvoke(self, user_instructions: str, data_raw: pd.DataFrame, max_retries=3, retry_count=0):
        """
        Cleans the provided dataset based on user instructions.

        Parameters:
            user_instructions (str): Instructions for data cleaning.
            data_raw (pd.DataFrame): The raw dataset to be cleaned.
            max_retries (int): Maximum retry attempts for cleaning.
            retry_count (int): Current retry attempt.

        Returns:
            None. The response is stored in the response attribute.
        """
        response = self.ainvoke({
            "user_instructions": user_instructions,
            "data_raw": data_raw.to_dict(),
            "max_retries": max_retries,
            "retry_count": retry_count,
        })
        self.response = response
        return None
    
    def invoke(self, user_instructions: str, data_raw: pd.DataFrame, max_retries=3, retry_count=0):
        """
        Cleans the provided dataset based on user instructions.

        Parameters:
            user_instructions (str): Instructions for data cleaning.
            data_raw (pd.DataFrame): The raw dataset to be cleaned.
            max_retries (int): Maximum retry attempts for cleaning.
            retry_count (int): Current retry attempt.

        Returns:
            None. The response is stored in the response attribute.
        """
        response = self.invoke({
            "user_instructions": user_instructions,
            "data_raw": data_raw.to_dict(),
            "max_retries": max_retries,
            "retry_count": retry_count,
        })
        self.response = response
        return None

    def explain_cleaning_steps(self):
        """
        Provides an explanation of the cleaning steps performed by the agent.

        Returns:
            str: Explanation of the cleaning steps.
        """
        messages = self.response.get("messages", [])
        return messages

    def get_log_summary(self):
        """
        Logs a summary of the agent's operations, if logging is enabled.
        """
        if self.response:
            if self.log: 
                log_details = f"Log Path: {self.response.get('data_cleaner_function_path')}"
                return log_details
    
    def get_state_keys(self):
        """
        Returns a list of keys that the state graph returns in a response.
        """
        return list(self.get_output_jsonschema()['properties'].keys())
    
    def get_state_properties(self):
        """
        Returns a list of keys that the state graph returns in a response.
        """
        return self.get_output_jsonschema()['properties']
    
    def get_data_cleaned(self):
        """
        Retrieves the cleaned data stored after running invoke or clean_data methods.
        """
        if self.response:
            return pd.DataFrame(self.response.get("data_cleaned"))
        
    def get_data_raw(self):
        """
        Retrieves the raw data.
        """
        if self.response:
            return pd.DataFrame(self.response.get("data_raw"))
    
    def get_data_cleaner_function(self):
        """
        Retrieves the agent's pipeline function.
        """
        if self.response:
            return self.response.get("data_cleaner_function")
        
    
    



# Agent

def make_data_cleaning_agent(
    model, 
    n_samples = 30, 
    log=False, 
    log_path=None, 
    file_name="data_cleaner.py",
    overwrite = True, 
    human_in_the_loop=False, 
    bypass_recommended_steps=False, 
    bypass_explain_code=False
):
    """
    Creates a data cleaning agent that can be run on a dataset. The agent can be used to clean a dataset in a variety of
    ways, such as removing columns with more than 40% missing values, imputing missing
    values with the mean of the column if the column is numeric, or imputing missing
    values with the mode of the column if the column is categorical.
    The agent takes in a dataset and some user instructions, and outputs a python
    function that can be used to clean the dataset. The agent also logs the code
    generated and any errors that occur.

    The agent is instructed to to perform the following data cleaning steps:

    - Removing columns if more than 40 percent of the data is missing
    - Imputing missing values with the mean of the column if the column is numeric
    - Imputing missing values with the mode of the column if the column is categorical
    - Converting columns to the correct data type
    - Removing duplicate rows
    - Removing rows with missing values
    - Removing rows with extreme outliers (3X the interquartile range)
    - User instructions can modify, add, or remove any of the above steps

    Parameters
    ----------
    model : langchain.llms.base.LLM
        The language model to use to generate code.
    n_samples : int, optional
        The number of samples to use when summarizing the dataset. Defaults to 30.
        If you get an error due to maximum tokens, try reducing this number.
        > "This model's maximum context length is 128000 tokens. However, your messages resulted in 333858 tokens. Please reduce the length of the messages."
    log : bool, optional
        Whether or not to log the code generated and any errors that occur.
        Defaults to False.
    log_path : str, optional
        The path to the directory where the log files should be stored. Defaults to
        "logs/".
    file_name : str, optional
        The name of the file to save the response to. Defaults to "data_cleaner.py".
    overwrite : bool, optional
        Whether or not to overwrite the log file if it already exists. If False, a unique file name will be created. 
        Defaults to True.
    human_in_the_loop : bool, optional
        Whether or not to use human in the loop. If True, adds an interput and human in the loop step that asks the user to review the data cleaning instructions. Defaults to False.
    bypass_recommended_steps : bool, optional
        Bypass the recommendation step, by default False
    bypass_explain_code : bool, optional
        Bypass the code explanation step, by default False.
        
    Examples
    -------
    ``` python
    import pandas as pd
    from langchain_openai import ChatOpenAI
    from ai_data_science_team.agents import data_cleaning_agent

    llm = ChatOpenAI(model = "gpt-4o-mini")

    data_cleaning_agent = make_data_cleaning_agent(llm)

    df = pd.read_csv("https://raw.githubusercontent.com/business-science/ai-data-science-team/refs/heads/master/data/churn_data.csv")

    response = data_cleaning_agent.invoke({
        "user_instructions": "Don't remove outliers when cleaning the data.",
        "data_raw": df.to_dict(),
        "max_retries":3, 
        "retry_count":0
    })

    pd.DataFrame(response['data_cleaned'])
    ```

    Returns
    -------
    app : langchain.graphs.CompiledStateGraph
        The data cleaning agent as a state graph.
    """
    llm = model
    
    # Setup Log Directory
    if log:
        if log_path is None:
            log_path = LOG_PATH
        if not os.path.exists(log_path):
            os.makedirs(log_path)    

    # Define GraphState for the router
    class GraphState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]
        user_instructions: str
        recommended_steps: str
        data_raw: dict
        data_cleaned: dict
        all_datasets_summary: str
        data_cleaner_function: str
        data_cleaner_function_path: str
        data_cleaner_function_name: str
        data_cleaner_error: str
        max_retries: int
        retry_count: int

    
    def recommend_cleaning_steps(state: GraphState):
        """
        Recommend a series of data cleaning steps based on the input data. 
        These recommended steps will be appended to the user_instructions.
        """
        print(format_agent_name(AGENT_NAME))
        print("    * RECOMMEND CLEANING STEPS")

        # Prompt to get recommended steps from the LLM
        recommend_steps_prompt = PromptTemplate(
            template="""
            You are a Data Cleaning Expert. Given the following information about the data, 
            recommend a series of numbered steps to take to clean and preprocess it. 
            The steps should be tailored to the data characteristics and should be helpful 
            for a data cleaning agent that will be implemented.
            
            General Steps:
            Things that should be considered in the data cleaning steps:
            
            * Removing columns if more than 40 percent of the data is missing
            * Imputing missing values with the mean of the column if the column is numeric
            * Imputing missing values with the mode of the column if the column is categorical
            * Converting columns to the correct data type
            * Removing duplicate rows
            * Removing rows with missing values
            * Removing rows with extreme outliers (3X the interquartile range)
            
            Custom Steps:
            * Analyze the data to determine if any additional data cleaning steps are needed.
            * Recommend steps that are specific to the data provided. Include why these steps are necessary or beneficial.
            * If no additional steps are needed, simply state that no additional steps are required.
            
            IMPORTANT:
            Make sure to take into account any additional user instructions that may add, remove or modify some of these steps. Include comments in your code to explain your reasoning for each step. Include comments if something is not done because a user requested. Include comments if something is done because a user requested.
            
            User instructions:
            {user_instructions}

            Previously Recommended Steps (if any):
            {recommended_steps}

            Below are summaries of all datasets provided:
            {all_datasets_summary}

            Return the steps as a bullet point list (no code, just the steps).
            
            Avoid these:
            1. Do not include steps to save files.
            2. Do not include unrelated user instructions that are not related to the data cleaning.
            """,
            input_variables=["user_instructions", "recommended_steps", "all_datasets_summary"]
        )

        data_raw = state.get("data_raw")
        df = pd.DataFrame.from_dict(data_raw)

        all_datasets_summary = get_dataframe_summary([df], n_sample=n_samples)
        
        all_datasets_summary_str = "\n\n".join(all_datasets_summary)

        steps_agent = recommend_steps_prompt | llm
        recommended_steps = steps_agent.invoke({
            "user_instructions": state.get("user_instructions"),
            "recommended_steps": state.get("recommended_steps"),
            "all_datasets_summary": all_datasets_summary_str
        }) 
        
        return {
            "recommended_steps": "\n\n# Recommended Data Cleaning Steps:\n" + recommended_steps.content.strip(),
            "all_datasets_summary": all_datasets_summary_str
        }
    
    def create_data_cleaner_code(state: GraphState):
        
        print("    * CREATE DATA CLEANER CODE")
        
        if bypass_recommended_steps:
            print(format_agent_name(AGENT_NAME))
            
            data_raw = state.get("data_raw")
            df = pd.DataFrame.from_dict(data_raw)

            all_datasets_summary = get_dataframe_summary([df], n_sample=n_samples)
            
            all_datasets_summary_str = "\n\n".join(all_datasets_summary)
        else:
            all_datasets_summary_str = state.get("all_datasets_summary")
        
        data_cleaning_prompt = PromptTemplate(
            template="""
            You are a Data Cleaning Agent. Your job is to create a data_cleaner() function that can be run on the data provided using the following recommended steps.
            
            Recommended Steps:
            {recommended_steps}
            
            You can use Pandas, Numpy, and Scikit Learn libraries to clean the data.
            
            Below are summaries of all datasets provided. Use this information about the data to help determine how to clean the data:

            {all_datasets_summary}
            
            Return Python code in ```python ``` format with a single function definition, data_cleaner(data_raw), that includes all imports inside the function. 
            
            Return code to provide the data cleaning function:
            
            def data_cleaner(data_raw):
                import pandas as pd
                import numpy as np
                ...
                return data_cleaned
            
            Best Practices and Error Preventions:
            
            Always ensure that when assigning the output of fit_transform() from SimpleImputer to a Pandas DataFrame column, you call .ravel() or flatten the array, because fit_transform() returns a 2D array while a DataFrame column is 1D.
            
            """,
            input_variables=["recommended_steps", "all_datasets_summary"]
        )

        data_cleaning_agent = data_cleaning_prompt | llm | PythonOutputParser()
        
        response = data_cleaning_agent.invoke({
            "recommended_steps": state.get("recommended_steps"),
            "all_datasets_summary": all_datasets_summary_str
        })
        
        response = relocate_imports_inside_function(response)
        response = add_comments_to_top(response, agent_name=AGENT_NAME)
        
        # For logging: store the code generated:
        file_path, file_name_2 = log_ai_function(
            response=response,
            file_name=file_name,
            log=log,
            log_path=log_path,
            overwrite=overwrite
        )
   
        return {
            "data_cleaner_function" : response,
            "data_cleaner_function_path": file_path,
            "data_cleaner_function_name": file_name_2,
            "all_datasets_summary": all_datasets_summary_str
        }
    
    def human_review(state: GraphState) -> Command[Literal["recommend_cleaning_steps", "create_data_cleaner_code"]]:
        return node_func_human_review(
            state=state,
            prompt_text="Is the following data cleaning instructions correct? (Answer 'yes' or provide modifications)\n{steps}",
            yes_goto="create_data_cleaner_code",
            no_goto="recommend_cleaning_steps",
            user_instructions_key="user_instructions",
            recommended_steps_key="recommended_steps"            
        )
    
    def execute_data_cleaner_code(state):
        return node_func_execute_agent_code_on_data(
            state=state,
            data_key="data_raw",
            result_key="data_cleaned",
            error_key="data_cleaner_error",
            code_snippet_key="data_cleaner_function",
            agent_function_name="data_cleaner",
            pre_processing=lambda data: pd.DataFrame.from_dict(data),
            post_processing=lambda df: df.to_dict() if isinstance(df, pd.DataFrame) else df,
            error_message_prefix="An error occurred during data cleaning: "
        )
        
    def fix_data_cleaner_code(state: GraphState):
        data_cleaner_prompt = """
        You are a Data Cleaning Agent. Your job is to create a data_cleaner() function that can be run on the data provided. The function is currently broken and needs to be fixed.
        
        Make sure to only return the function definition for data_cleaner().
        
        Return Python code in ```python``` format with a single function definition, data_cleaner(data_raw), that includes all imports inside the function.
        
        This is the broken code (please fix): 
        {code_snippet}

        Last Known Error:
        {error}
        """

        return node_func_fix_agent_code(
            state=state,
            code_snippet_key="data_cleaner_function",
            error_key="data_cleaner_error",
            llm=llm,  
            prompt_template=data_cleaner_prompt,
            agent_name=AGENT_NAME,
            log=log,
            file_path=state.get("data_cleaner_function_path"),
        )
    
    def explain_data_cleaner_code(state: GraphState):        
        return node_func_explain_agent_code(
            state=state,
            code_snippet_key="data_cleaner_function",
            result_key="messages",
            error_key="data_cleaner_error",
            llm=llm,  
            role=AGENT_NAME,
            explanation_prompt_template="""
            Explain the data cleaning steps that the data cleaning agent performed in this function. 
            Keep the summary succinct and to the point.\n\n# Data Cleaning Agent:\n\n{code}
            """,
            success_prefix="# Data Cleaning Agent:\n\n ",
            error_message="The Data Cleaning Agent encountered an error during data cleaning. Data could not be explained."
        )
        
    # Define the graph
    node_functions = {
        "recommend_cleaning_steps": recommend_cleaning_steps,
        "human_review": human_review,
        "create_data_cleaner_code": create_data_cleaner_code,
        "execute_data_cleaner_code": execute_data_cleaner_code,
        "fix_data_cleaner_code": fix_data_cleaner_code,
        "explain_data_cleaner_code": explain_data_cleaner_code
    }
    
    app = create_coding_agent_graph(
        GraphState=GraphState,
        node_functions=node_functions,
        recommended_steps_node_name="recommend_cleaning_steps",
        create_code_node_name="create_data_cleaner_code",
        execute_code_node_name="execute_data_cleaner_code",
        fix_code_node_name="fix_data_cleaner_code",
        explain_code_node_name="explain_data_cleaner_code",
        error_key="data_cleaner_error",
        human_in_the_loop=human_in_the_loop,  # or False
        human_review_node_name="human_review",
        checkpointer=MemorySaver() if human_in_the_loop else None,
        bypass_recommended_steps=bypass_recommended_steps,
        bypass_explain_code=bypass_explain_code,
    )
        
    return app



