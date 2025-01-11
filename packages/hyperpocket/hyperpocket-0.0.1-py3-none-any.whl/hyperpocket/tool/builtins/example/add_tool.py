# from pydantic import BaseModel, Field
# 
# from pocket.tool.builtin import BuiltinTool
# from pocket.tool.tool import TAny, TModelGeneric
# 
# 
# class Schema(BaseModel):
#     a: int = Field(description="first number to add")
#     b: int = Field(description="second number to add")
# 
# 
# class AddTool(BuiltinTool):
#     name: str = "add_two_number_tool"
#     description: str = "add two numbers"
#     argument_schema: TModelGeneric = Schema
# 
#     def invoke(self, a: int, b: int) -> TAny:
#         return a + b
