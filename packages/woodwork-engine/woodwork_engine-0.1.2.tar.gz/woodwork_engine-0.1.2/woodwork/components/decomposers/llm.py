from woodwork.helper_functions import print_debug, format_kwargs
from woodwork.components.decomposers.decomposer import decomposer

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json


class llm(decomposer):
    def __init__(self, name, api_key, **config):
        format_kwargs(config, api_key=api_key)
        super().__init__(name, **config)
        print_debug("Initialising decomposer...")

        self.__llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key,
        )

        # self.__retriever = None
        # if "knowledge_base" in config:
        #     self.__retriever = config["knowledge_base"].retriever

    def __clean(self, x):
        start_index = -1
        end_index = -1

        for i in range(len(x) - 1):
            if x[i] == "[":
                start_index = i
                break

        for i in range(len(x) - 1, 0, -1):
            if x[i] == "]":
                end_index = i
                break

        if start_index == -1:
            return x

        try:
            return json.loads(x[start_index : end_index + 1 :])
        except:
            print("Couldn't load array as JSON")
            print(x[start_index : end_index + 1 :])
            return x

    def input(self, query):
        # Search cache for similar results
        if self._cache_mode:
            closest_query = self._cache_search_actions(query)
            if closest_query["score"] > 0.95:
                print_debug("Cache hit!")
                return self._output.execute(closest_query["actions"])

        tool_documentation = ""
        for obj in self._tools:
            tool_documentation += f"tool name: {obj.name}\ntool type: {obj.type}\n{obj.description}\n\n\n"

        print_debug(f"[DOCUMENTATION]:\n{tool_documentation}")
        system_prompt = (
            "Given the following tools and their descriptions:\n"
            "{tools} "
            "Answer the user's prompt, returning only the necessary action plan "
            "to carry out the steps to solving the user's prompt. "
            "If you do not have necessary tools, say so."
            "Structure your steps in the following schema: "
            '[{{{{"tool": tool, "action": prompt, function or endpoint, "inputs": {{{{variable: value}}}}, "output": value}}}}, ...]'
            "Format this JSON into an array of steps, returing only this array. "
            "Include only these keys in the JSON object, no others. "
            "Specify only the function or endpoint name as an action when they are used, do not include them as a function key. "
            "If you do not have the necessary information, ask for the required information. "
            "Always specify an output variable. "
        ).format(tools=tool_documentation)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        chain = prompt | self.__llm
        result = chain.invoke({"input": query}).content

        print_debug(f"[RESULT] {result}")

        # Clean output as JSON
        result = self.__clean(result)

        print_debug(f"[RESULT] {result}")

        if isinstance(result, str):
            return result

        # Cache instructions
        if self._cache_mode:
            self._cache_actions(query, result)

        # Send to task_master
        return self._output.execute(result)
