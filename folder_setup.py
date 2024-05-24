import os

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

if __name__ == '__main__':
    pwd = os.getcwd()

    folders = ['src/analysis', 'src/analysis/line_plots', 
               'src/analysis/txts', 'src/analysis/individual_game_plots',
               'plots']
    
    for path in folders:
        create_folder_if_not_exists(os.path.join(pwd, path))

    exit(0)