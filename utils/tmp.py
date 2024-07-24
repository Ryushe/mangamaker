import os
import shutil
 
class TempDir:

    def __init__(self):
        try: 
            self.tmp = ".tmp"
            self.tmp_folder = os.path.join(os.getcwd(), self.tmp)
            os.mkdir(self.tmp_folder)
        except:
            print("tmp exists bozo")

    def make_tempdir(self, dirname):
        self.dirname = dirname
        self.temp_dir = os.path.join(os.getcwd(), self.tmp, self.dirname)
        try:
            print(f"Creating tempdir {self.dirname}")
            os.mkdir(self.temp_dir)
        except FileExistsError:
            print(f"Clearing {dirname} (Because it exists already)")
            try:
                shutil.rmtree(self.temp_dir)
                os.mkdir(self.temp_dir)
            except:
                print(f"Please manually remove {self.dirname} before continuing")
                exit()
        return self.temp_dir
    
    def get_path(self, dirname=''):
        try:
            return self.temp_dir
        except:
            if dirname:
                self.temp_dir = os.path.join(os.getcwd(), self.tmp, dirname)
                return self.temp_dir
            else: print("please add a dirname to get_path")
        
    def close(self):
        # gets the path of the temp folder
        temp_path = os.path.realpath(self.temp_dir)
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(temp_path)
                print(f"Sucessfully removed {temp_path}")
            except FileNotFoundError:
                print(f"{self.temp_dir.name} doen't exist")
            except Exception as e:
                print(f"Tried to remove {self.temp_dir.name} but failed")
                print(f"Error when trying to remove {e}")
               