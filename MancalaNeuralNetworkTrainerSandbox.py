from AIBots.BigNeuralNetworkBot import BigNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import Trainer
from pathlib import Path


def get_all_files_pathlib(path):
    files = [path + "/" + entry.name for entry in Path(path).iterdir() if entry.is_file()]
    return files


folder_paths = [f"Data/Random_vs_Random",
                f"Data/MinMax6_vs_MinMax6",
                f"Data/MinMax9_vs_MinMax9",
                f"Data/Random_vs_MinMax6",
                f"Data/MinMax_vs_Random"]
all_files = []
for folder_path in folder_paths:
    all_files.extend(get_all_files_pathlib(folder_path))

bot = BigNeuralNetworkBot()
bot.verbose = 1
epoch_count = 1000
trainer = Trainer()
trainer.load_data(all_files)
history = trainer.train_model(bot, epoch_count)
print("Training ended")

file_name = f"Data/Models/{bot.get_title()}/l{history.history['val_loss'][-1]:.6f}_a{history.history['val_accuracy'][-1]:.6f}_e{len(history.history['loss'])}.keras"
bot.model.save(file_name)
print(f"Model saved at {file_name}")
