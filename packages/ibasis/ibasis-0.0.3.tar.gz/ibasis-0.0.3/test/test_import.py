from ibasis import idtbs


class TestUnit():
    def __init__(self):
        self.pdir = 'tmp'

    def test_data_dir(self):
        dd = idtbs.DataDir().init_pdir(self.pdir)
        dd.add_attr(test_dir=dd.join(name='pdir', path='test'))
        dd.add_attr(test_path=dd.join(name='pdir', path='test.txt'))
        print(dd)

    def test_data_dirDT(self):
        dd = idtbs.DataDir().init_pdir(self.pdir)
        dd.add_attr(test_dir=dd.join(name='pdir', path='test'))
        dd.add_attr(test_path=dd.join(name='pdir', path='test.txt'))
        print(dd)


if __name__ == "__main__":
    tu = TestUnit()
    tu.test_data_dir()
    tu.test_data_dirDT()
