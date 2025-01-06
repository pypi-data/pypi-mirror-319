# tinyhash
Generate a tiny hash using RFC 4648 base64url format


```python
from datetime import datetime, timezone
from tinyhash import small_hash
now = datetime.now(timezone.utc)
my_hash = small_hash(now.strftime("%Y%m%d_%H%M%S"))
```
