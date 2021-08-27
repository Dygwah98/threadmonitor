Library originally made by Guido Scarlato, forked by Davide Caligiuri.

# GraphThreading

![](resource/application.PNG)

### Example
``` python 
# to obtain a perfectly valid multithreading code, replace with:
# from threading import Lock, Thread, Condition
from threadmonitor.wrapper.threading import Lock, Thread, Condition
from threadmonitor import startGraph

class Structure:
    def __init__(self):
        self.lock = Lock()
        self.condition = Condition(self.lock)
    
    def get(self):
        self.lock.acquire()
        self.lock.release()

class MyThread(GraphThread):
    def __init__(self,structure):
        super().__init__()
        self.structure = structure

    def run(self):
        while True:
            self.structure.get()

if __name__ == "__main__":            
    structure = Structure()
    threads = []

    for i in range(4):
        t = MyThread(structure)
        threads.append(t)

    for t in threads:
        t.start()

    startGraph()
```
## Instructions
---
### Clone

- Clone this repo to your local machine using `https://github.com/Dygwah98/threadmonitor`
---
### Setup

> using pipenv (recommended):

```shell
pipenv run install
```

> using pipenv (alternative):

```shell
py -m pipenv run install
```

> using pip:

```shell
sudo apt-get install python3-tk
pip3 install -r requirements.txt 
```

---
### Update documentation

```shell
cd docs
make clean
make [html | epub | latex | ...] 
```
For more, refer to the [Sphinx documentation](https://www.sphinx-doc.org/en/master/man/sphinx-build.html).

---
### Execute tests

```shell
py -m tests.[testname]
```

---
## Features
> Graphic representation of the components

> Start and stop the whole system

> Excecution step by step 

> Seamless integration with the existing threading module
