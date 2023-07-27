import subprocess

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
        Find an executable file given it's name given as a parameter
        """
        print("TOOLS DEBUG", file_name_p)
        command = f"find /home/ -type f -name {file_name_p} -executable 2>/dev/null | grep -vE '/\.local/share/Trash/'"
        output = subprocess.check_output(command, shell=True, text=True)
        search_results = output.strip().split('\n')
        print("DEBUG SEARCH",search_results)
        # 1/0
        if len(search_results) > 1:
            print(f"Multiple {file_name_p} files found, executing the first one only.")
        return search_results[0]