# distributed lock module

This Python package provides a mechanism to acquire and release Redis and MYSQL locks with authentication. It is useful for ensuring that only one process can access a particular resource or execute a critical section of code at a time.

## Features
- Connects to Redis or MySQL with username and password for authentication.
- Acquires a lock, executes a function, and then releases the lock.
- Useful in distributed systems where resource locking is needed.

## Installation

To install the module, use `pip`:

```bash
pip install distributedlock