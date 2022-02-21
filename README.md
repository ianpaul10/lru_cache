# lru_cache

A simple example setup for a Least Recently Used Cache system.

This solution utilizes a dictionary paired with a doubly linked list.

Note: this is not intended to be used in production, just as an example of how one could implement a similar system in production.

## Testing

Note: requires docker.

Run `bash bin/run_tests.sh` from the root directory.

Tests consist of basic unit tests that ensure the functionality of `src/ec_lru_cache.py` works as expected.

## Production-izing

If one were to production-ize such a system, below are collection of possible steps that could be taken:

1. Build out a proper deployment/installation process for importing it into other apps (possibly via pip).
2. Update the main dictionary's key from an `int` to something like a GUID or a more robust key structure. `int` was chosen as the initial implementation out of simplicity & to make it easier to follow during testing.
3. The main dictionary's value can also be updated to something more specific (e.g. config settings, dict, GPS coordinates, etc.)
4. If the system was to be implemented in a distributed setting, abstracting the dictionary & node objects outside the context of the `ec_lru_cache.py` and into a distributed cache (possibly [redis](https://redis.io/)) is recommended. This would allow for accessing & updating the cache to scale effectively as the number of requests grows. This comes at the cost of complexity & increased latency.
