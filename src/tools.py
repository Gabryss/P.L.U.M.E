import subprocess
import os
import json

class Tools():

    def substract_list(self, list1_p, list2_p):
        """
        Substract two list and return the resulting list
        """
        result = []
        for i,j in zip(list1_p, list2_p):
            result.append(i-j)
        return result
    
    def oposite(self, list_p):
        """
        Return the oposite of every number on a list
        """
        for i in range(len(list_p)):
            list_p[i]=-list_p[i]
        return list_p
    

    def find_file(file_name_p):
        """
        Given an executable's name file given as a paramete check if the path exist in the path.json file.
        If the path.json file or the path doesn't exist find it over the /home/ directory.
        """
        file_name = file_name_p
        command = f"find /home/ -type f -name {file_name} -executable 2>/dev/null | grep -vE '/\.local/share/Trash/'"
        path_file_path = os.path.dirname(__file__)+"/path.json"
        if not os.path.exists(path_file_path):
            # path.json file doesn't exist
            output = subprocess.check_output(command, shell=True, text=True)
            search_results = output.strip().split('\n')
            if len(search_results) > 1:
                print(f"Multiple {file_name} files found, executing the first one only.")
            file_path = {
                    f"{file_name}":search_results[0]
                }
            json_object = json.dumps(file_path, indent=4)
            with open(path_file_path,"w") as outfile:
                outfile.write(json_object)
            return search_results[0]
            

        else:
            # path.json exist
            with open(path_file_path,'r') as openfile:
                json_object = json.load(openfile)
            
            for key in json_object:
                if key == file_name:
                    return json_object[key]
                else:
                    output = subprocess.check_output(command, shell=True, text=True)
                    search_results = output.strip().split('\n')
                    if len(search_results) > 1:
                        print(f"Multiple {file_name} files found, executing the first one only.")
                    json_object[file_name] = search_results[0]

                    with open(path_file_path,"w") as outfile:
                        outfile.write(json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': ')))
                    return search_results[0]