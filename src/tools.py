import subprocess
import os
import json


class Tools:

    @staticmethod
    def substract_list(list1_p, list2_p):
        """
        Substract two list and return the resulting list
        """
        result = []
        for i,j in zip(list1_p, list2_p):
            result.append(i-j)
        return result
    
    @staticmethod
    def oposite(list_p):
        """
        Return the oposite of every number on a list
        """
        for i in range(len(list_p)):
            list_p[i]=-list_p[i]
        return list_p


    @staticmethod
    def execute_cli(command_p, *args):
        """
        Execute a command line based on the python subprocess library
        """
        command = command_p
        output = subprocess.check_output(command, shell=True, text=True)
        results = output.strip().split('\n')
        return results
    

    @staticmethod
    def write_json(data_p, path_p):
        """
        Write data into a json file
        """
        data = data_p
        # mode = mode_p
        path = path_p

        json_object = json.dumps(data, indent=4)
        with open(path,"w") as outfile:
            outfile.write(json_object)
    

    @staticmethod
    def remove_dupliacte_tuples(tuple_list_p):
        """
        Takes a list of tuple in parameter and return a list of unique tuples irrespective of 
        their order.
        """
        if tuple_list_p:
            unique_tuples = []

            for t in tuple_list_p:
                if t==None:
                    continue
                if not all(t):
                    continue
                if sorted(t) not in [sorted(x) for x in unique_tuples]:
                    unique_tuples.append(t)
            return unique_tuples
        
        else:
            return None
    

    @staticmethod
    def remove_duplicate_none_list(list_p):
        """
        Take a list as input and return the same list without duplicates or none elements
        """
        list_pre = list(dict.fromkeys(list_p))
        while None in list_pre:
            list_pre.remove(None)
        return list_pre


    @staticmethod
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
            search_results = Tools.execute_cli(command)
            if len(search_results) > 1:
                print(f"Multiple {file_name} files found, executing the first one only.")
            data = {
                    f"{file_name}":search_results[0]
                }
            Tools.write_json(data, path_file_path)
            return search_results[0]
            

        else:
            # path.json exist
            with open(path_file_path,'r') as openfile:
                json_object = json.load(openfile)
            
            for key in json_object:
                if key == file_name:
                    if os.path.exists(path_file_path):
                        return json_object[key]
                    else:
                        search_results = Tools.execute_cli(command)
                        json_object[file_name] = search_results[0]
                        Tools.write_json(json_object, path_file_path)
                else:
                    search_results = Tools.execute_cli(command)
                    if len(search_results) > 1:
                        print(f"Multiple {file_name} files found, executing the first one only.")
                    json_object[file_name] = search_results[0]

                    Tools.write_json(json_object, path_file_path)
                    return search_results[0]


