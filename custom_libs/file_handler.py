
def get_replacement_list(file_path : str):
    dict_built = dict()
    try:
        f = open(file_path, 'r')
        STRING = f.read()
        f.close()
        for line in STRING.splitlines():
            args = line.split(":")
            arg1 = args[0].split("\"")[1]
            arg2 = args[1].split("\"")[1]
            dict_built[arg1] = arg2
        return dict_built
    except Exception as E:
        print(f"failed to get replacment list \"{file_path}\"; defualting to none\nERROR INFO:{str(E)}")
        return dict()
