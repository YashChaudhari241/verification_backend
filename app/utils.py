def fixFilename(filename: str, index: int):
    return (str(index)+filename[filename.rindex('.'):])
