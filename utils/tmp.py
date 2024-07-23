import os
import shutil
 
class TempDir:

    def make_tempdir(self, dirname):
        self.temp_dir = os.path.join(os.getcwd(), dirname)
        try:
            print(f"attempting to create tempdir {dirname}")
            os.mkdir(self.temp_dir)
        except FileExistsError:
            print(f"Clearing {dirname} (Because it exists already)")
            try:
                shutil.rmtree(self.temp_dir)
                os.mkdir(self.temp_dir)
            except:
                print(f"Please manually remove {dirname} before continuing")
                exit()
        return self.temp_dir
    
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
               