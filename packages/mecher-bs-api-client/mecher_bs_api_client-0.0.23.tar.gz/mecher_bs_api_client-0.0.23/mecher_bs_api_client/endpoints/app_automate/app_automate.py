import allure
from easydict import EasyDict
from starlette.datastructures import UploadFile

from mecher_bs_api_client.browserstack_api_init import BrowserStack_ApiCommon


class AppAutomate_Api(BrowserStack_ApiCommon):
    def __init__(self, user_name: str, access_key: str):
        super().__init__(user_name=user_name, access_key=access_key)
        self.app_automate_url = self.url + "/app-automate"

    def recent_apps_get(self, **kwargs) -> EasyDict:
        uri = self.app_automate_url + "/recent_apps"
        with allure.step('Browserstack API: Get recent apps'):
            response = self.send_request(method='get',
                                         uri=uri)
            if response == {'message': 'No results found'}:
                response = []
            return response

    def app_delete(self, app_id: str, **kwargs) -> EasyDict:
        uri = self.app_automate_url + f"/app/delete/{app_id}"
        with allure.step('Browserstack API: Delete app'):
            return self.send_request(method='delete',
                                     uri=uri)

    def app_upload(self, custom_id: str, file: UploadFile = None, file_path: str = None, **kwargs) -> EasyDict:
        uri = self.app_automate_url + "/upload"
        with allure.step('Browserstack API: Upload app'):
            if file and file_path:
                raise ValueError('You must provide either file or file_path, not both')

            if file_path:
                multipart_form_data = {
                    'file': (custom_id, open(file_path, 'rb')),
                    'custom_id': (None, custom_id),
                }
            else:
                multipart_form_data = {
                    'file': (custom_id, file),
                    'custom_id': (None, custom_id),
                }
            return self.send_request(method='post',
                                     uri=uri,
                                     files=multipart_form_data)
