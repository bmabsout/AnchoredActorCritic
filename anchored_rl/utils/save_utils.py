import json
import os
from keras import models, Model
import pickle
from anchored_rl.utils.args_utils import Arg_Serializer
from pathlib import Path
from anchored_rl.utils.serialization_utils import ExtraTypesEncoder


def save_hypers(experiment_name, hypers, cmd_args, serializer:Arg_Serializer):
    """ Saves the hyperparameters to a json file in the experiment folder. Uses semantic naming for the folder."""
    all_hypers = {**vars(cmd_args), **vars(hypers)}

    save_path = Path(serializer.get_seed_folder_path(experiment_name, all_hypers), "epochs")
    common_output_path = Path("trained", experiment_name, serializer.get_semantic_folder_name(all_hypers))
    os.makedirs(common_output_path, exist_ok=True)
    with open(f"{common_output_path}/hypers.json", "w") as f:
        json.dump(serializer.remove_ignored(all_hypers), f, indent=4, cls=ExtraTypesEncoder)
    return save_path


def latest_subdir(path='.'):
    return max(Path(path).glob('*/'), key=os.path.getmtime)


def get_last_epoch_path_for_each_seed_folder(path):
    return [latest_subdir(str(d)) for d in Path(path).glob('seeds/*/epochs/')]


def find_folders(dirname, name_to_find) -> list[str]:
    subfolders = [f.path for f in os.scandir(
        dirname) if f.is_dir()]
    subfolders_with_the_right_name = [ subfolder for subfolder in subfolders if Path(subfolder).name == name_to_find]
    for dirname in list(subfolders):
        subfolders_with_the_right_name.extend(find_folders(dirname, name_to_find))
    return subfolders_with_the_right_name


def find_all_train_paths(path):
    return [Path(folder) for folder in find_folders(path, "models")]


def latest_train_folder(path):
    return max(find_all_train_paths(path), key=os.path.getmtime)


def concatenate_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def on_save(actor: Model, q_network: Model, epoch:int, replay_buffer, replay_save:bool, save_path:str):
    path = Path(save_path, str(epoch), "models")
    os.makedirs(path, exist_ok=True)
    print("saving at", path.parent)
    actor.save(path / "actor.keras")
    q_network.save(path / "critic.keras")
    if replay_save:
        with open( Path(save_path, "replay.p"), "wb" ) as replay_file:
            pickle.dump( replay_buffer, replay_file)

def load_critic(folder):
    return models.load_model(Path(folder, "critic.keras"))

def load_actor(folder):
    return models.load_model(Path(folder, "actor.keras"))

def load_replay(folder: str):
    return pickle.load(open(Path(folder).parent / "replay.p", "rb"))
