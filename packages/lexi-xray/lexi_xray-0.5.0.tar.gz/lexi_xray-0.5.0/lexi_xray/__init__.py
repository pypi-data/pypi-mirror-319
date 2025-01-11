# lexi/__init__.py

# Import the version from your setup.py file
from importlib.metadata import version, PackageNotFoundError


# Add the docstring to the package
__doc__ = """
The lexi is a package developed using the Python programming language. The package is
designed to provide a simple list of functions to work with the LEXI dataset. The package has
following usable modules:
    - **get_lexi_data**: This module is used to get the LEXI dataset from the CDAweb website using a
      specified time range.
    - **get_spc_prams**: This module is used to get the spacecraft parameters from the LEXI dataset using
      a specified time range.
    - **calc_exposure_maps**: This module is used to get the exposure maps from the LEXI dataset using a
      specified time range and some other input parameters.
    - **calc_sky_backgrounds**: This module is used to get the sky backgrounds from the LEXI dataset which
      corresponds to the exposure maps. The module uses the exposure maps to get the sky backgrounds.
    - **make_lexi_images**: This module is used to get the LEXI images from the LEXI dataset using a
      specified time range and some other input parameters. The module uses the exposure maps and sky
      backgrounds to get the LEXI images. One can either get a background corrected image or a raw
      image from the data set.

The package development is by the LEXI team at the Boston University and supported by institutes
involved in the development of LEXI payload.
For more information, please visit the LEXI website at https://sites.bu.edu/lexi/ or read the README
file. 
"""

try:
    __version__ = version("lexi_xray")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Import the functions from the lexi package
from .lexi import (
    validate_input,
    download_files_from_github,
    get_lexi_data,
    get_spc_prams,
    calc_exposure_maps,
    calc_sky_backgrounds,
    make_lexi_images,
    array_to_image,
)
