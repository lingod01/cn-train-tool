#!/opt/app/dj_train/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/opt/app/dj_train/releases/current/")
sys.path.insert(0, "/opt/app/dj_train/releases/current/dj_train")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "dj_train.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
