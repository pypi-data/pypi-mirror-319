import pickle
import msgpack


def dump_pkl(fpath, var_lis):
    with open(fpath, 'wb') as f:
        pickle.dump(var_lis, f)


def load_pkl(fpath):
    with open(fpath, 'rb') as f:
        return pickle.load(f)


def dump_msgpack(path, data):
    with open(path, "wb") as f:
        f.write(msgpack.packb(data))


def load_msgpack(path):
    with open(path, "rb") as f:
        data = msgpack.unpackb(f.read())
        return data
