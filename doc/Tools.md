This class provides a set of utility methods for performing operations such as list manipulation, executing command line instructions, writing data to a JSON file, and finding files in a given directory.

## Methods:

- `substract_list(list1_p, list2_p)`:
    
    Subtracts the values of `list2_p` from `list1_p` element-wise. Returns a list of the result.
    
    Input: `list1_p`: List of integers or floats. `list2_p`: List of integers or floats.
    
    Output: List of integers or floats.
    
- `oposite(list_p)`:
    
    Negates each value in the given list `list_p`.
    
    Input: `list_p`: List of integers or floats.
    
    Output: List of integers or floats where each number is the negation of the corresponding number in `list_p`.
    
- `execute_cli(command_p, *args)`:
    
    Executes a shell command provided as `command_p` using the subprocess library. It returns the output of the command as a list of lines.
    
    Input: `command_p`: A string representing a shell command.
    
    Output: List of strings representing lines of command output.
    
- `write_json(data_p, path_p)`:
    
    Writes a Python object `data_p` to a JSON file at location `path_p`.
    
    Input: `data_p`: A Python object (can be a list, dictionary, etc.) `path_p`: String representing the file path.
    
- `find_file(file_name_p)`:
    
    Tries to find the path to a file `file_name_p` in a directory. This function has some specific behaviors:
    
    - If the `path.json` file does not exist, it creates one and records the paths to `file_name_p` in it.
    - If the `path.json` file does exist, it tries to find the path of `file_name_p` in it.
        - If the path exists and is valid, it is returned.
        - If the path exists but is invalid (i.e., the file doesn't exist), it looks for the file in the directory, updates the path in `path.json`, and returns it.
        - If the path does not exist in `path.json`, it looks for the file in the directory, adds the path to `path.json`, and returns it.
    
    If the file is not found in the directory, an error will be raised.
    
    Input: `file_name_p`: String representing the name of the file to find.
    
    Output: String representing the path to the file if found.
    

## Note:

This class is designed as a set of static methods. As such, you don't need to create an instance of the Tools class to use them. You can call them directly on the class itself, like so: `Tools.substract_list(list1, list2)`.