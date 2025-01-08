import json
import logging

from langchain_core.language_models import BaseChatModel

from ceo.ability.ability import Ability
from ceo.prompt.prompt import Prompt

log = logging.getLogger('ceo.prompt')

END = '--END--'


class SchedulerPrompt(Prompt):
    def __init__(self, query: str, abilities: list[Ability], ext_context: str = ''):
        self.abilities = abilities
        prompt = dict()
        for ability in self.abilities:
            prompt[ability.name] = ability.to_dict()
        prompt = json.dumps({
            "precondition": "In <abilities> are the abilities you have. "
                            f'And there is a <user_query>.',
            "limitation": "You can only use abilities in <abilities>.",
            "user_query": query,
            "task": "What you need to do is to plan your workflow based on the <abilities> and <user_query>.",
            "description": "<user_query> might contains many steps, "
                           "think carefully about every step and plan your workflow "
                           "based on your abilities in <abilities>.",
            "hint_for_tool_usage": "<user_query> sometimes need to use one specific tool(s) more than once, "
                                   "you need to estimate as accurately as possible "
                                   "the number of times specific tools need to be used "
                                   "to properly achieve the <user_query>!",
            "hint_for_tool_choosing": "Sometimes some of the tools are irrelevant to <user_query>. "
                                      "Make sure to choose tools properly and wisely.",
            "abilities": prompt,
            "output_format": "{thinking_process}\n"
                             "schedule:{schedule_as_a_list_of_tool_names}\n"
                             f"{END}",
            "hint_1_for_output": 'firstly, output your thinking process step by step clear and organized. '
                                 'secondly, outputs a list of names of tools, surrounded by "[ ]", split by ", ".',
            "hint_2_for_output": 'You must strictly follow the format in <output_format>! '
                                 'You should refer to example in <output_example>!',
            "output_example": "1.First, I need to determine which ingredients to purchase, "
                              "which requires checking a recipe or personal preferences to decide.\n"
                              "2.After determining the ingredients, "
                              "I need to go to the market or supermarket to buy the required ingredients.\n"
                              "3.After purchasing the ingredients, I need to bring them home.\n"
                              "4.Once home, I need to wash and prepare the ingredients.\n"
                              "5.After preparation, I start cooking.\n"
                              "6.After cooking is complete, I need to arrange the dishes on the dining table.\n"
                              "schedule:"
                              "[go_to_market, payment_purchase, go_home, do_wash, do_cook, arrange_dished_on_table]\n"
                              f"{END}",
            "hint_for_end_pattern": f'The "{END}" pattern marks the end of your whole response, '
                                    f'no more words are allowed after "{END}" pattern. '
                                    f'The "{END}" pattern is absolutely important, do not forget to place it '
                                    'in the end of your response.'
        }, ensure_ascii=False)
        super().__init__(prompt, ext_context)
        log.debug(f'SchedulerPrompt: {self.prompt}')

    def invoke(self, model: BaseChatModel) -> list[Ability]:
        results = model.invoke(self.prompt).content
        log.debug(f'SchedulerResponse: {results}')
        results = results[results.rfind('['):results.rfind(']') + 1][1:-1].split(',')
        results = [result
                   .replace('\n', '')
                   .replace('\"', '')
                   .replace('\'', '').strip()
                   for result in results]
        _fin_results = list()
        for _a_result in results:
            for ability in self.abilities:
                if ability.name == _a_result:
                    _fin_results.append(ability)
        return _fin_results
