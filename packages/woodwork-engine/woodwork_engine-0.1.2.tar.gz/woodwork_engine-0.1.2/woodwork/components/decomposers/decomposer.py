from abc import ABC, abstractmethod
import json

from woodwork.helper_functions import print_debug, get_optional
from woodwork.components.component import component
from woodwork.components.knowledge_bases.graph_databases.neo4j import neo4j


class decomposer(component, ABC):
    def __init__(self, name, tools, output, **config):
        super().__init__(name, "decomposer")
        print_debug("Creating the decomposer...")

        self._tools = tools
        self._output = output
        self._cache = None
        api_key = get_optional(config, "api_key")

        if "cache" in config:
            if config["cache"]:
                # Initialise neo4j cache
                self._cache_mode = True

                if api_key is None:
                    exit()

                self._cache = neo4j(
                    "decomposer_cache",
                    **{
                        "uri": "bolt://localhost:7687",
                        "user": "neo4j",
                        "password": "testpassword",
                        "api_key": api_key,
                    },
                )
                self._cache.init_vector_index("embeddings", "Prompt", "embedding")
        else:
            self._cache_mode = False

    @abstractmethod
    def input(self, query):
        """Given a query, return the JSON array denoting the actions to take, passed to the task master."""
        pass

    def _cache_actions(self, prompt: str, instructions: list[any]):
        """Add the actions to the graph if they aren't already present, as a chain."""
        # Check to see if the action has been cached
        if self._cache_search_actions(prompt)["score"] > 0.95:
            print_debug("Similar prompts have already been cached.")
            return

        # Instructions must have at least one instruction
        if len(instructions) == 0:
            return

        # Generate the database query
        query = f'MERGE (:Prompt {{value: "{prompt}"}})'

        for instruction in instructions:
            query += f'-[:NEXT]->(:Action {{value: "{instruction}"}})'

        # Execute query
        self._cache.run(query)

        # Add the vector embedding for the prompt
        self._cache.embed("Prompt", "value")
        return

    def _cache_search_actions(self, prompt: str):
        similar_prompts = self._cache.similarity_search(prompt, "Prompt", "value")

        if len(similar_prompts) == 0:
            return {"prompt": "", "actions": [], "score": 0}

        print_debug(f"[SIMILAR PROMPTS] {similar_prompts}")

        best_prompt = similar_prompts[0]["value"]
        score = similar_prompts[0]["score"]

        actions = self._cache.run(f"""MATCH (p:Prompt)
                WHERE elementId(p) = \"{similar_prompts[0]["nodeID"]}\"
                WITH p
                MATCH path=(p)-[NEXT*]-(a:Action)
                RETURN a AS result""")

        actions = list(map(lambda x: json.loads(x["result"]["value"].replace("'", '"')), actions))

        return {"prompt": best_prompt, "actions": actions, "score": score}
