from AIBots.SmallNeuralNetworkBot import SmallNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import Trainer
from pathlib import Path


def get_all_files_pathlib(path):
    files = [path + "/" + entry.name for entry in Path(path).iterdir() if entry.is_file()]
    return files


folder_paths = [f"Data/Random_vs_Random", f"Data/MinMax6_vs_MinMax6"]
all_files = []
for folder_path in folder_paths:
    all_files.extend(get_all_files_pathlib(folder_path))

bot = SmallNeuralNetworkBot()
epoch_count = 10
trainer = Trainer()
trainer.load_data(all_files)
history = trainer.train_model(bot, epoch_count)
print("Training ended")

file_name = f"Data/Models/SmallNeuralNetworkBot/l{history.history['val_loss'][-1]:.6f}_a{history.history['val_accuracy'][-1]:.6f}_e{epoch_count}.keras"
bot.model.save(file_name)
print(f"Model saved at {file_name}")
