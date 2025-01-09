import os
from typing import Self, Callable
from pydantic import BaseModel, ConfigDict
from types import ModuleType


class BasePromptLibrary(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda name: name.replace('_', ' ').title(),
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    @classmethod
    def load(cls, path_or_module: str | ModuleType) -> Self:
        data = directory_to_dict(path_or_module)
        return cls.model_validate(data)


def directory_to_dict(
    path_or_module: str | ModuleType, extension: str = ''
) -> dict[str, dict | str]:
    """
    Recursively read a directory of files/subdirectories into a dictionary, where
    file/directory names are used as keys, and the contents are used as values.

    Pass an extension to filter which files are read.

    Example:

    Given a directory with the following structure...

        MY_PATH/
          subdir/
            subsubdir/
              foo.md
            bar.md
          stuff.md

    ...the following code...

        print(directory_to_dict('path/to/MY_PATH', extension='.md'))

    ...will produce this dictionary:

        {
            "subdir": {
                "subsubdir": {
                    "foo": "contents of foo.md",
                },
                "bar": "contents of bar.md",
            },
            "stuff": "contents of stuff.md",
        }
    """
    path = _handle_module_path(path_or_module)

    if not os.path.isdir(path):
        raise ValueError(f"Path must be a directory: '{path}'")

    def filter_entry(entry: os.DirEntry) -> bool:
        return entry.is_dir() or entry.is_file() and entry.name.endswith(extension)

    def handle_path(path: str) -> dict | str:
        if os.path.isdir(path):
            return {
                entry.name.split('.')[0]: handle_path(entry.path)
                for entry in os.scandir(path)
                if filter_entry(entry)
            }
        return open(path, 'r').read()

    return handle_path(path)  # type: ignore


def dict_to_directory(
    data: dict,
    path_or_module: str | ModuleType,
    extension: str = '',
    alias_generator: Callable[[str], str] = lambda s: s,
    clear_directory: bool = False,
) -> None:
    """
    Recursively writes a dict to files/subdirectories in a given directory path.

    The inverse of 'directory_to_dict', this function takes a dict of string keys,
    whose values are either strings representing a file's contents or another dict
    representing a subdirectory, and writes them to the given path.

    If `clear_directory` is set, `path` will be deleted if it exists before writing.

    The `alias_generator` function, if passed, will be used to transform the names of
    keys for files and directories. Do NOT use this function to add file extensions,
    because it will also be applied to subdirectory names.
    """
    path = _handle_module_path(path_or_module)

    if clear_directory and os.path.exists(path):
        import shutil
        shutil.rmtree(path)

    suffix = extension and '.' + extension.removeprefix('.')
    
    def handle_data(data: dict | str, path: str):
        if not isinstance(data, dict):
            return open(path + suffix, 'w').write(str(data))

        os.makedirs(path, exist_ok=True)
        for name, value in data.items():
            handle_data(value, os.path.join(path, alias_generator(name)))

    handle_data(data, path)


def module_path(module: ModuleType) -> str:
    """
    Returns the path to the given module as a string.
    """
    return getattr(module, '__path__')[0]


def _handle_module_path(path_or_module: str | ModuleType) -> str:
    if isinstance(path_or_module, ModuleType):
        return module_path(path_or_module)
    return path_or_module


if __name__ == '__main__':
    import prompts
    print(directory_to_dict(module_path(prompts), '.md'))

    class StuffPrompts(BasePromptLibrary):
        thing3: str = 'hi world'

    class Prompts(BasePromptLibrary):
        other_thing: str
        thing1: str
        stuff: StuffPrompts
        nice: str = 'hello'


    p = Prompts.load(prompts)
    print(p)
