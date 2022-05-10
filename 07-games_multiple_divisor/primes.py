primes = []
for i in range(100):
    prime = True
    for j in range(2, i):
        if not prime: break
        prime = i % j != 0;
    if prime: primes.append(i)
print(primes)