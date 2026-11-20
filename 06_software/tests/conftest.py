import os
import tempfile

# Base de datos temporal por sesión de pruebas (antes de importar la app)
os.environ.setdefault("DSS_DB", tempfile.mktemp(prefix="dss_test_", suffix=".db"))
