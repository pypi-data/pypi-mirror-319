from ._core import MathOperations

_math_ops = MathOperations()
fibonacci = _math_ops.fibonacci
factorial = _math_ops.factorial

__all__ = ['fibonacci', 'factorial']

