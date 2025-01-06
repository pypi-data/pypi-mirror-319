cdef class MathOperations:
    cpdef int fibonacci(self, int n):
        cdef int a = 0
        cdef int b = 1
        cdef int i
        
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        for i in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    cpdef double factorial(self, int n):
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

