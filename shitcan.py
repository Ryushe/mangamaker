def check_file_modified(repo_url, file_path, branch='master'):
    local_repo_path = f'{file_path}'

    # Clone the repository if it doesn't exist locally
    if not os.path.exists(local_repo_path):
        repo = git.Repo.clone_from(repo_url, local_repo_path)
    else:
        repo = git.Repo(local_repo_path)
        repo.remotes.origin.fetch()

    # Get the latest commit
    latest_commit = repo.commit(branch)

    # Get the file from the latest commit
    file_in_latest_commit = latest_commit.tree / file_path

    # Get the content of the file in the latest commit
    remote_content = file_in_latest_commit.data_stream.read().decode('utf-8')

    local_file_path = f'./{os.path.basename(file_path)}'

    if os.path.exists(local_file_path):
        with open(local_file_path, 'r') as local_file:
            local_content = local_file.read()

        if local_content == remote_content:
            print("File hasn't been modified.")
        else:
            print("File has been modified.")
            # Perform the necessary actions if needed
    else:
        print("Local file doesn't exist. Need to clone.")

# check_file_modified('https://github.com/ciromattia/kcc/blob/master/kcc-c2e.py', 'kcc-c2e.py')

def make_temp_dir(cbz_path):
    try:
        print(f"Trying to make temp directory in {cbz_path}")
        temp_dir = os.path.join(cbz_path, '.temp_files')
        os.makedirs(temp_dir)
        time.sleep(1)
        return temp_dir
    except FileExistsError:
        time.sleep(1)
        print(f"temp folder already exists in {cbz_path}")

