import os
from random import random, randint

from mlflow import log_metric, log_param, log_artifacts
import mlflow
import pathlib
import urllib
import platform


if __name__ == "__main__":
    print("Running mlflow_tracking.py")

#   mlflow.set_tracking_uri(pathlib.Path(os.path.abspath('./mlruns')).as_uri())
#   doesn't work because :
#   path = urllib.parse.urlparse(store_uri).path
#   Windows doesn't work with the path component of the URI

    # Doesn't work because it's supposed to be an URI and then scheme parsing of urllib fails
    #s = os.path.abspath('./mlruns')

    # doesn't work because:
    #       path = urllib.parse.urlparse(store_uri).path
    # windows doesn't work with the path component
    s = pathlib.Path(os.path.abspath('./mlruns')).as_uri()

    s1 = urllib.parse.urlparse(s).path

    s2 = str(pathlib.PureWindowsPath(s1))
    s3 = s2[1:]

    b2 = os.path.exists(s2)
    b3 = os.path.exists(s3)

    p = platform.system()
    is_windows = (platform.system() == 'Windows')

    # mlflow.set_tracking_uri(s)

    log_param("param1", randint(0, 100))

    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")

    log_artifacts("outputs")
