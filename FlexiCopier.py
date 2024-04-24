import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# グローバル変数の定義
filename_list = 'filenames.txt'  # ファイル名リストのパス

def create_filename_list():
    # ファイル名リストが存在しない場合に作成する
    if not os.path.exists(filename_list):
        open(filename_list, 'a').close()

def select_source_file():
    # 元のファイルを選択する
    return filedialog.askopenfilename(title="元のファイルを選択", filetypes=[("All files", "*.*")])

def select_destination_dir():
    # コピー先のディレクトリを選択する
    return filedialog.askdirectory(title="コピー先のディレクトリを選択")

def copy_files(source_file, destination_dir):
    # ファイルの拡張子を取得
    _, file_extension = os.path.splitext(source_file)
    
    # ファイル名リストを読み込んでファイルをコピーする
    try:
        with open(filename_list, 'r') as file:
            for line in file:
                new_filename = line.strip() + file_extension  # 拡張子を追加
                if new_filename:
                    destination_path = os.path.join(destination_dir, new_filename)
                    shutil.copy(source_file, destination_path)
                    print(f"File copied to: {destination_path}")
        messagebox.showinfo("完了", "すべてのファイルがコピーされました。")
    except FileNotFoundError:
        messagebox.showerror("エラー", "元のファイルまたはファイル名リストが見つかりません。")
    except PermissionError:
        messagebox.showerror("エラー", "ファイルのコピーに必要な権限がありません。")
    except Exception as e:
        messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {str(e)}")

def main():
    create_filename_list()
    source_file = select_source_file()
    if source_file:
        destination_dir = select_destination_dir()
        if destination_dir:
            copy_files(source_file, destination_dir)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない
    main()
