# My Package

This is a simple Python package that demonstrates how to create a Python package.

## Installation

You can install this package using pip:

```bash
pip install msvproperties
```

Here is a example usage of the library :

```python

from msvproperties import save_configs, Data, AuthManager, Lead

save_configs(
    env_path="/Users/alireza/Desktop/msvproperties",
    log_path="/Users/alireza/Desktop/msvproperties",
)

data = Data(
    is_auction=True,
    source_name="Auction",
    full_address="123 Main S Lodi, CA 95242",
)

session = AuthManager("username", "password")

Lead(session).start(data)

```
