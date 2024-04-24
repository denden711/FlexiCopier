import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# グローバル設定ファイルのパス
config_file = 'app_config.json'
default_filenames = 'filenames.txt'  # デフォルトのファイル名リストのパス

# アプリケーション設定のロードまたは初期設定の作成
def load_or_initialize_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # 初期設定: ファイル名リストがない場合には作成する
        if not os.path.exists(default_filenames):
            with open(default_filenames, 'w') as f:
                # 簡単な例をファイル名リストに記述
                f.write("example_copy1\n")
                f.write("example_copy2\n")
                f.write("example_copy3\n")
            messagebox.showinfo("初期設定", "初期のファイル名リストが作成されました。プログラムを再起動してください。")
            return None  # 初期設定後はプログラムを終了するためにNoneを返す
        config = {
            'filename_list': default_filenames,
            'last_source_dir': '',
            'last_destination_dir': ''
        }
        with open(config_file, 'w') as f:
            json.dump(config, f)
        return config

# 設定の保存
def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

# 元のファイルの選択
def select_source_file(initialdir):
    return filedialog.askopenfilename(title="元のファイルを選択", initialdir=initialdir, filetypes=[("All files", "*.*")])

# コピー先ディレクトリの選択
def select_destination_dir(initialdir):
    return filedialog.askdirectory(title="コピー先のディレクトリを選択", initialdir=initialdir)

# ファイルのコピーと存在チェック
def copy_files(source_file, destination_dir, filename_list):
    _, file_extension = os.path.splitext(source_file)  # 元のファイルの拡張子を取得
    try:
        with open(filename_list, 'r') as file:
            for line in file:
                new_filename = line.strip() + file_extension  # 新しいファイル名に拡張子を追加
                if new_filename:
                    destination_path = os.path.join(destination_dir, new_filename)
                    if os.path.exists(destination_path):
                        if not messagebox.askyesno("確認", f"{new_filename} はすでに存在します。上書きしますか？"):
                            continue
                    shutil.copy(source_file, destination_path)
        messagebox.showinfo("完了", "すべてのファイルがコピーされました。")
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルのコピー中にエラーが発生しました: {str(e)}")
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error copying files: {str(e)}\n")

def main():
    config = load_or_initialize_config()
    if config is None:
        return  # 初期設定の後はプログラムを終了する

    source_file = select_source_file(config['last_source_dir'])
    if source_file:
        config['last_source_dir'] = os.path.dirname(source_file)
        destination_dir = select_destination_dir(config['last_destination_dir'])
        if destination_dir:
            config['last_destination_dir'] = destination_dir
            copy_files(source_file, destination_dir, config['filename_list'])
            save_config(config)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示
    main()
    root.destroy()  # GUIの終了
