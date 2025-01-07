import unittest

from frozendict import frozendict

from argshold.core import FrozenArgumentHolder


class TestFrozenArgumentHolder(unittest.TestCase):

    def test_initialization(self):
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        self.assertEqual(holder.args, (1, 2))
        self.assertEqual(holder.kwargs, frozendict(a=3, b=4))

    def test_equality(self):
        holder1 = FrozenArgumentHolder(1, 2, a=3, b=4)
        holder2 = FrozenArgumentHolder(1, 2, a=3, b=4)
        holder3 = FrozenArgumentHolder(1, 2, a=3)
        self.assertEqual(holder1, holder2)
        self.assertNotEqual(holder1, holder3)

    def test_hash(self):
        holder1 = FrozenArgumentHolder(1, 2, a=3, b=4)
        holder2 = FrozenArgumentHolder(1, 2, a=3, b=4)
        self.assertEqual(hash(holder1), hash(holder2))

    def test_len(self):
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        self.assertEqual(len(holder), 4)

    def test_repr(self):
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        self.assertEqual(repr(holder), "FrozenArgumentHolder(1, 2, a=3, b=4)")

    def test_immutable_attributes(self):
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        with self.assertRaises(AttributeError):
            holder.args = (3, 4)
        with self.assertRaises(AttributeError):
            holder.kwargs = frozendict(c=5)

    def test_call(self):
        def sample_function(x, y, a=0, b=0):
            return x + y + a + b

        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        result = holder.call(sample_function)
        self.assertEqual(result, 10)

    def test_copy(self):
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        copied = holder.copy()
        self.assertEqual(holder, copied)
        self.assertIsNot(holder, copied)

    def test_partial(self):
        def sample_function(x, y, a=0, b=0):
            return x + y + a + b

        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        partial_func = holder.partial(sample_function)
        self.assertEqual(partial_func(), 10)

    def test_partialmethod(self):
        class SampleClass:
            def sample_method(self, x, y, a=0, b=0):
                return x + y + a + b

        obj = SampleClass()
        holder = FrozenArgumentHolder(1, 2, a=3, b=4)
        partial_method = holder.partialmethod(obj.sample_method)
        self.assertEqual(partial_method(obj), 10)


if __name__ == "__main__":
    unittest.main()
