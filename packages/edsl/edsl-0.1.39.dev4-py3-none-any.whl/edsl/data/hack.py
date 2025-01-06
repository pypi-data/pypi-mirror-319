from edsl.data.CacheEntry import CacheEntry

first = 0
for i in range(0,1000000):
    if i == 0:
        first = CacheEntry.example().key
    if first != "55ce2e13d38aa7fb6ec848053285edb4":
        print(first)
    print(CacheEntry.example().__dict__)
    break