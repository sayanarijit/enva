import enva
import pytest
from os import environ
from unittest.mock import patch


# unset ENVIRONMENT
@patch.dict(environ, {}, clear=True)
def test_undefined():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod=enva.environ("DATABASE_URL"),  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
    )

    assert DATABASE_URL == "postgres://localhost:5432/postgres"


# export ENVIRONMENT=NON_EXISTENT
@patch.dict(environ, {}, clear=True)
def test_default():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
    )

    assert DATABASE_URL == "postgres://localhost:5432/postgres"


# export ENVIRONMENT=DEVELOPMENT
@patch.dict(environ, {"ENVIRONMENT": "DEVELOPMENT"}, clear=True)
def test_dev():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://dev:dev@localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
    )

    assert DATABASE_URL == "postgres://dev:dev@localhost:5432/postgres"


# export ENVIRONMENT=STAGING
@patch.dict(environ, {"ENVIRONMENT": "STAGING"}, clear=True)
def test_stage():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://stage:stage@localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
    )

    assert DATABASE_URL == "postgres://stage:stage@localhost:5432/postgres"


# export ENVIRONMENT=PRODUCTION
@patch.dict(environ, {"ENVIRONMENT": "PRODUCTION"}, clear=True)
def test_prod():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://prod:prod@localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://prod:prod@localhost:5432/postgres"


# export ENVIRONMENT=PRODUCTION
@patch.dict(
    environ,
    {
        "ENVIRONMENT": "PRODUCTION",
        "DATABASE_URL": "postgres://prod:prod@localhost:5432/postgres",
    },
    clear=True,
)
def test_environ():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
        stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
        prod=enva.environ("DATABASE_URL"),  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://prod:prod@localhost:5432/postgres"

    DATABASE_URL = env(
        "postgres://localhost:5432/postgres",  # Default value
        prod=enva.environ("DATABASE_URL"),  # When $ENVIRONMENT == PRODUCTION
    )

    assert DATABASE_URL == "postgres://prod:prod@localhost:5432/postgres"


# export ENVIRONMENT=NON_EXISTENT
@patch.dict(environ, {"ENVIRONMENT": "NON_EXISTENT"}, clear=True)
def test_not_found():

    env = enva.define(
        "ENVIRONMENT", dev="DEVELOPMENT", stage="STAGING", prod="PRODUCTION"
    )

    with pytest.raises(KeyError, match="default"):
        env(
            dev="postgres://dev:dev@localhost:5432/postgres",  # When $ENVIRONMENT == DEVELOPMENT
            stage="postgres://stage:stage@localhost:5432/postgres",  # When $ENVIRONMENT == STAGING
            prod="postgres://prod:prod@localhost:5432/postgres",  # When $ENVIRONMENT == PRODUCTION
        )
