from enum import Enum


class Color(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



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