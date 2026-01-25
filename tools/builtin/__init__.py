from tools.builtin.edit_tool import EditTool
from tools.builtin.grep import GrepTool
from tools.builtin.read_file import ReadFileTool
from tools.builtin.shell import ShellTool
from tools.builtin.write_file import WriteFileTool
from tools.builtin.list_dir import ListDirTool
__all__=[
    "ReadFileTool",
    "WriteFileTool",
    "EditTool",
    "ShellTool",
    "ListDirTool",
    "GrepTool"
]

def get_all_builtin_tools()->list[type]:
    return [
        ReadFileTool,
        WriteFileTool,
        EditTool,
        ShellTool,
        ListDirTool,
        GrepTool
        ]