from types import SimpleNamespace
import yaml

Config: SimpleNamespace = SimpleNamespace(
    render=False,
    agent_blue_method="Human",
    agent_red_method="Human",
)

with open("config.yml") as raw_yaml:
    yml = yaml.load(raw_yaml, Loader=yaml.FullLoader)
    if yml["app"]:
        if yml["app"]["render"]:
            Config.render = yml["app"]["render"]
    if yml["agent_blue"]:
        if yml["agent_blue"]["method"]:
            Config.agent_blue_method = yml["agent_blue"]["method"]
    if yml["agent_red"]:
        if yml["agent_red"]["method"]:
            Config.agent_red_method = yml["agent_red"]["method"]
