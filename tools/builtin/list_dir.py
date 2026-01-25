from pydantic import BaseModel, Field
from tools.base import Tool, ToolInvocation, ToolKind, ToolResult
from utils.paths import resolve_path


class ListDirParams(BaseModel): 
    path:str = Field(".",description="The directory path to list(default: current directory)")
    include_hidden:bool = Field(False,description="Whether to include hidden files (default: False)")


class ListDirTool(Tool):
    name = 'list_dir'
    description = 'Lists contents of a directory'
    kind = ToolKind.READ
    schema = ListDirParams


    async def execute(self, invocation:ToolInvocation) -> ToolResult:
        params = ListDirParams(**invocation.params)

        dir_path = resolve_path(invocation.cwd,params.path)

        if not dir_path.exists() or not dir_path.is_dir():
            return ToolResult.error_result(
                f"Directory does not exist: {dir_path}",
            )

        try:
            items = sorted(dir_path.iterdir(),key=lambda p:(not p.is_dir(),p.name.lower()))
        except Exception as e:
            return ToolResult.error_result(
                f"Failed to list directory {dir_path}: {e}",
            )
        
        if not params.include_hidden:
            items = [item for item in items if not item.name.startswith('.')]

        if not items:
            return ToolResult.success_result(
                output=f"Directory is empty: {dir_path}",
                metadata={ 
                    "path": str(dir_path),
                    "entries":0 ,
                }
            )  

        lines = []
        for item in items:
            if item.is_dir():
                lines.append(f"{item.name}/")
            else:
                lines.append(f"{item.name}") 

        return ToolResult.success_result(
            output="\n".join(lines),
            metadata={
                "path": str(dir_path),
                "entries": len(items),
            }  
        )