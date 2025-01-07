import os
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Any

from easydict import EasyDict

from mecher_bs_api_client.blocks.blocks_aggregator._blocks import _BrowserStack_ApiBlocks
from mecher_bs_api_client.utils import get_element_from_list


@dataclass
class BrowserStack_Artefact_APIBlocks:
    api: Union[_BrowserStack_ApiBlocks, Any]

    def check_is_artefact_uploaded(self, app_artefact_file_name: str) -> EasyDict | None:
        uploaded_apps = self.api.app_automate_api.recent_apps_get()
        app_info = get_element_from_list(
            list_for_search=uploaded_apps,
            function_for_search=lambda app: app.custom_id == app_artefact_file_name,
            not_found_ok=True)
        return app_info

    def upload_artefact(self, custom_id: str, file_bytes) -> EasyDict:
        return self.api.app_automate_api.app_upload(custom_id=custom_id,
                                                    file=file_bytes)

    def update_artefacts(self, artefact_paths: list[str], artefact_maximum_age_in_days: int = 20):
        recent_apps = self.api.app_automate_api.recent_apps_get()

        for artefact_path in artefact_paths:
            artefact_name = os.path.basename(artefact_path)

            app_info = get_element_from_list(list_for_search=recent_apps,
                                             function_for_search=lambda app: app.custom_id == artefact_name,
                                             not_found_ok=True)

            if not app_info:
                self.api.app_automate_api.app_upload(file_path=artefact_path,
                                                     file_name=artefact_name,
                                                     custom_id=artefact_name)
            else:
                uploaded_at_dt = datetime.strptime(app_info.uploaded_at, '%Y-%m-%d %H:%M:%S %Z')
                if (datetime.now() - uploaded_at_dt).days > artefact_maximum_age_in_days:
                    self.api.app_automate_api.app_delete(app_info.app_id)
                    self.api.app_automate_api.app_upload(file_path=artefact_path,
                                                         file_name=artefact_name,
                                                         custom_id=artefact_name)
                else:
                    self.api.app_automate_api.logger.info(f'Artefact "{artefact_name}" is up to date')
