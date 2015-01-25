# SANDBOX

Python Sandbox to run unsafe python code, like unsafe user input. The objective of this sandbox is to block the unsafe
code from run system commadnds like os.system(" rm -rf ~") and access to the file system as well.  This packages
comes with the Sandbox module and the Sandbox test that is a sequence of codes which tries to exploit the sandbox.

REFERENCES

    * http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
    * http://bot24.blogspot.com.br/2013/03/escaping-python-sandbox-ndh-2013-quals.html
    * http://blog.delroth.net/2013/03/escaping-a-python-sandbox-ndh-2013-quals-writeup