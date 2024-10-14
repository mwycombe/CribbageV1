#selftest.py
#
# see how declared class level vars are accessed
class SelfTest:
    myi = 3.14159
    def try_myi (self):
        print (myi)
        self.local = 1.2345
        print (self.local)
    def try_local(self):
        print (self.local)
if __name__ == '__main__':
    st = SelfTest()
    st.try_myi()
    print (st.myi)
    st.try_local()
