import emp_wifi
from emp_ide import IDE
from emp_utils import WebREPL, webrepl_pass

WebREPL.start(password=webrepl_pass())
ide = IDE(1)
