from mecher_bs_api_client.endpoints.app_automate.app_automate import AppAutomate_Api


class BrowserStack_API(AppAutomate_Api):
    def __init__(self, user_name: str, access_key: str):
        super().__init__(user_name=user_name, access_key=access_key)

