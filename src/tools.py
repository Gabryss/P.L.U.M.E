import subprocess

class Tools():

    def substract_list(self, list1, list2):
        """
        Substract two list and return the resulting list
        """
        result = []
        for i,j in zip(list1, list2):
            result.append(i-j)
        return result
    
    def oposite(self, list_p):
        """
        Return the oposite of every number on a list
        """
        for i in range(len(list_p)):
            list_p[i]=-list_p[i]
        return list_p
    

    def find_file(file_name):
        command = f"locate -b '\{file_name}' | xargs -r -I % find % -prune -type f -executable"
        output = subprocess.check_output(command, shell=True, text=True)
        search_results = output.strip().split('\n')
        if len(search_results) > 1:
            print(f"Multiple {file_name} files found, executing the first one only.")
        return search_results[0]