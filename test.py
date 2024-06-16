def fibonacci(n):
    a, b = 0, 1
    while n > 0:
        yield a
        a, b = b, a + b
        n -= 1

# Using the generator
for num in fibonacci(1000000):
    print(num)
