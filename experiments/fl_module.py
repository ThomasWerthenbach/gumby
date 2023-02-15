import traceback

from gumby.experiment import experiment_callback
from gumby.modules.community_experiment_module import IPv8OverlayExperimentModule
from gumby.modules.ipv8_community_launchers import IPv8CommunityLauncher
from ipv8.loader import overlay

from experiment_settings.settings import Settings
from federated_learning.community import FLCommunity


@overlay(FLCommunity)
class FederatedLearningCommunityLauncher(IPv8CommunityLauncher):
    pass


class FederatedLearningModule(IPv8OverlayExperimentModule):
    """
    This module contains code to manage experiments with the Basalt community.
    """
    def __init__(self, experiment):
        super().__init__(experiment, FLCommunity)

    def on_id_received(self):
        super().on_id_received()
        self.ipv8_provider.custom_ipv8_community_loader.set_launcher(FederatedLearningCommunityLauncher())

    @experiment_callback
    def assign_role(self, settings_file):
        try:
            with open(settings_file) as f:
                settings = Settings.from_json("".join([x.strip() for x in f.readlines()]))
            self.overlay.log(settings.to_json())
            if self.my_id == 1:
                self.overlay.assign_server(settings)
            else:
                self.overlay.assign_node(self.my_id, self.get_peer('1'), settings)
        except Exception as e:
            self.overlay.log(str(traceback.format_exc()))
