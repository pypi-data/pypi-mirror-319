from mecher_bs_api_client.blocks.artefact_blocks import BrowserStack_Artefact_APIBlocks
from mecher_bs_api_client.blocks.blocks_aggregator._blocks import _BrowserStack_ApiBlocks


class BrowserStack_ApiBlocks(_BrowserStack_ApiBlocks):
    def __init__(self, user_name: str, access_key: str):
        super().__init__(user_name=user_name, access_key=access_key)

        self.artefact = BrowserStack_Artefact_APIBlocks(api=self)
