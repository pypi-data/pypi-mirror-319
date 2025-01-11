# storage-bridge
A Python library providing a typeclass-based abstraction for managing diverse storage backends. Storage Manager simplifies and standardizes interactions with storage systems, enabling seamless access to local files, in-memory storage, and cloud-based resources.

Key Features
Unified Interface: Interact with various storage backends using a consistent API.
Extensible Framework: Add custom storage backends with minimal implementation effort.
Mock-Friendly: Built-in support for testing with mock storage or local solutions.
Batch and Transactional Support: Perform bulk operations or enable transactional workflows.
Why Use Storage Manager?
Modern applications often require integration with multiple storage systems—local, remote, or in-memory. Storage Manager homogenizes these interactions, letting developers focus on application logic rather than backend differences.

## Installation
Install via pip:

```bash
pip install storage_bridge
```

## Usage
### Core API
The Storage typeclass provides the core methods:

save(key, value): Save a value under a key.
load(key): Retrieve a value by key.
delete(key): Remove a key-value pair.
list_keys(): List all keys in the storage.
Additional methods like exists, update, save_batch, and backup are derived from these core methods.

#### Example: File-Based Storage
```python
from storage_bridge.implementation import FileStorage

# Create a file-based storage backend
store = FileStorage(filepath='data.json')

# Save and load data
store.save('user', {'name': 'Alice', 'age': 30})
print(store.load('user'))  # Output: {'name': 'Alice', 'age': 30}

# List keys
print(store.list_keys())  # Output: ['user']

# Delete data
store.delete('user')
```

#### Example: In-Memory Storage
```python
from storage_bridge.implementation import MemoryStorage

# Create an in-memory storage backend
memory_store = MemoryStorage()

# Save and retrieve data
memory_store.save('session', {'token': 'abc123'})
print(memory_store.load('session'))  # Output: {'token': 'abc123'}
```

#### Testing with Mock Storage
```python
from storage_bridge.implementation import MemoryStorage

def test_storage():
    mock_store = MemoryStorage()
    mock_store.save('test_key', 'test_value')
    assert mock_store.load('test_key') == 'test_value'
    assert 'test_key' in mock_store.list_keys()
    mock_store.delete('test_key')
```

### Extending Storage Manager
To create a custom storage backend, subclass Storage and implement the core methods (save, load, delete, list_keys).

Example: Custom Storage
```python
from storage_bridge.typeclass import Storage

class CustomStorage(Storage):
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def load(self, key):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found.")
        return self.data[key]

    def delete(self, key):
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(f"Key '{key}' not found.")

    def list_keys(self):
        return list(self.data.keys())
```

### Roadmap
Add cloud storage integrations (AWS S3, Google Cloud Storage, Azure Blob Storage).
Introduce advanced features like data versioning and compression.
Expand support for transactional and distributed workflows.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License
storage-bridge is licensed under the MIT License. See LICENSE for more details.
