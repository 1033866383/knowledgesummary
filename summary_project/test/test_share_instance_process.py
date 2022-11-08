# 多进程共享对象并修改对象内容
import pickle
from multiprocessing import Process, Queue


def before(queue) -> None:
    obj = list()
    obj.append(dict())
    obj_s = pickle.dumps(obj)
    queue.put(obj_s)


def after(queue: Queue) -> None:
    res = queue.get()
    obj = pickle.loads(res)
    print(obj, "rec")
    obj.append(set())
    res = pickle.dumps(obj)
    queue.put(res)


if __name__ == '__main__':
    q = Queue()
    p = Process(target=before, args=(q,))
    p.start()
    p.join()
    p1 = Process(target=after, args=(q,))
    p1.start()
    p1.join()
    print("end")
    print(pickle.loads(q.get()))  # prints "[42, None, 'hello']"
