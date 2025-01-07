from mecher_bs_api_client.endpoints.browserstack_api import BrowserStack_API


class _BrowserStack_ApiBlocks:
    def __init__(self, user_name: str, access_key: str):
        self.bs_api = BrowserStack_API(user_name=user_name, access_key=access_key)
