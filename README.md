# my_dict
A dictionary program to store all the new words I encountered.

# How to release
Currently, I use _PyInstaller_ to deply single file program for **my_dict**.

Check all dependencies are installed using `pipenv`.

```bash
pip list
# And the output shall similar to below,
Package        Version   
-------------- ----------
altgraph       0.17      
beautifulsoup4 4.8.2     
bs4            0.0.1     
certifi        2019.11.28
chardet        3.0.4     
idna           2.9       
pip            20.0.2    
PyInstaller    3.6       
PyMySQL        0.9.3     
PyQt5          5.14.1    
PyQt5-sip      12.7.1    
PyQtWebEngine  5.14.0    
requests       2.23.0    
setuptools     46.1.3    
soupsieve      2.0       
urllib3        1.25.8    
wheel          0.34.2 
```

Use following command to deploy a single file executable.
`pyinstaller -F dict.py`
