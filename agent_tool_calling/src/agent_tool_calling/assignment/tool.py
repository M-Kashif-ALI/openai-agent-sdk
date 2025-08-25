from agents import function_tool
import math

@function_tool
def calculator_tool(num1: int | float, operation: str, num2: int | float = 0):
  """
  This is a simple calculator tool that can handle different math problems.  
  It follows the standard order of operations (PEMDAS/BODMAS):  

  1. Parentheses ( )  
  2. Exponents and Square Roots (** , sqrt)  
  3. Division, Multiplication, and Modulus (/ , * , %)  
  4. Addition and Subtraction (+ , -)  

  You can use the following operations:  
  - Addition (+)  
  - Subtraction (-)  
  - Multiplication (*)  
  - Division (/)  
  - Modulus (%)  
  - Exponentiation (**)  
  - Square Root (sqrt)  
  - Parentheses ( ) for grouping  

  Just write your math expression, and the calculator will solve it step by step using the correct rules.
  """
  
  
  # print("Calculating.....")
  
  if operation in ("add", "+"):
    return num1 + num2
  elif operation in ("subtract", "-"):
      return num1 - num2
  elif operation in ("multiply", "*"):
      return num1 * num2
  elif operation in ("divide", "/"):
      return num1 / num2
  elif operation in ("modulus", "%"):
      return num1 % num2
  elif operation in ("exponentiate", "**"):
      return num1 ** num2
  elif operation == "sqrt":
      return math.sqrt(num1)
  else:
      return "Invalid operation"