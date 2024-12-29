
import unittest
import palindrome
from sympy.ntheory import is_palindromic

class TestPalindrome(unittest.TestCase):
    def test_0_floor(self):
        self.assertEqual(palindrome.pal_floor(0), 0)
        self.assertEqual(palindrome.pal_floor(10), 9)
        self.assertEqual(palindrome.pal_floor(11), 11)
        self.assertEqual(palindrome.pal_floor(21), 11)
        self.assertEqual(palindrome.pal_floor(99), 99)
        self.assertEqual(palindrome.pal_floor(100), 99)
        self.assertEqual(palindrome.pal_floor(110), 101)
        self.assertEqual(palindrome.pal_floor(135), 131)
        self.assertEqual(palindrome.pal_floor(1000), 999)
        self.assertEqual(palindrome.pal_floor(1041), 1001)
        for i in range(100, 10_000):
            self.assertTrue(palindrome.pal_floor(i) <= i)
            self.assertTrue(is_palindromic(palindrome.pal_floor(i)))

    def test_1_ceil(self):
        self.assertEqual(palindrome.pal_ceil(0), 0)
        self.assertEqual(palindrome.pal_ceil(10), 11)
        self.assertEqual(palindrome.pal_ceil(11), 11)
        self.assertEqual(palindrome.pal_ceil(21), 22)
        self.assertEqual(palindrome.pal_ceil(99), 99)
        self.assertEqual(palindrome.pal_ceil(110), 111)
        self.assertEqual(palindrome.pal_ceil(135), 141)
        self.assertEqual(palindrome.pal_ceil(1041), 1111)
        for i in range(100, 10_000):
            self.assertTrue(palindrome.pal_ceil(i) >= i)
            self.assertTrue(is_palindromic(palindrome.pal_ceil(i)))

    def test_2_prev_next(self):
        self.assertEqual(palindrome.next_pal(999), 1001)
        self.assertEqual(palindrome.prev_pal(999), 989)
        self.assertEqual(palindrome.next_pal(0), 1)
        self.assertEqual(palindrome.prev_pal(1), 0)

    def test_3_pal_iterator(self):
        test_cases = [(53,9999), (123, 1010), (10, 1000), (9, 999)]
        for first, last in test_cases:
            sum1 = 0
            for i in range(first, last):
                if is_palindromic(i):
                    sum1 += i
            sum2 = 0
            for n in palindrome.pal_iterator(first, last):
                sum2 += n
            #print(first, last, sum1, sum2)
            self.assertEqual(sum1, sum2)
       
    def test_4_pal_div_iterator_(self):
        test_cases = [(67, 9, 9_999_999), 
                      (81, 99_999_999, 10**9), 
                      (43, 10**6, 10**7)]
        for n, first, last in test_cases:
            #print(n, first, last)
            sum1 = 0
            for i in palindrome.pal_iterator(first, last):
                if i%n==0:
                    sum1 += i
            sum2 = 0
            for i in palindrome.pal_div_iterator(n, first, last):
                sum2 += i
            self.assertEqual(sum1, sum2) 


if __name__ == '__main__':
    unittest.main()