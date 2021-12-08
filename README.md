# TL

TL is a tool for performing [Termeley-Lieb](https://en.wikipedia.org/wiki/Temperley%E2%80%93Lieb_algebra) calculus in [Python](https://www.python.org/).
There are no other libraries required.

This project was initially developed during a course on [Lie algebras](https://en.wikipedia.org/wiki/Lie_algebra) for calculating Jones-Wenzl projectors in <img src="https://render.githubusercontent.com/render/math?math=TL%5E%5Cmathbb%7BC%7D_n(-2)">.
But this library can be used for general calculations.

## Install

### Never heard of git
At the top right of this page, there is a green button labelled **Code**.
Press it and choose the option **Download ZIP**.
You can now place the zip anywhere you want to have the TL library available.
Unzip the folder into your project directory.
Assuming your project directory is called _My Project_ and you already have a file called _main.py_, then your  file sturcture should look like:
```
My Project/
├── main.py
└── TL/
    ├── examples.py
    └── [...]
```
In your _main.py_ you can now import TL via:
```python
from TL import *
```

### Using git
`cd` into your project directory.
Then run
```
$ git clone git@github.com:hexaron/TL.git
```
In your project directory create a _main.py_.
In your _main.py_ you can now import TL via:
```python
from TL import *
```

## Examples
Find many examples in the [_TL/examples.py_](https://github.com/hexaron/TL/blob/main/examples.py) file.

### First example

Put the following into your _main.py_ using your favorite editor:
```python
from TL.tl import TL

# Get `U_2` in TL_4
U_2 = TL.U(4, 2)

# Print the string diagram of `U_2`
print(U_2)

U_1 = TL.U(4, 1)

# Print the composition of `U_1` and `U_2`
# (read right to left as usual)
print(U_1 * U_2)

# Print the tensor product of `U_1` and `U_2`
# (resulting in an element of TL_8)
print(U_1 & U_2)
```
Running _main.py_ now produces the following output:
```
    0 1 2 3 
    | | \_/
    | |    
    | |    
1 * | |    
    | |    
    | |  _ 
    | | / \
    7 6 5 4 




    0 1 2 3 
    | \_/ |
    |     /
    |    / 
1 * |   /  
    |  /   
    | /  _ 
    | | / \
    7 6 5 4 




    0 1 2 3 4 5 6 7 
    | \_/ | | | \_/
    |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
1 * |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
    |     | | |    
    |  _  | | |  _ 
    | / \ | | | / \
    1514131211109 8 
```
