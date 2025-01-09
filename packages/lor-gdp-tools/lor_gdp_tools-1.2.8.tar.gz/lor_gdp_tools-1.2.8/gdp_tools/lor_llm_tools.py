import pandas as pd
from openai import AzureOpenAI

class LORLargeLanguageModels:

    def __init__(self, api_key, azure_endpoint):
        """
        initalise the class with a specific api key and endpoint. 
        Contact the LOR Data Science team to access these.
        """
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint

        self.registered_models = [
            "gpt-4o-hi-rate",
            "gpt-4o-mini",
            "gpt-35-turbo-16k",
            "gpt35turbo",
            "gpt4-32k",
            "gpt4",
        ]

    def tell_me_about_the_models_that_are_available(self):
        """
        This function returns a pandas table with information about the models available.

        the numbers here were pulled from Chat GPT and checked, but may not be 100% accurate.

        Citations:
        https://openai.com/api/pricing/
        https://learn.microsoft.com/en-us/answers/questions/1327201/pricing-for-gpt-3-5-turbo-on-azure-is-not-updated
        https://myscale.com/blog/gpt4o-benchmark-comparative-analysis/
        https://docsbot.ai/models/compare/gpt-4o-mini/gpt-4o
        https://community.openai.com/t/gpt-4-turbo-and-gpt-4-o-benchmarks-released-they-do-well-compared-to-the-marketplace/744528
        """

        model_info = {
            "gpt-4o-hi-rate": {
                "token_rate_limit": 10000000,
                "request_rate_limit": 60000,
                "input_cost_per_1000_token": 0.002,
                "output_cost_per_1000_token": 0.008,
                "accuracy": 92,
            },
            "gpt-4o-mini": {
                "token_rate_limit": 100000000,
                "request_rate_limit": 1000000,
                "input_cost_per_1000_token": 0.00012,
                "output_cost_per_1000_token": 0.00048,
                "accuracy": 90,
            },
            "gpt-35-turbo-16k": {
                "token_rate_limit": 120000,
                "request_rate_limit": 720,
                "input_cost_per_1000_token": 0.0024,
                "output_cost_per_1000_token": 0.0032,
                "accuracy": 88,
            },
            "gpt35turbo": {
                "token_rate_limit": 120000,
                "request_rate_limit": 720,
                "input_cost_per_1000_token": 0.0012,
                "output_cost_per_1000_token": 0.0016,
                "accuracy": 87,
            },
            "gpt4-32k": {
                "token_rate_limit": 60000,
                "request_rate_limit": 360,
                "input_cost_per_1000_token": 0.048,
                "output_cost_per_1000_token": 0.096,
                "accuracy": 89,
            },
            "gpt4": {
                "token_rate_limit": 20000,
                "request_rate_limit": 120,
                "input_cost_per_1000_token": 0.024,
                "output_cost_per_1000_token": 0.048,
                "accuracy": 90,
            },
        }

        return pd.DataFrame.from_dict(model_info, orient="index")

    def llm_architecture(self, guidence: str, prompt: str, model_name: str):
        """
        Use chatgpt to generate an answer for a given prompt

        Note that this method only works for openai version 1.35 and less

        input:
        guidence = string (overivew of role and approach to the problem)
        prompt = string (be aware of the prompt length restrictions)

        Output:
        output = string, generated text
        """

        msgs = [
            {"role": "system", "content": guidence},
            {"role": "user", "content": prompt},
        ]

        client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-02-01",
            azure_endpoint=self.azure_endpoint,
        )

        try:
            response = client.chat.completions.create(
                model=model_name,
                # model = "deployment_name".
                messages=msgs,
            )

            output = response.choices[0].message.content
        except:
            print("failed response")
            output = "NaN"

        return output

    def test_llm(self, api_name: str):
        """
        Run a user test with a given model and a consistent question (what is 2+2?)
        """

        guidence = """
                   you are an agent design to carry out a number of basic tests
                   """

        print(f"testing = {api_name}")
        test_prompt = "What is 2+2?"

        if api_name in self.registered_models:
            answer = self.llm_architecture(guidence, test_prompt, api_name)
        else:
            answer = f"{api_name} is incorrect or not built into the package"

        print(answer)
