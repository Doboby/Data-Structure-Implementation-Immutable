from typing import Callable, TypeVar, Any, Generic, List


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value


VI = TypeVar("VI", Node, str, int, float, object, bool, Any)


class Hashdic(Generic[VI]):
    empty = Node()

    def __init__(self, Hashcode: int = 13):
        self.code = Hashcode
        self.key_set: List = []
        self.data: List[VI] = [self.empty for _ in range(Hashcode)]
        self.size = 0

    def __eq__(self, other: VI) -> VI:
        if other is None:
            return False
        for x in range(0, len(self.data)):
            if self.data[x] != self.empty:
                if self.data[x].key != -1:
                    if other.data[x] != other.empty:
                        if other.data[x].key != -1:
                            if self.data[x].key != other.data[x].key:
                                return False
                            if self.data[x].value != other.data[x].value:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    if other.data[x] != other.empty:
                        if other.data[x].key != -1:
                            return False
            else:
                if other.data[x] != other.empty:
                    if other.data[x].key != -1:
                        return False
        return True

    def __iter__(self):
        return Hashdic_Iterator(self.data)


class Hashdic_Iterator:
    empty = object()

    def __init__(self, data: List[VI]):
        self.index = 0
        self.iterator_list = []
        for i in range(0, len(data)):
            if (not data[i] is self.empty) \
                    and data[i].key != -1:
                self.iterator_list.append(
                    Node(data[i].key, data[i].value))

    def __next__(self) -> Node:
        try:
            temp = self.iterator_list[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return temp

    def __iter__(self):
        return self


def cons(Hd: Hashdic, key: VI, value: VI) -> Hashdic:

    new = Hashdic()
    new.size = Hd.size
    new.key_set = Hd.key_set.copy()

    if key is None:
        raise Exception("key cant be NULL")
    # 先将Hd的数据 复制到 new 里面 再添加新的元素 k v
    for x in range(0, len(Hd.data)):
        if Hd.data[x] != Hd.empty and Hd.data[x].key != -1:
            new.data[x] = Node(Hd.data[x].key, Hd.data[x].value)

    if key in new.key_set:
        for temp in new.data:
            if temp != new.empty and temp.key == key:
                temp.value = value
                return new
    else:
        hash_value = key.__hash__() % new.code
        kv_entry = Node(key, value)
        if new.data[hash_value] == new.empty \
                or new.data[hash_value].key == -1:
            new.data[hash_value] = kv_entry
            new.key_set.append(key)
            new.size = new.size + 1
            return new
        else:
            i = 0
            while i < new.size:
                index = (hash_value + 1).__hash__() % new.code
                hash_value = index
                if new.data[index] == new.empty \
                        or new.data[hash_value].key == -1:
                    new.data[index] = kv_entry
                    new.key_set.append(key)
                    new.size = new.size + 1
                    return new
                else:
                    i += 1
    return new


def remove(Hd: Hashdic, key: VI) -> Hashdic:

    if key is None:
        raise Exception("key cant be NULL")
    new = Hashdic()
    new.size = Hd.size
    new.key_set = Hd.key_set.copy()
    flag = False
    for x in range(0, len(Hd.data)):
        if Hd.data[x] != Hd.empty and Hd.data[x].key != -1:
            new.data[x] = Node(Hd.data[x].key, Hd.data[x].value)

    for x in range(0, len(new.data)):
        if new.data[x] != new.empty and new.data[x].key == key:
            new.key_set.remove(new.data[x].key)
            new.data[x].key = -1
            new.size -= 1
            flag = True
    if not flag:
        raise Exception("no such key")
    return new


def length(Hd: Hashdic) -> VI:

    if Hd:
        return Hd.size
    else:
        return -1


def to_list(h: Hashdic) -> List[VI]:

    outlist: List[VI] = []
    if not h:
        return outlist
    for x in range(0, len(h.key_set)):
        v = find(h, h.key_set[x])
        outlist.append(v)
    return outlist


def from_list(a: List[VI]) -> Hashdic:
    p = Hashdic()
    for k, v in enumerate(a):
        p = cons(p, k+1, v)
    return p


def iterator(hp: Hashdic) -> Callable:
    iterator_list = []
    for i in range(0, len(hp.key_set)):
        v = find(hp, hp.key_set[i])
        iterator_list.append(v)
    na = 0

    def next():
        nonlocal na
        t = na
        na = na + 1
        if t >= len(iterator_list):
            return -1
        return iterator_list[t]
    return next


def member(mp: Hashdic, key: VI) -> VI:
    if key is None:
        return False
    for x in range(0, len(mp.data)):
        if mp.data[x] != mp.empty:
            if mp.data[x].key == key:
                return True
    return False


def find(mp: Hashdic, key: VI) -> VI:

    if key is None:
        raise Exception("key cant be NULL")
        return None
    for x in range(0, len(mp.data)):
        if mp.data[x] != mp.empty:
            if mp.data[x].key == key:
                return mp.data[x].value
    raise Exception("no such element")
    return None


def mempty(h: Hashdic) -> Hashdic:

    return Hashdic()


def mconcat(a: Hashdic, b: Hashdic) -> Hashdic:

    if not a and not b:
        return a
    new = Hashdic()
    if not a:
        new.size = b.size
        new.key_set = b.key_set.copy()
        for x in range(0, len(b.data)):
            if b.data[x] != b.empty and b.data[x].key != -1:
                new.data[x] = Node(b.data[x].key, b.data[x].value)
        return new
    elif not b:
        new.size = a.size
        new.key_set = a.key_set.copy()
        for x in range(0, len(a.data)):
            if a.data[x] != a.empty and a.data[x].key != -1:
                new.data[x] = Node(a.data[x].key, a.data[x].value)
        return new
    else:
        for x in range(0, len(b.key_set)):
            v = find(b, b.key_set[x])
            a = cons(a, b.key_set[x], v)
        return a


def map(a: Hashdic, f: Callable) -> Hashdic:

    new = Hashdic()
    new.size = a.size
    new.key_set = a.key_set.copy()

    for x in range(0, len(a.data)):
        if a.data[x] != a.empty and a.data[x].key != -1:
            new.data[x] = Node(a.data[x].key, a.data[x].value)

    for d in range(0, len(new.data)):
        if new.data[d] != new.empty:
            if new.data[d].key != -1:
                new.data[d].value = f(new.data[d].value)
    return new


def reduce(a: Hashdic, f: Callable, state: VI) -> VI:

    instate = state
    for x in range(0, len(a.data)):
        if a.data[x] != a.empty:
            if a.data[x].key != -1:
                instate = f(instate, a.data[x].value)
    return instate


def filter(a: Hashdic, f: Callable) -> List[VI]:

    result = to_list(a)
    for x in range(0, len(a.data)):
        if a.data[x] != a.empty:
            if a.data[x].key != -1:
                value = a.data[x].value
                flag = f(value)
                if flag:
                    result.remove(value)
    return result
