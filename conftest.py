import pytest
import user_emulation
import logging


@pytest.fixture(scope="session")
def user():
    user = user_emulation.User()
    yield user


@pytest.fixture()
def log_test_borders():
    logging.info("################################## START TEST ##################################")
    yield
    logging.info("################################### END TEST ###################################")
