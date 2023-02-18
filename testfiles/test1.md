
```bash
(base) root@hecs-67846:~/pybind11-code# python
Python 3.9.12 (main, Apr  5 2022, 06:56:58)
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import classs
>>> p = classs.Pet("Molly")
>>> print(p)
<classs.Pet object at 0x7fe21b234030>
>>> p.getName()
'Molly'
>>> p.setName("Charly")
>>> p.getName()
'Charly'
>>> ?
```