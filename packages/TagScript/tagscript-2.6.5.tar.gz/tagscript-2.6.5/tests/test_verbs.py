import time
import unittest

from TagScriptEngine import Interpreter, adapter, block


class TestVerbFunctionality(unittest.TestCase):
    def setUp(self):
        self.blocks = [
            block.BreakBlock(),
            block.MathBlock(),
            block.RandomBlock(),
            block.RangeBlock(),
            block.StrfBlock(),
            block.AssignmentBlock(),
            block.FiftyFiftyBlock(),
            block.StrictVariableGetterBlock(),
        ]
        self.engine = Interpreter(self.blocks)

    def tearDown(self):
        self.blocks = None
        self.engine = None

    def seen_all(self, string, outcomes, tries=100):
        unique_outcomes = set(outcomes)
        seen_outcomes = set()
        for _ in range(tries):
            outcome = self.engine.process(string).body
            seen_outcomes.add(outcome)

        result = unique_outcomes == seen_outcomes

        if not result:
            print("Error from '" + string + "'")
            print("Seen:")
            for item in seen_outcomes:
                print("> " + str(item))
            print("Expected: ")
            for item in unique_outcomes:
                print(">> " + str(item))

        return result

    def test_random(self):
        # Test simple random
        test = "{random:Hello,Goodbye}"
        expect = ["Hello", "Goodbye"]
        self.assertTrue(self.seen_all(test, expect))

        # Test that it wont crash with a false block
        test = "{random:{ahad},one,two}"
        expect = ["{ahad}", "one", "two"]
        self.assertTrue(self.seen_all(test, expect))

        # Test that inner blocks can use , to sep and outer use ~ without tripping
        # Also testing embedded random
        test = "{random:{random:1,2} cakes~No cakes}"
        expect = ["1 cakes", "2 cakes", "No cakes"]
        self.assertTrue(self.seen_all(test, expect))

        # Test random being able to use a var
        test = "{assign(li):1,2,3,4}{random:{li}}"
        expect = ["1", "2", "3", "4"]
        self.assertTrue(self.seen_all(test, expect))

    def test_fifty(self):
        # Test simple 5050
        test = "Hi{5050: :)}"
        expect = ["Hi", "Hi :)"]
        self.assertTrue(self.seen_all(test, expect))

        # Test simple embedded 5050
        test = "Hi{5050: :){5050: :(}}"
        expect = ["Hi", "Hi :)", "Hi :) :("]
        self.assertTrue(self.seen_all(test, expect))

    def test_range(self):
        # Test simple range
        test = "{range:1-2} cows"
        expect = ["1 cows", "2 cows"]
        self.assertTrue(self.seen_all(test, expect))
        # Test simple float range
        test = "{rangef:1.5-2.5} cows"
        self.assertTrue("." in self.engine.process(test).body)

    def test_math(self):
        test = "{math:100/2}"
        expect = "50.0"  # division implies float
        self.assertEqual(self.engine.process(test).body, expect)

        test = "{math:100**100**100}"  # should 'fail'
        self.assertEqual(self.engine.process(test).body, test)

    def test_misc(self):
        # Test using a variable to get a variable
        data = {
            "pointer": adapter.StringAdapter("message"),
            "message": adapter.StringAdapter("Hello"),
        }
        test = "{{pointer}}"
        self.assertEqual(self.engine.process(test, data).body, "Hello")

        test = r"\{{pointer}\}"
        self.assertEqual(self.engine.process(test, data).body, r"\{message\}")

        test = "{break(10==10):Override.} This is my actual tag!"
        self.assertEqual(self.engine.process(test, data).body, "Override.")

    def test_cuddled_strf(self):
        t = time.gmtime()
        huggle_wuggle = time.strftime("%y%y%y%y")
        self.assertEqual(self.engine.process("{strf:%y%y%y%y}").body, huggle_wuggle)

    def test_basic_strf(self):
        year = time.strftime("%Y")
        self.assertEqual(self.engine.process("Hehe, it's {strf:%Y}").body, f"Hehe, it's {year}")
