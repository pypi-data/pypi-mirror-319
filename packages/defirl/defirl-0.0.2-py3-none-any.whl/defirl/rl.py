import pandas as pd
import numpy as np
from dataclasses import dataclass
import pickle
from pathlib import Path
import fire
from importlib.resources import files
from scipy.spatial import KDTree



@dataclass
class RLmodel:
    sma_05: float
    sma_07: float
    sma_25: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/q_table.npy'
    state_index_file: str = f'{Path(__file__).resolve().parent}/state_to_index.npy'

    def load_qtable(self):
        with open(self.model_file_path, "rb") as f:
            q_table = np.load(f)
        return q_table

    def load_state_index(self):
        with open(self.state_index_file, "rb") as f:
            state_to_index = np.load(f, allow_pickle=True).item()
        return state_to_index

    def load_action_mapping(self):
        action_mapping = {"go_long": 0, "go_short": 1, "do_nothing": 2}
        return action_mapping

    def prep_state(self):
        state = np.array([[self.sma_05, self.sma_07, self.sma_25, self.sma_compare, self.is_short]])
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)
        return state
    
    def predict_action(self):
        state = self.prep_state()
        loaded_qtable = self.load_qtable()
        loaded_state_to_index = self.load_state_index()
        loaded_mapping = self.load_action_mapping()


        state_tuple = tuple(state.flatten())
        state_index = loaded_state_to_index.get(state_tuple, -1)
        if not state_index == -1:
            try:
                q_values = loaded_qtable[state_index]
            except ValueError as e:
                print(e)
        else:
            # Create a KDTree from the states in the loaded_state_to_index mapping
            state_tuples = list(loaded_state_to_index.keys())
            kdtree = KDTree(state_tuples)

            # Find the nearest neighbor to the current state
            distance, index = kdtree.query(state.flatten())
            nearest_state_tuple = state_tuples[index]
            new_state_index = loaded_state_to_index[nearest_state_tuple]
            q_values = loaded_qtable[new_state_index]
            #raise ValueError("State not found in the state index mapping.")
        best_action_index = np.argmax(q_values)
        
        action = [action for action, index in loaded_mapping.items() if index == best_action_index][0]
        
        results_dict = {
            "raw_state": state,
            "state_tuple": state_tuple,
            "best_action_index": best_action_index,
            "action": action
        }
        return results_dict

def main(sma_05: float, sma_07: float, sma_25: float, sma_compare: int, is_short: int) -> dict:
    try:
        rl_model = RLmodel(
            sma_05,
            sma_07,
            sma_25,
            sma_compare,
            is_short
        )

        return rl_model.predict_action().get("action")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    fire.Fire(main)