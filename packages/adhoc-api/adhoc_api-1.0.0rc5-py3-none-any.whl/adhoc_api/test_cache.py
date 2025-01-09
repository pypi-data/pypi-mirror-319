from archytas.react import ReActAgent, FailedTaskError
from easyrepl import REPL
from adhoc_api.tool import AdhocApi, APISpec
from adhoc_api.utils import move_to_isolated_dir
from pathlib import Path

import pdb




def main():
    api = get_api_spec()
    adhoc_api = AdhocApi(apis=[api], drafter_config={'provider': 'google', 'model': 'gemini-1.5-flash-001', 'ttl_seconds': 60})
    # agent = ReActAgent(model='gpt-4o', tools=[adhoc_api], verbose=True)
    # print(agent.prompt)

    # work in an isolated directory
    with move_to_isolated_dir():
        # REPL to interact with agent
        for query in REPL(history_file='../.chat'):
            try:
                # answer = agent.react(query)
                answer = adhoc_api.ask_api('Secret Number API', query)
                print(answer)
            except FailedTaskError as e:
                print(f"Error: {e}")



def get_api_spec() -> APISpec:
    numbers = '\n'.join(f'{i}' for i in range(33000) if i not in (42, 19246))  # skip some target numbers
    documentation = f'## Secret Number API\nThis is sample documentation for testing purposes. A list of numbers will be provided and the goal is to identify which number(s) are missing.\n\n#Number\n{numbers}'
    api: APISpec = {
        'name': "Secret Number API",
        'cache_key': 'secret_number_cache_debugging',
        'description': "This is a test API for debugging purposes.",
        'documentation': documentation,
    }
    return api



if __name__ == "__main__":
    main()

