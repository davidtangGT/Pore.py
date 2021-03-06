r"""

===============================================================================
io
===============================================================================

**Convert Between Formats**

.. autosummary::

    porespy.io.to_vtk
    porespy.io.dict_to_vtk
    porespy.io.to_palabos
    porespy.io.to_openpnm
    porespy.io.openpnm_to_im
    porespy.io.to_stl
    porespy.io.spheres_to_comsol
    porespy.io.to_openfoam

.. autofunction:: to_vtk
.. autofunction:: dict_to_vtk
.. autofunction:: to_palabos
.. autofunction:: to_openpnm
.. autofunction:: openpnm_to_im
.. autofunction:: to_stl
.. autofunction:: spheres_to_comsol
.. autofunction:: to_openfoam


"""

from .__funcs__ import to_vtk
from .__funcs__ import dict_to_vtk
from .__funcs__ import to_palabos
from .__funcs__ import to_openpnm
from .__funcs__ import openpnm_to_im
from .__funcs__ import to_stl
from .__funcs__ import spheres_to_comsol
from .__openfoam__ import to_openfoam
