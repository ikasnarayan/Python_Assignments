import threading

def read_file(file_path: str):
    try:
        with open(file_path, "r") as f:
            content = f.read()
        print(f"\nThread {threading.get_ident()} reading {file_path}:\n{content}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def read_multiple_files(files: list[str]):
    threads = []
    for file in files:
        t = threading.Thread(target=read_file, args=(file,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("\nAll threads finished.")
