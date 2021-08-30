#class LockQueue
#class ConditionQueue


import threading
import copy
from typing import Any
from threadmonitor.utils import singleton


class _Topic(list):
    def __call__(self, *args, **kwargs):
        print(f'callbacks being executed: {self}')
        ret = [f(*args, **kwargs) for f in self]
        print(f'returning results of call: {ret}')
        return ret

    def __repr__(self):
        return "Topic(%s)" % list.__repr__(self)


class Broker:
    def __init__(self, topicType: _Topic) -> None:
        self.topics = {}
        self.lock = threading.Lock()
        self.callbackCondition = threading.Condition(self.lock)
        self.topicType = topicType

    def _register(self, key: str):
        if key not in self.topics.keys():
            print(f'{self} registering topic {key}')
            self.topics[key] = self.topicType()

    def registerTopic(self, key: str):
        with self.lock:
            self._register(key)
            
    def registerCallback(self, key, callback, register = True):
        with self.lock:
            if register:
                self._register(key)
            self.topics[key].append(callback)
            print(f'{self} registered callback to {key}')
            self.callbackCondition.notifyAll()

    def sendAndRecieve(self, key: str, register = True, *args, **kwargs) -> list:
        with self.lock:
            if register:
                self._register(key)
            if key in self.topics.keys():
                topic = self.topics[key]
                while not topic:
                    self.callbackCondition.wait()
                return copy.deepcopy( topic(*args, **kwargs) )
            return []

    def send(self, key: str, register = True, *args, **kwargs) -> None:
        with self.lock:
            if register:
                self._register(key)
            if key in self.topics.keys():
                topic = self.topics[key]
                print(f'{self} acquired topic, waiting for callbacks to be registered')
                while not topic:
                    self.callbackCondition.wait()
                print(f'{self} topic ready, executing call to topic {key}')
                topic(*args, **kwargs)


class _ThreadTopic(_Topic):
    pass

@singleton
class ThreadBroker(Broker):
    def __init__(self) -> None:
        super().__init__(_ThreadTopic)


class _LockTopic(_Topic):
    pass

@singleton
class LockBroker(Broker):
    def __init__(self) -> None:
        super().__init__(_LockTopic)


class _ConditionTopic(_Topic):
    pass

@singleton
class ConditionBroker(Broker):
    def __init__(self) -> None:
        super().__init__(_ConditionTopic)



class _GeneralTopic(_Topic):    
    pass

@singleton
class GeneralBroker(Broker):
    def __init__(self) -> None:
        super().__init__(_GeneralTopic)
