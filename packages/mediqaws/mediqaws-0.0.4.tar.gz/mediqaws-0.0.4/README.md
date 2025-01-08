# [Package Name]

A collection of AWS clients for SmartMediQ.

## Install

[`pip install mediqaws`]

## Usage

```python
from mediqaws.clients import S3

profile_name = "..."
bucket_name = "..."
object_key_prefix = "..."
file_path = "..."

with S3(profile_name=profile_name) as s3:
  object_key = s3.upload(file_path, bucket_name, object_key_prefix)
print(object_key)
```

See more examples under `tests` directory.
