from emp_ide import IDE
from emp_utils import webrepl_pass
from emp_utils import WebREPL


WebREPL.start(password=webrepl_pass())
ide = IDE(1)
