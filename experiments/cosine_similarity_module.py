from asyncio import get_event_loop

from ipv8.loader import overlay

from experiment_infrastructure.cosine_similarity_eval.community import CosineEvalCommunity
from gumby.experiment import experiment_callback
from gumby.modules.community_experiment_module import IPv8OverlayExperimentModule
from gumby.modules.ipv8_community_launchers import IPv8CommunityLauncher


@overlay(CosineEvalCommunity)
class CosineEvalCommunityLauncher(IPv8CommunityLauncher):
    pass


class CosineEvalModule(IPv8OverlayExperimentModule):
    def __init__(self, experiment):
        super().__init__(experiment, CosineEvalCommunity)

    def on_id_received(self):
        super().on_id_received()
        self.ipv8_provider.custom_ipv8_community_loader.set_launcher(CosineEvalCommunityLauncher())

    @experiment_callback
    def start_cosine_exec(self):
        self.overlay.start_cosine_exec(self.my_id, self)
        get_event_loop().run_forever()
