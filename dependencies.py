
from sverchok.dependencies import SvDependency

ex_dependencies = dict()

try:
    import sverchok
    from sverchok.utils.logging import info, error, debug

    from sverchok.dependencies import (
            SvDependency,
            ensurepip,
            pip, scipy, geomdl, skimage,
            mcubes, circlify,
            FreeCAD
        )

    sverchok_d = ex_dependencies["sverchok"] = SvDependency(None, "https://github.com/nortikin/sverchok")
    sverchok_d.module = sverchok
    sverchok_d.message =  "Sverchok addon is available"
except ImportError:
    message =  "Sverchok addon is not available. Sverchok-Open3d will not work."
    print(message)
    sverchok = None

opend3D_d = ex_dependencies["open3d"] = SvDependency("open3d", "http://www.open3d.org/")
opend3D_d.pip_installable = True
try:
    import open3d
    opend3D_d.message = "open3d package is available"
    opend3D_d.module = open3d
except ImportError:
    opend3D_d.message = "open3d package is not available, the addon will not work"
    info(opend3D_d.message)
    open3d = None
