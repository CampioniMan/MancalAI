from AIBots.BigNeuralNetworkBot import BigNeuralNetworkBot
from AIBots.SmallNeuralNetworkBot import SmallNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import Trainer
from pathlib import Path


def get_all_files_pathlib(path):
    files = [path + "/" + entry.name for entry in Path(path).iterdir() if entry.is_file()]
    return files


folder_paths = [#f"Data/Random_vs_Random",
                #f"Data/MinMax6_vs_MinMax6",
                f"Data/MinMax9_vs_MinMax9",
                #f"Data/Random_vs_MinMax6",
                #f"Data/MinMax_vs_Random",
                #f"Data/MinMaxBot3_vs_MinMaxBot3",
                #f"Data/MinMaxBot5_vs_MinMaxBot5",
                #f"Data/MancalaFocusedMinMaxBot3_vs_MinMaxBot3",
                #f"Data/MinMaxBot3_vs_MancalaFocusedMinMaxBot3",
                #f"Data/Random Player_vs_Random Player",
                "Data/MinMaxBot8_vs_MancalaFocusedMinMaxBot7",
                "Data/MinMaxBot7_vs_MancalaFocusedMinMaxBot7",
                "Data/MinMaxBot7_vs_MancalaFocusedMinMaxBot6",
                "Data/MinMaxBot6_vs_MancalaFocusedMinMaxBot7",
                "Data/MancalaFocusedMinMaxBot7_vs_MinMaxBot7",
                ]
all_files = []
for folder_path in folder_paths:
    all_files.extend(get_all_files_pathlib(folder_path))

patience = 4
bot = BigNeuralNetworkBot()
bot.verbose = 1
epoch_count = 1000
trainer = Trainer()
trainer.load_data(all_files)
history = trainer.train_model(bot, epoch_count, patience)
print("Training ended")

file_name = f"Data/Models/{bot.get_title()}/l{history.history['val_loss'][-1-patience]:.6f}_a{history.history['val_accuracy'][-1-patience]:.6f}_e{len(history.history['loss'])-patience}.keras"
bot.model.save(file_name)
print(f"Model saved at {file_name}")
