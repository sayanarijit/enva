# enva

A simple, consolidated `settings.py`.

Usage:

```python
# export ENVIRONMENT=PRODUCTION

import os
import enva

# You can define as many environments as you want.
env = enva.define("ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION")

DATABASE_URL = env(
    "postgres://localhost:5432/postgres",                    # Default value
    dev="postgres://dev:dev@localhost:5432/postgres",        # When $ENVIRONMENT == DEVELOPMENT
    stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
    prod=os.environ["ENVIRONMENT"],                          # When $ENVIRONMENT == PRODUCTION
)

print(DATABASE_URL)
# postgres://prod:prod@localhost:5432/postgres
```
