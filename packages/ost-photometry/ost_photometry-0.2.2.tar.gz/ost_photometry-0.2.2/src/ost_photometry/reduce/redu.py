############################################################################
#                               Libraries                                  #
############################################################################

import sys

import shutil

from pytimedinput import timedInput

from pathlib import Path

import numpy as np

from scipy.ndimage import median_filter

import ccdproc as ccdp

from astropy.stats import mad_std
from astropy.nddata import CCDData, StdDevUncertainty
import astropy.units as u

import astroalign as aa

from . import utilities, plots

from .. import checks, style, terminal_output, calibration_parameters

from .. import utilities as aux_general

from ..analyze.utilities import Executor


############################################################################
#                           Routines & definitions                         #
############################################################################

def reduce_main(
        image_path: str, output_dir: str,
        image_type_dir: dict[str, list[str]] | None = None,
        gain: float | None = None, read_noise: float | None = None,
        dark_rate: float | None = None, rm_cosmic_rays: bool = True,
        mask_cosmic_rays: bool = False, saturation_level: float | None = None,
        limiting_contrast_rm_cosmic_rays: float = 5.,
        sigma_clipping_value_rm_cosmic_rays: float = 4.0,
        scale_image_with_exposure_time: bool = True,
        reference_image_id: int = 0, enforce_bias: bool = False,
        add_hot_bad_pixel_mask: bool = True, shift_method: str = 'skimage',
        n_cores_multiprocessing: int | None = None, stack_images: bool = True,
        estimate_fwhm: bool = False, shift_all: bool = False,
        exposure_time_tolerance: float = 0.5, stack_method: str = 'average',
        dtype_image_stacking: str | np.dtype | None = None,
        target_name: str | None = None, find_wcs: bool = True,
        wcs_method: str = 'astrometry', find_wcs_of_all_images: bool = False,
        force_wcs_determination: bool = False,
        rm_outliers_image_shifts: bool = True,
        filter_window_image_shifts: int = 25,
        threshold_image_shifts: float = 10., temperature_tolerance: float = 5.,
        plot_dark_statistic_plots: bool = False,
        plot_flat_statistic_plots: bool = False,
        ignore_readout_mode_mismatch: bool = False, debug: bool = False
        ) -> None:
    """
    Main reduction routine: Creates master images for bias, darks,
                            flats, reduces the science images and trims
                            them to the same filed of view.

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be stored

    image_type_dir
        Image types of the images. Possibilities: bias, dark, flat,
        light
        Default is ``None``.

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``None``.

    dark_rate
        Dark rate in e-/pix/s:
        Default is ``None``.

    rm_cosmic_rays
        If True cosmics rays will be removed.
        Default is ``True``.

    mask_cosmic_rays
        If True cosmics will ''only'' be masked. If False the
        cosmics will be removed from the input image and the mask will
        be added.
        Default is ``False``.

    saturation_level
        Saturation limit of the camera chip.
        Default is ``None``.

    limiting_contrast_rm_cosmic_rays
        Parameter for the cosmic ray removal: Minimum contrast between
        Laplacian image and the fine structure image.
        Default is ``5``.

    sigma_clipping_value_rm_cosmic_rays
        Parameter for the cosmic ray removal: Fractional detection limit
        for neighboring pixels.
        Default is ``4.5``.

    scale_image_with_exposure_time
        If True the image will be scaled with the exposure time.
        Default is ``True``.

    reference_image_id
        ID of the image that should be used as a reference
        Default is ``0``.

    enforce_bias
        If True the usage of bias frames during the reduction is
        enforced if possible.
        Default is ``False``.

    add_hot_bad_pixel_mask
        If True add hot and bad pixel mask to the reduced science
        images.
        Default is ``True``.

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation with skimage
        Default is ``skimage``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.

    stack_images
        If True the individual images of each filter will be stacked and
        those images will be aligned to each other.
        Default is ``True``.

    estimate_fwhm
        If True the FWHM of each image will be estimated.
        Default is ``False``.

    shift_all
        If False shifts between images are only calculated for images of
        the same filter. If True shifts between all images are
        estimated.
        Default is ``False``.

    exposure_time_tolerance
        Tolerance between science and dark exposure times in s.
        Default is ``0.5``s.

    stack_method
        Method used for combining the images.
        Possibilities: ``median`` or ``average`` or ``sum``
        Default is ``average`.

    dtype_image_stacking
        dtype that should be used while combining the images.
        Default is ''None'' -> None is equivalent to float64

    target_name
        Name of the target. Used for file selection.
        Default is ``None``.

    find_wcs
        If `True` the WCS will be determined for the images.
        Default is ``True``.

    wcs_method
        Method to use for WCS determination.
        Possibilities are 'astrometry', 'astap', and 'twirl'
        Default is ``astrometry``.

    find_wcs_of_all_images
        If `True` the WCS will be calculated for each image
        individually.
        Default is ``False``.

    force_wcs_determination
        If ``True`` a new WCS determination will be calculated even if
        a WCS is already present in the FITS Header.
        Default is ``False``.

    rm_outliers_image_shifts
        If True outliers in the image shifts will be detected and removed.
        Default is ``True``.

    filter_window_image_shifts
        Width of the median filter window
        Default is ``25``.

    threshold_image_shifts
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    temperature_tolerance
        The images are required to have the temperature. This value
        specifies the temperature difference that is acceptable.
        Default is ``5.``.

    plot_dark_statistic_plots
        If True some plots showing some statistic on the dark frames are
        created.
        Default is ``False``

    plot_flat_statistic_plots
        If True some plots showing some statistic on the flat frames are
        created.
        Default is ``False``

    ignore_readout_mode_mismatch
        If set to `True` a mismatch of the detected readout modes will
        be ignored.
        Default is ``False``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.
    """
    ###
    #   Prepare reduction
    #
    #   Sanitize the provided paths
    file_path = Path(image_path)
    output_path = Path(output_dir)

    #   Get image file collection
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Get image types
    if image_type_dir is None:
        image_type_dir = calibration_parameters.get_image_types()

    #   Except if image collection is empty
    if not image_file_collection.files:
        raise RuntimeError(
            f'{style.Bcolors.FAIL}No images found -> EXIT\n'
            f'\t=> Check paths to the images!{style.Bcolors.ENDC}'
        )

    #   Get image types
    ifc_image_types = set(image_file_collection.summary['imagetyp'])

    #   TODO: Add a completeness check so that all science images have
    #         the necessary flats. Add here or in utilities.

    #   Check exposure times:   Successful if dark frames with ~ the same
    #                           exposure time are available all flat and
    #                           science
    #   Dark times
    dark_times = utilities.get_exposure_times(
        image_file_collection,
        image_type_dir['dark'],
    )

    #   Flat times
    flat_times = utilities.get_exposure_times(
        image_file_collection,
        image_type_dir['flat'],
    )

    #   Science times
    science_times = utilities.get_exposure_times(
        image_file_collection,
        image_type_dir['light'],
    )

    #   Check if bias frames are available
    bias_true = np.any(
        [True if t in ifc_image_types else False for t in image_type_dir['bias']]
    )

    #   Check flats
    image_scaling_required = utilities.check_exposure_times(
        image_file_collection,
        image_type_dir['flat'],
        flat_times,
        dark_times,
        bias_true,
        exposure_time_tolerance=exposure_time_tolerance,
    )

    #   Check science exposures
    image_scaling_required = image_scaling_required | utilities.check_exposure_times(
        image_file_collection,
        image_type_dir['light'],
        science_times,
        dark_times,
        bias_true,
        exposure_time_tolerance=exposure_time_tolerance,
    )

    ###
    #   Get camera specific parameters
    #
    image_parameters = utilities.get_instrument_info(
        image_file_collection,
        temperature_tolerance,
        ignore_readout_mode_mismatch=ignore_readout_mode_mismatch,
    )
    instrument = image_parameters[0]
    readout_mode = image_parameters[1]
    gain_setting = image_parameters[2]
    pixel_bit_value = image_parameters[3]
    temperature = image_parameters[4]

    if (read_noise is None or gain is None or dark_rate is None
            or saturation_level is None):
        camera_info = calibration_parameters.camera_info(
            instrument,
            readout_mode,
            temperature,
            gain_setting=gain_setting,
        )
        if read_noise is None:
            read_noise = camera_info[0]
        if gain is None:
            gain = camera_info[1]
        if dark_rate is None:
            dark_rate = camera_info[2]
        if saturation_level is None:
            saturation_level = pow(2, pixel_bit_value) - 1

    ###
    #   Check master files on disk
    #
    #   Get all filter
    filters = set(
        image_file_collection.summary['filter'][
            np.invert(image_file_collection.summary['filter'].mask)
        ]
    )

    #   Check is master files already exist
    master_available = utilities.check_master_files_on_disk(
        output_path,
        image_type_dir,
        dark_times,
        filters,
        image_scaling_required,
    )

    mk_new_master_files = True
    if master_available:
        user_input, timed_out = timedInput(
            f"{style.Bcolors.OKBLUE}   Master files are already calculated."
            f" Should these files be used? [yes/no] {style.Bcolors.ENDC}",
            timeout=30,
        )
        if timed_out:
            user_input = 'n'

        if user_input in ['y', 'yes']:
            mk_new_master_files = False

    #   Set master boolean for bias subtraction
    rm_bias = True if image_scaling_required or enforce_bias else False

    if mk_new_master_files:
        ###
        #   Reduce bias
        #
        if rm_bias:
            terminal_output.print_to_terminal(
                "Create master bias...",
                indent=1,
            )
            master_bias(file_path, output_path, image_type_dir)

        ###
        #   Master dark and master flat darks
        #
        terminal_output.print_to_terminal("Create master darks...", indent=1)

        if rm_bias:
            #   Reduce dark frames and apply bias subtraction
            reduce_dark(
                file_path,
                output_path,
                image_type_dir,
                gain=gain,
                read_noise=read_noise,
                n_cores_multiprocessing=n_cores_multiprocessing,
            )

            #   Set dark path
            dark_path = Path(output_path / 'dark')
        else:
            dark_path = file_path

        #   Create master dark
        master_dark(
            dark_path,
            output_path,
            image_type_dir,
            gain=gain,
            read_noise=read_noise,
            dark_rate=dark_rate,
            plot_plots=plot_dark_statistic_plots,
            debug=debug,
            n_cores_multiprocessing=n_cores_multiprocessing,
        )

        ###
        #   Master flat
        #
        terminal_output.print_to_terminal("Create master flat...", indent=1)

        #   Reduce flats
        reduce_flat(
            file_path,
            output_path,
            image_type_dir,
            gain=gain,
            read_noise=read_noise,
            rm_bias=rm_bias,
            exposure_time_tolerance=exposure_time_tolerance,
            debug=debug,
            n_cores_multiprocessing=n_cores_multiprocessing,
        )

        #   Create master flat
        master_flat(
            Path(output_path / 'flat'),
            output_path,
            image_type_dir,
            plot_plots=plot_flat_statistic_plots,
            debug=debug,
            # n_cores_multiprocessing=n_cores_multiprocessing,
            n_cores_multiprocessing=1,
        )

    ###
    #   Image reduction & stacking (calculation of image shifts, etc. )
    #
    terminal_output.print_to_terminal("Reduce science images...", indent=1)

    reduce_light(
        file_path,
        output_path,
        image_type_dir,
        rm_cosmic_rays=rm_cosmic_rays,
        mask_cosmics=mask_cosmic_rays,
        gain=gain,
        read_noise=read_noise,
        limiting_contrast_rm_cosmic_rays=limiting_contrast_rm_cosmic_rays,
        sigma_clipping_value_rm_cosmic_rays=sigma_clipping_value_rm_cosmic_rays,
        saturation_level=saturation_level,
        rm_bias=rm_bias,
        verbose=debug,
        add_hot_bad_pixel_mask=add_hot_bad_pixel_mask,
        exposure_time_tolerance=exposure_time_tolerance,
        target_name=target_name,
        scale_image_with_exposure_time=scale_image_with_exposure_time,
        n_cores_multiprocessing=n_cores_multiprocessing,
    )

    ###
    #   Calculate and apply image shifts for individual filters or all
    #   images
    #
    terminal_output.print_to_terminal(
        "Trim images to the same field of view...",
        indent=1,
    )
    if shift_all:
        shift_all_images(
            output_path / 'light',
            output_path,
            image_type_dir['light'],
            reference_image_id=reference_image_id,
            shift_method=shift_method,
            n_cores_multiprocessing=n_cores_multiprocessing,
            rm_outliers=rm_outliers_image_shifts,
            filter_window=filter_window_image_shifts,
            threshold=threshold_image_shifts,
            instrument=instrument,
            debug=debug,
        )
    else:
        shift_image(
            output_path / 'light',
            output_path,
            image_type_dir['light'],
            reference_image_id=reference_image_id,
            shift_method=shift_method,
            n_cores_multiprocessing=n_cores_multiprocessing,
            rm_outliers=rm_outliers_image_shifts,
            filter_window=filter_window_image_shifts,
            threshold=threshold_image_shifts,
            instrument=instrument,
            debug=debug,
        )

    if find_wcs and find_wcs_of_all_images:
        ###
        #   Determine WCS and add it to all reduced images
        #
        terminal_output.print_to_terminal("Determine WCS ...", indent=1)
        utilities.determine_wcs_all_images(
            output_path / 'shifted_and_trimmed',
            output_path / 'shifted_and_trimmed',
            wcs_method=wcs_method,
            force_wcs_determination=force_wcs_determination,
        )

    if estimate_fwhm:
        ###
        #   Estimate FWHM
        #
        terminal_output.print_to_terminal("Estimate FWHM ...", indent=1)
        utilities.estimate_fwhm(
            output_path / 'shifted_and_trimmed',
            output_path,
            image_type_dir['light'],
        )

    if stack_images:
        ###
        #   Stack images of the individual filters
        #
        terminal_output.print_to_terminal(
            "Combine the images of the individual filter...",
            indent=1,
        )
        stack_image(
            output_path / 'shifted_and_trimmed',
            output_path,
            image_type_dir['light'],
            stacking_method=stack_method,
            dtype=dtype_image_stacking,
            debug=debug,
        )

        if find_wcs and not find_wcs_of_all_images:
            ###
            #   Determine WCS and add it to the stacked images
            #
            terminal_output.print_to_terminal("Determine WCS ...", indent=1)

            utilities.determine_wcs_all_images(
                output_path,
                output_path,
                force_wcs_determination=force_wcs_determination,
                wcs_method=wcs_method,
                only_combined_images=True,
                image_type=image_type_dir['light'],
            )

        if not shift_all:
            if shift_method == 'aa_true':
                ###
                #   Trim stacked images using astroalign
                #
                shift_stack_astroalign(
                    output_path,
                    output_path,
                    image_type_dir['light'],
                )

            elif shift_method in ['own', 'skimage', 'aa']:
                ###
                #   Make large images with the same dimensions to allow
                #   cross correlation
                #
                make_big_images(
                    output_path,
                    output_path,
                    image_type_dir['light'],
                )

                ###
                #   Calculate and apply image shifts between filters
                #
                terminal_output.print_to_terminal(
                    "Trim stacked images of the filters to the same "
                    "field of view...",
                    indent=1,
                )

                trim_image(
                    output_path,
                    output_path,
                    image_type_dir['light'],
                    shift_method=shift_method,
                    n_cores_multiprocessing=n_cores_multiprocessing,
                    rm_outliers=rm_outliers_image_shifts,
                    filter_window=filter_window_image_shifts,
                    threshold=threshold_image_shifts,
                    verbose=debug,
                )

            else:
                raise RuntimeError(
                    f"{style.Bcolors.FAIL}Method for determining image "
                    f"shifts {shift_method} not known {style.Bcolors.ENDC}"
                )

    else:
        #   Sort files according to filter into subdirectories
        light_image_type = utilities.get_image_type(
            image_file_collection,
            image_type_dir,
            image_class='light',
        )
        ifc_filtered = image_file_collection.filter(imagetyp=light_image_type)
        filters = set(
            ifc_filtered.summary['filter'][
                np.invert(ifc_filtered.summary['filter'].mask)
            ]
        )
        for filter_ in filters:
            #   Remove old files in the output directory
            checks.clear_directory(output_path / filter_)

            #   Set path to files
            file_path = checks.check_pathlib_path(output_path / 'shifted_and_trimmed')

            #   New image collection for the images
            image_file_collection = ccdp.ImageFileCollection(file_path)

            #   Restrict to current filter
            filtered_files = image_file_collection.files_filtered(
                filter=filter_,
                include_path=True,
            )

            #   Link files to corresponding directory
            aux_general.link_files(output_path / filter_, filtered_files)


def master_bias(
        bias_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]]) -> None:
    """
    This function calculates master biases from individual bias images
    located in one directory.

    Parameters
    ----------
    bias_path            : `string` or `pathlib.Path`
        Path to the images

    output_dir           : `string` or `pathlib.Path`
        Path to the directory where the master files should be saved to

    image_type           : `dictionary`
        Image types of the images. Possibilities: bias, dark, flat,
        light
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(bias_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Create image collection
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Return if image collection is empty
    if not image_file_collection.files:
        return

    #   Get bias frames
    bias_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='bias',
    )
    bias_frames = image_file_collection.files_filtered(
        imagetyp=bias_image_type,
        include_path=True,
    )

    #   Combine biases: Average images + sigma clipping to remove outliers,
    #                   set memory limit to 15GB, set unit to 'adu' since
    #                   this is not set in our images -> find better
    #                   solution
    combined_bias = ccdp.combine(
        bias_frames,
        method='average',
        sigma_clip=True,
        sigma_clip_low_thresh=5,
        sigma_clip_high_thresh=5,
        sigma_clip_func=np.ma.median,
        signma_clip_dev_func=mad_std,
        mem_limit=15e9,
        unit='adu',
    )

    #   Add Header keyword to mark the file as a Master
    combined_bias.meta['combined'] = True

    #   Write file to disk
    combined_bias.write(out_path / 'combined_bias.fit', overwrite=True)


def master_image_list(*args, **kwargs):
    """
        Wrapper function to create a master calibration image for the files
        in the directories given in the path list 'paths'
    """
    if kwargs['calib_type'] == 'dark':
        master_dark(*args, **kwargs)
    elif kwargs['calib_type'] == 'flat':
        master_flat(*args, **kwargs)


def reduce_dark(
        image_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]], gain: float | None = None,
        read_noise: float = 8., n_cores_multiprocessing: int | None = None
    ) -> None:
    """
    Reduce dark images: This function reduces the raw dark frames

    Parameters
    ----------
    image_path          : `string` or `pathlib.Path`
        Path to the images

    output_dir          : `string` or `pathlib.Path`
        Path to the directory where the master files should be saved to

    image_type          : `dictionary`
        Image types of the images. Possibilities: bias, dark, flat,
        light

    gain                : `float` or `None`, optional
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise          : `float`, optional
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Create image collection for the raw data
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Create image collection for the reduced data
    image_file_collection_reduced = ccdp.ImageFileCollection(out_path)

    #   Get master bias
    bias_image_type = utilities.get_image_type(
        image_file_collection_reduced,
        image_type,
        image_class='bias',
    )
    stacked_bias = CCDData.read(
        image_file_collection_reduced.files_filtered(
            imagetyp=bias_image_type,
            combined=True,
            include_path=True,
        )[0]
    )

    #   Set new dark path
    dark_path = Path(out_path / 'dark')
    checks.clear_directory(dark_path)

    #   Initialize multiprocessing object
    executor = Executor(n_cores_multiprocessing)

    #   Loop over darks and reduce darks
    dark_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='dark',
    )
    for dark, file_name in image_file_collection.ccds(
            imagetyp=dark_image_type,
            ccd_kwargs={'unit': 'adu'},
            return_fname=True,
    ):
        executor.schedule(
            reduce_dark_image,
            args=(
                dark,
                stacked_bias,
                dark_path,
                file_name,
            ),
            kwargs={
                'gain': gain,
                'read_noise': read_noise,
            }
        )


def reduce_dark_image(
        dark: CCDData, stacked_bias: CCDData, dark_path: Path, file_name: str,
        gain: float | None = None, read_noise: float = 8.,
    ) -> None:
    """
    This function reduces the individual raw dark frame images

    Parameters
    ----------
    dark
        The CCDData object of the dark image that will be reduced

    stacked_bias
        Reduced and stacked Bias CCDData object

    dark_path
        Path where the reduced images should be saved

    file_name
        Name of the image file

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.
    """
    #   Set gain _> get it from Header if not provided
    if gain is None:
        gain = dark.header['EGAIN']

    #   Calculated uncertainty
    dark = ccdp.create_deviation(
        dark,
        gain=gain * u.electron / u.adu,
        readnoise=read_noise * u.electron,
        disregard_nan=True,
    )

    # Subtract bias
    dark = ccdp.subtract_bias(dark, stacked_bias)

    #   Save the result
    dark.write(dark_path / file_name, overwrite=True)


def master_dark(
        image_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]], gain: float | None = None,
        read_noise: float = 8., dark_rate: float | None = None,
        mk_hot_pixel_mask: bool = True, plot_plots: bool = False,
        debug: bool = False, n_cores_multiprocessing: int | None = None,
        **kwargs) -> None:
    """
    This function calculates master darks from individual dark images
    located in one directory. The dark images are group according to
    their exposure time.

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type
        Image types of the images. Possibilities: bias, dark, flat,
        light

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.

    dark_rate
        Temperature dependent dark rate in e-/pix/s:
        Default is ``None``.

    mk_hot_pixel_mask
        If True a hot pixel mask is created.
        Default is ``True``.

    plot_plots
        If True some plots showing some statistic on the dark frames are
        created.
        Default is ``False``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Sanitize dark rate
    if dark_rate is None:
        terminal_output.print_to_terminal(
            f"Dark current not specified. Assume 0.1 e-/pix/s.",
            indent=1,
            style_name='WARNING',
        )
        # dark_rate = {0: 0.1}
        dark_rate = 0.1

    #   Create image collection
    try:
        image_file_collection = ccdp.ImageFileCollection(out_path / 'dark')
    except FileNotFoundError:
        image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Return if image collection is empty
    if not image_file_collection.files:
        return

    #   Find darks
    dark_mask = [True if file in image_type['dark'] else False
                 for file in image_file_collection.summary['imagetyp']]

    #   Return if no darks are found in this directory
    if not dark_mask:
        return

    #   Get all available shapes with exposure times
    all_available_image_shapes_and_exposure_times = set(tuple(zip(
        image_file_collection.summary['naxis1'][dark_mask],
        image_file_collection.summary['naxis2'][dark_mask],
        image_file_collection.summary['exptime'][dark_mask]
    )))

    #   Get only the shapes
    all_available_image_shapes = set(tuple(zip(
        image_file_collection.summary['naxis1'][dark_mask],
        image_file_collection.summary['naxis2'][dark_mask]
    )))

    #   Get the maximum exposure time for each shape
    max_exposure_time_per_shape: list = []
    for shape in all_available_image_shapes:
        exposure_times: list = []
        for shape_expo_time in all_available_image_shapes_and_exposure_times:
            if shape[0] == shape_expo_time[0] and shape[1] == shape_expo_time[1]:
                exposure_times.append(shape_expo_time[2])
        max_exposure_time_per_shape.append((*shape, np.max(exposure_times)))

    #   Get exposure times (set allows to return only unique values)
    dark_exposure_times = set(
        image_file_collection.summary['exptime'][dark_mask]
    )

    #   Get dark image type
    dark_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='dark',
    )

    #   Initialize multiprocessing object
    executor = Executor(n_cores_multiprocessing)

    #   Reduce science images and save to an extra directory
    for exposure_time in sorted(dark_exposure_times):
        executor.schedule(
            master_dark_stacking,
            args=(
                image_file_collection,
                exposure_time,
                dark_image_type,
                max_exposure_time_per_shape,
                out_path,
                dark_rate,
            ),
            kwargs={
                'gain': gain,
                'read_noise': read_noise,
                'mk_hot_pixel_mask': mk_hot_pixel_mask,
                'plot_plots': plot_plots,
            }
        )

    #   Exit if exceptions occurred
    if executor.err is not None:
        raise RuntimeError(
            f'\n{style.Bcolors.FAIL}Dark image stacking using multiprocessing'
            f' failed :({style.Bcolors.ENDC}'
        )

    #   Close multiprocessing pool and wait until it finishes
    executor.wait()

    #   Remove reduced dark files if they exist
    if not debug:
        shutil.rmtree(out_path / 'dark', ignore_errors=True)

def master_dark_stacking(
        image_file_collection: ccdp.ImageFileCollection,
        exposure_time: float, dark_image_type: str | list[str] | None,
        max_exposure_time_per_shape: list[tuple[int, int, float]],
        out_path: Path, dark_rate: float, gain: float | None = None,
        read_noise: float = 8., mk_hot_pixel_mask: bool = True,
        plot_plots: bool = False, debug: bool = False) -> None:
    """
    This function stacks all dark images with the same exposure time.

    Parameters
    ----------
    image_file_collection
        Image file collection for referencing all dark files

    exposure_time
        Exposure time of the current set of dark images

    dark_image_type
        Image type designation used for dark files

    out_path
        Path to the directory where the master files should be saved to

    max_exposure_time_per_shape
        Maximum exposure time for each available image shape

    dark_rate
        Temperature dependent dark rate in e-/pix/s:

    gain
        The gain (e-/adu) of the camera. If set to `None` the gain will
        be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera.
        Default is 8 e-.

    mk_hot_pixel_mask
        If True a hot pixel mask is created.
        Default is ``True``.

    plot_plots
        If True some plots showing some statistic on the dark frames are
        created.
        Default is ``False``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.
    """
    #   Get only the darks with the correct exposure time
    calibrated_darks = image_file_collection.files_filtered(
        imagetyp=dark_image_type,
        exptime=exposure_time,
        include_path=True,
    )

    #   Combine darks: Average images + sigma clipping to remove
    #                  outliers, set memory limit to 15GB, set unit to
    #                  'adu' since this is not set in our images
    #                  -> find better solution
    combined_dark = ccdp.combine(
        calibrated_darks,
        method='average',
        sigma_clip=True,
        sigma_clip_low_thresh=5,
        sigma_clip_high_thresh=5,
        sigma_clip_func=np.ma.median,
        sigma_clip_dev_func=mad_std,
        mem_limit=15e9,
        unit='adu',
    )

    #   Add Header keyword to mark the file as a Master
    combined_dark.meta['combined'] = True

    #   Write file to disk
    dark_file_name = f'combined_dark_{exposure_time:4.2f}.fit'
    combined_dark.write(out_path / dark_file_name, overwrite=True)

    #   Set gain _> get it from Header if not provided
    if gain is None:
        gain = combined_dark.header['EGAIN']

    #   Plot histogram
    if plot_plots:
        plots.plot_histogram(
            combined_dark.data,
            out_path,
            gain,
            exposure_time,
        )
        plots.plot_dark_with_distributions(
            combined_dark.data,
            read_noise,
            dark_rate,
            out_path,
            exposure_time=exposure_time,
            gain=gain,
        )

    #   Create mask with hot pixels
    current_shape_x = combined_dark.meta['naxis1']
    current_shape_y = combined_dark.meta['naxis2']
    if ((current_shape_x, current_shape_y, exposure_time) in
            max_exposure_time_per_shape and mk_hot_pixel_mask):
        utilities.make_hot_pixel_mask(
            combined_dark,
            gain,
            out_path,
            verbose=debug,
        )


def reduce_flat(
        image_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]], gain: float | None = None,
        read_noise: float = 8., rm_bias: bool = False,
        exposure_time_tolerance: float = 0.5,
        n_cores_multiprocessing: int | None = None, **kwargs) -> None:
    """
    Reduce flat images: This function reduces the raw flat frames,
                        subtracts master dark and if necessary also
                        master bias

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type
        Image types of the images. Possibilities: bias, dark, flat,
        light

    gain
        The gain (e-/adu) of the camera. If set to `None` the gain will
        be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera.
        Default is 8 e-.

    rm_bias
        If True the master bias image will be subtracted from the flats
        Default is ``False``.

    exposure_time_tolerance
        Maximum difference, in seconds, between the image and the
        closest entry from the exposure time list. Set to ``None`` to
        skip the tolerance test.
        Default is ``0.5``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Create image collection for the flats
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Return if image collection is empty
    if not image_file_collection.files:
        return

    #   Find flats
    flats = [
        True if file in image_type['flat'] else False for file in
        image_file_collection.summary['imagetyp']
    ]

    #   Return if no flats are found in this directory
    if not flats:
        return

    #   Get image collection for the reduced files
    image_file_collection_reduced = ccdp.ImageFileCollection(out_path)

    #   Get master dark
    dark_image_type = utilities.get_image_type(
        image_file_collection_reduced,
        image_type,
        image_class='dark',
    )
    combined_darks = {
        ccd.header['exptime']: ccd for ccd in image_file_collection_reduced.ccds(
            imagetyp=dark_image_type,
            combined=True,
        )
    }

    #   Get master bias
    combined_bias = None
    if rm_bias:
        bias_image_type = utilities.get_image_type(
            image_file_collection_reduced,
            image_type,
            image_class='bias',
        )

        combined_bias = CCDData.read(
            image_file_collection_reduced.files_filtered(
                imagetyp=bias_image_type,
                combined=True,
                include_path=True,
            )[0]
        )

    #   Set new flat path
    flat_path = Path(out_path / 'flat')
    checks.clear_directory(flat_path)

    #   Loop over flats and reduce flats
    flat_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='flat',
    )

    #   Initialize multiprocessing object
    executor = Executor(n_cores_multiprocessing)

    #   Reduce science images and save to an extra directory
    for flat, file_name in image_file_collection.ccds(
            imagetyp=flat_image_type,
            ccd_kwargs={'unit': 'adu'},
            return_fname=True,
    ):
        executor.schedule(
            reduce_flat_image,
            args=(
                flat,
                combined_bias,
                combined_darks,
                file_name,
                flat_path
            ),
            kwargs={
                'gain': gain,
                'read_noise': read_noise,
                'rm_bias': rm_bias,
                'exposure_time_tolerance': exposure_time_tolerance,
            }
        )

    #   Exit if exceptions occurred
    if executor.err is not None:
        raise RuntimeError(
            f'\n{style.Bcolors.FAIL}Flat image reduction using multiprocessing'
            f' failed :({style.Bcolors.ENDC}'
        )

    #   Close multiprocessing pool and wait until it finishes
    executor.wait()


def reduce_flat_image(
        flat: CCDData, combined_bias: CCDData | None,
        combined_darks: dict[float, CCDData],
        file_name: str, flat_path: Path,
        gain: float | None = None, read_noise: float = 8.,
        rm_bias: bool = False, exposure_time_tolerance: float = 0.5,) -> None:
    """
    Reduce an individual image

    Parameters
    ----------
    flat
        The CCDData object of the flat that should be reduced.

    combined_bias
        Reduced and stacked Bias CCDData object

    combined_darks
        Combined darks in a dictionary with exposure times as keys and
        CCDData object as values.

    file_name
        Name of the image file

    flat_path
        Path where the reduced flats should be saved

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.

    rm_bias
        If True the master bias image will be subtracted from the flats
        Default is ``False``.

    exposure_time_tolerance
        Tolerance between science and dark exposure times in s.
        Default is ``0.5``s.
    """
    #   Set gain _> get it from Header if not provided
    if gain is None:
        gain = flat.header['EGAIN']

    #   Calculated uncertainty
    flat = ccdp.create_deviation(
        flat,
        gain=gain * u.electron / u.adu,
        readnoise=read_noise * u.electron,
        disregard_nan=True,
    )

    # Subtract bias
    if rm_bias:
        flat = ccdp.subtract_bias(flat, combined_bias)

    #   Find the correct dark exposure
    valid_dark_available, closest_dark_exposure_time = utilities.find_nearest_exposure_time_to_reference_image(
        flat,
        list(combined_darks.keys()),
        time_tolerance=exposure_time_tolerance,
    )

    #   Exit if no dark with a similar exposure time have been found
    if not valid_dark_available and not rm_bias:
        raise RuntimeError(
            f"{style.Bcolors.FAIL}Closest dark exposure time is "
            f"{closest_dark_exposure_time} for flat of exposure time "
            f"{flat.header['exptime']}. {style.Bcolors.ENDC}"
        )

    #   Subtract the dark current
    flat = ccdp.subtract_dark(
        flat,
        combined_darks[closest_dark_exposure_time],
        exposure_time='exptime',
        exposure_unit=u.second,
        scale=rm_bias,
    )

    #   Save the result
    flat.write(flat_path / file_name, overwrite=True)


def master_flat(
        image_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]], mk_bad_pixel_mask: bool = True,
        plot_plots: bool = False, debug: bool = False,
        n_cores_multiprocessing: int | None = None, **kwargs) -> None:
    """
    This function calculates master flats from individual flat field
    images located in one directory. The flat field images are group
    according to their exposure time.

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type
        Image types of the images. Possibilities: bias, dark, flat,
        light

    mk_bad_pixel_mask
        If True a bad pixel mask is created.
        Default is ``True``.

    plot_plots
        If True some plots showing some statistic on the flat fields are
        created.
        Default is ``False``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Create new image collection for the reduced flat images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Determine filter
    flat_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='flat',
    )
    filters = set(
        h['filter'] for h in image_file_collection.headers(imagetyp=flat_image_type)
    )

    #   Initialize multiprocessing object
    executor = Executor(n_cores_multiprocessing)

    #   Reduce science images and save to an extra directory
    for filter_ in filters:
        executor.schedule(
            stack_flat_images,
            args=(
                image_file_collection,
                flat_image_type,
                filter_,
                out_path,
            ),
            kwargs={
                'plot_plots': plot_plots,
            }
        )

    #   Exit if exceptions occurred
    if executor.err is not None:
        raise RuntimeError(
            f'\n{style.Bcolors.FAIL}Stacking of flat images using multiprocessing'
            f' failed :({style.Bcolors.ENDC}'
        )

    #   Close multiprocessing pool and wait until it finishes
    executor.wait()

    #   Collect multiprocessing results
    #
    #   Get bad pixel masks
    bad_pixel_mask_list: list[np.ndarray] = executor.res

    if mk_bad_pixel_mask:
        utilities.make_bad_pixel_mask(
            bad_pixel_mask_list,
            out_path,
            verbose=debug,
        )

    #   Remove reduced dark files if they exist
    if not debug:
        shutil.rmtree(file_path, ignore_errors=True)


def stack_flat_images(
    image_file_collection: ccdp.ImageFileCollection,
    flat_image_type: str | list[str] | None, filter_: str, out_path: Path,
    plot_plots: bool = False) -> np.ndarray:
    """
    Stack flats for the individual filters

    Parameters
    ----------
    image_file_collection
        Image file collection for referencing all dark files

    flat_image_type
        Image type designation used for dark files

    filter_
        Current filter

    out_path
        Path to the directory where the master files should be saved to

    plot_plots
        If True some plots showing some statistic on the flat fields are
        created.
        Default is ``False``.

    Returns
    -------
    bad_pixel_mask_list
    """
    #   Select flats to combine
    flats_to_combine = image_file_collection.files_filtered(
        imagetyp=flat_image_type,
        filter=filter_,
        include_path=True,
    )

    #   Combine darks: Average images + sigma clipping to remove
    #                  outliers, set memory limit to 15GB, scale the
    #                  frames so that they have the same median value
    #                  ('inv_median')
    combined_flat = ccdp.combine(
        flats_to_combine,
        method='average',
        scale=utilities.inverse_median,
        sigma_clip=True,
        sigma_clip_low_thresh=5,
        sigma_clip_high_thresh=5,
        sigma_clip_func=np.ma.median,
        signma_clip_dev_func=mad_std,
        mem_limit=15e9,
    )

    #   Add Header keyword to mark the file as a Master
    combined_flat.meta['combined'] = True

    #   Define name and write file to disk
    flat_file_name = 'combined_flat_filter_{}.fit'.format(
        filter_.replace("''", "p")
    )
    combined_flat.write(out_path / flat_file_name, overwrite=True)

    #   Plot flat medians and means
    if plot_plots:
        plots.plot_median_of_flat_fields(
            image_file_collection,
            flat_image_type,
            out_path,
            filter_,
        )

    return ccdp.ccdmask(combined_flat.data)


def reduce_master(paths, *args, **kwargs):
    """
    Wrapper function for reduction of the science images

    Parameters
    ----------
    paths           : `list of strings`
        List with paths to the images
    """
    if isinstance(paths, list):
        for path in paths:
            reduce_light(path, *args, **kwargs)
    elif isinstance(paths, str) or isinstance(paths, Path):
        reduce_light(paths, *args, **kwargs)
    else:
        raise RuntimeError(
            f'{style.Bcolors.FAIL}Supplied path is neither str nor list'
            f'{style.Bcolors.ENDC}'
        )


def reduce_light(
        image_path: str | Path, output_dir: str | Path,
        image_type: dict[str, list[str]], rm_cosmic_rays: bool = True,
        mask_cosmics: bool = False, gain: float | None = None,
        read_noise: float = 8., saturation_level: float = 65535.,
        limiting_contrast_rm_cosmic_rays: float = 5.,
        sigma_clipping_value_rm_cosmic_rays: float = 4.5,
        scale_image_with_exposure_time: bool = True, rm_bias: bool = False,
        verbose: bool = False, add_hot_bad_pixel_mask: bool = True,
        exposure_time_tolerance: float = 0.5,
        target_name: str | None = None,
        n_cores_multiprocessing: int | None = None) -> None:
    """
    Reduce the science images

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be stored

    image_type
        Image types of the images. Possibilities: bias, dark, flat,
        light

    rm_cosmic_rays
        If True cosmic rays will be removed.
        Default is ``True``.

    mask_cosmics
        If True cosmics will ''only'' be masked. If False the
        cosmics will be removed from the input image and the mask will
        be added.
        Default is ``False``.

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.

    saturation_level
        Saturation limit of the camera chip.
        Default is ``65535``.

    limiting_contrast_rm_cosmic_rays
        Parameter for the cosmic ray removal: Minimum contrast between
        Laplacian image and the fine structure image.
        Default is ``5``.

    sigma_clipping_value_rm_cosmic_rays
        Parameter for the cosmic ray removal: Fractional detection limit
        for neighboring pixels.
        Default is ``4.5``.

    scale_image_with_exposure_time
        If True the image will be scaled with the exposure time.
        Default is ``True``.

    rm_bias
        If True the master bias image will be subtracted from the flats
        Default is ``False``.

    verbose
        If True additional output will be printed to the command line.
        Default is ``False``.

    add_hot_bad_pixel_mask
        If True add hot and bad pixel mask to the reduced science
        images.
        Default is ``True``.

    exposure_time_tolerance
        Tolerance between science and dark exposure times in s.
        Default is ``0.5``s.

    target_name
        Name of the target. Used for file selection.
        Default is ``None``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   Get image collection for the science images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Return if image collection is empty
    if not image_file_collection.files:
        raise RuntimeError(
            f"{style.Bcolors.FAIL} \tNo object image detected.\n\t"
            f"-> EXIT{style.Bcolors.ENDC}"
        )
        # return

    #   Limit images to those of the target. If a target is given.
    if target_name is not None:
        image_file_collection = image_file_collection.filter(
            object=target_name
        )

    if not image_file_collection.files:
        raise RuntimeError(
            f"{style.Bcolors.FAIL} \tERROR: No image left after filtering by "
            f"object name.\n\t-> EXIT{style.Bcolors.ENDC}"
        )

    #   Find science images
    lights = [True if file in image_type['light'] else False for file in
              image_file_collection.summary['imagetyp']]

    #   Return if no science images are found in this directory
    if not lights:
        return

    #   Get image collection for the reduced files
    image_file_collection_reduced = ccdp.ImageFileCollection(out_path)

    #   Load combined darks and flats in dictionary for easy access
    dark_image_type = utilities.get_image_type(
        image_file_collection_reduced,
        image_type,
        image_class='dark',
    )
    combined_darks: dict[float, CCDData] = {
        ccd.header['exptime']: ccd for ccd in image_file_collection_reduced.ccds(
            imagetyp=dark_image_type,
            combined=True,
        )
    }
    flat_image_type = utilities.get_image_type(
        image_file_collection_reduced,
        image_type,
        image_class='flat',
    )
    combined_flats: dict[str, CCDData] = {
        ccd.header['filter']: ccd for ccd in image_file_collection_reduced.ccds(
            imagetyp=flat_image_type,
            combined=True,
        )
    }

    #   Get master bias
    combined_bias: CCDData | None = None
    if rm_bias:
        bias_image_type = utilities.get_image_type(
            image_file_collection_reduced,
            image_type,
            image_class='bias',
        )

        combined_bias = CCDData.read(
            image_file_collection_reduced.files_filtered(
                imagetyp=bias_image_type,
                combined=True,
                include_path=True,
            )[0]
        )

    #   Set science image path
    light_path = Path(out_path / 'light')

    dir_empty = checks.check_if_directory_is_empty(light_path)

    if not dir_empty:
        user_input, timed_out = timedInput(
            f"{style.Bcolors.OKBLUE}   Reduced images from a previous run "
            f"found. Should these be used? [yes/no] {style.Bcolors.ENDC}",
            timeout=30,
        )
        if timed_out:
            user_input = 'n'

        if user_input in ['y', 'yes']:
            return

    checks.clear_directory(light_path)

    #   Get possible image types
    light_image_type = utilities.get_image_type(
        image_file_collection,
        image_type,
        image_class='light',
    )

    #   Initialize multiprocessing object
    executor = Executor(n_cores_multiprocessing)

    #   Reduce science images and save to an extra directory
    for light, file_name in image_file_collection.ccds(
            imagetyp=light_image_type,
            return_fname=True,
            ccd_kwargs=dict(unit='adu'),
        ):
        executor.schedule(
            reduce_light_image,
            args=(
                light,
                combined_bias,
                combined_darks,
                combined_flats,
                file_name,
                out_path,
                light_path
            ),
            kwargs={
                'gain': gain,
                'read_noise': read_noise,
                'rm_bias': rm_bias,
                'exposure_time_tolerance': exposure_time_tolerance,
                'add_hot_bad_pixel_mask': add_hot_bad_pixel_mask,
                'rm_cosmic_rays': rm_cosmic_rays,
                'limiting_contrast_rm_cosmic_rays': limiting_contrast_rm_cosmic_rays,
                'sigma_clipping_value_rm_cosmic_rays': sigma_clipping_value_rm_cosmic_rays,
                'saturation_level': saturation_level,
                'mask_cosmics': mask_cosmics,
                'scale_image_with_exposure_time': scale_image_with_exposure_time,
                'verbose': verbose,
            }
        )

    #   Exit if exceptions occurred
    if executor.err is not None:
        raise RuntimeError(
            f'\n{style.Bcolors.FAIL}Light image reduction using multiprocessing'
            f' failed :({style.Bcolors.ENDC}'
        )

    #   Close multiprocessing pool and wait until it finishes
    executor.wait()


def reduce_light_image(
        light: CCDData, combined_bias: CCDData | None,
        combined_darks: dict[float, CCDData],
        combined_flats: dict[str, CCDData], file_name: str,
        out_path: Path, light_path: Path,
        gain: float | None = None, read_noise: float = 8.,
        rm_bias: bool = False, exposure_time_tolerance: float = 0.5,
        add_hot_bad_pixel_mask: bool = True, rm_cosmic_rays: bool = True,
        limiting_contrast_rm_cosmic_rays: float = 5.,
        sigma_clipping_value_rm_cosmic_rays: float = 4.5,
        saturation_level: float = 65535., mask_cosmics: bool = False,
        scale_image_with_exposure_time: bool = True, verbose: bool = False
    ) -> None:
    """
    Reduce an individual image

    Parameters
    ----------
    light
        The CCDData object that should be reduced.

    combined_bias
        Reduced and stacked Bias CCDData object

    combined_darks
        Combined darks in a dictionary with exposure times as keys and
        CCDData object as values.

    combined_flats
        Combined flats in a dictionary with exposure times as keys and
        CCDData object as values.

    file_name
        Name of the image file

    out_path
        Path to the general output directory

    light_path
        Path where the reduced images should be saved

    gain
        The gain (e-/adu) of the camera chip. If set to `None` the gain
        will be extracted from the FITS header.
        Default is ``None``.

    read_noise
        The read noise (e-) of the camera chip.
        Default is ``8`` e-.

    rm_bias
        If True the master bias image will be subtracted from the flats
        Default is ``False``.

    exposure_time_tolerance
        Tolerance between science and dark exposure times in s.
        Default is ``0.5``s.

    add_hot_bad_pixel_mask
        If True add hot and bad pixel mask to the reduced science
        images.
        Default is ``True``.

    rm_cosmic_rays
        If True cosmic rays will be removed.
        Default is ``True``.

    limiting_contrast_rm_cosmic_rays
        Parameter for the cosmic ray removal: Minimum contrast between
        Laplacian image and the fine structure image.
        Default is ``5``.

    sigma_clipping_value_rm_cosmic_rays
        Parameter for the cosmic ray removal: Fractional detection limit
        for neighboring pixels.
        Default is ``4.5``.

    saturation_level
        Saturation limit of the camera chip.
        Default is ``65535``.

    mask_cosmics
        If True cosmics will ''only'' be masked. If False the
        cosmics will be removed from the input image and the mask will
        be added.
        Default is ``False``.

    scale_image_with_exposure_time
        If True the image will be scaled with the exposure time.
        Default is ``True``.

    verbose
        If True additional output will be printed to the command line.
        Default is ``False``.
    """
#   Set gain -> get it from Header if not provided
    if gain is None:
        try:
            gain = light.header['EGAIN']
        except KeyError:
            gain = 1.
            terminal_output.print_to_terminal(
                "WARNING: Gain could not de derived from the "
                "image header. Use 1.0 instead",
                style_name='WARNING',
                indent=2,
            )

    #   Calculated uncertainty
    light = ccdp.create_deviation(
        light,
        gain=gain * u.electron / u.adu,
        readnoise=read_noise * u.electron,
        disregard_nan=True,
    )

    #   Subtract bias
    if rm_bias:
        light = ccdp.subtract_bias(light, combined_bias)

    #   Find the correct dark exposure
    valid_dark_available, closest_dark_exposure_time = utilities.find_nearest_exposure_time_to_reference_image(
        light,
        list(combined_darks.keys()),
        time_tolerance=exposure_time_tolerance,
    )

    #   Exit if no dark with a similar exposure time have been found
    if not valid_dark_available and not rm_bias:
        raise RuntimeError(
            f"{style.Bcolors.FAIL}Closest dark exposure time is "
            f"{closest_dark_exposure_time} for science image of exposure "
            f"time {light.header['exptime']}. {style.Bcolors.ENDC}"
        )

    #   Subtract dark
    reduced = ccdp.subtract_dark(
        light,
        combined_darks[closest_dark_exposure_time],
        exposure_time='exptime',
        exposure_unit=u.second,
        scale=rm_bias,
    )

    #   Mask negative pixel
    mask = reduced.data < 0.
    reduced.mask = reduced.mask | mask

    #   Check if the "FILTER" keyword is set in Header
    #   TODO: Added ability to skip if filter not found. Add warning about which file will be skipped.
    #   TODO: Check if this works...
    if 'filter' not in reduced.header:
        terminal_output.print_to_terminal(
            f"WARNING: FILTER keyword not found in HEADER. \n Skip file: {file_name}.",
            style_name='WARNING',
            indent=2,
        )
        return

    #   Get master flat field
    flat_master = combined_flats[reduced.header['filter']]

    #   Divided science by the master flat
    reduced = ccdp.flat_correct(reduced, flat_master)

    if add_hot_bad_pixel_mask:
        #   Get mask of bad and hot pixel
        mask_available, bad_hot_pixel_mask = utilities.get_pixel_mask(
            out_path,
            reduced.shape,
        )

        #   Add bad pixel mask: If there was already a mask, keep it
        if mask_available:
            if reduced.mask is not None:
                reduced.mask = reduced.mask | bad_hot_pixel_mask
            else:
                reduced.mask = bad_hot_pixel_mask

    #   Gain correct data
    reduced = ccdp.gain_correct(reduced, gain * u.electron / u.adu)

    #   Remove cosmic rays
    if rm_cosmic_rays:
        if verbose:
            print(f'Remove cosmic rays from image {file_name}')
        reduced_without_cosmics = ccdp.cosmicray_lacosmic(
            reduced,
            objlim=limiting_contrast_rm_cosmic_rays,
            readnoise=read_noise,
            sigclip=sigma_clipping_value_rm_cosmic_rays,
            satlevel=saturation_level,
            verbose=verbose,
        )

        if mask_cosmics:
            if add_hot_bad_pixel_mask:
                reduced.mask = reduced.mask | reduced_without_cosmics.mask

                #   Add a header keyword to indicate that the cosmics have been
                #   masked
                reduced.meta['cosmic_mas'] = True
        else:
            reduced = reduced_without_cosmics
            if not add_hot_bad_pixel_mask:
                reduced.mask = np.zeros(reduced.shape, dtype=bool)

            #   Add header keyword to indicate that cosmics have been removed
            reduced.meta['cosmics_rm'] = True

        if verbose:
            terminal_output.print_to_terminal('')

    #   Scale image with exposure time
    if scale_image_with_exposure_time:
        #   Get exposure time and all meta data
        exposure_time = reduced.header['exptime']
        reduced_meta = reduced.meta

        #   Scale image
        reduced = reduced.divide(exposure_time * u.second)

        #   Put metadata back on the image, because it is lost while
        #   dividing
        reduced.meta = reduced_meta
        reduced.meta['HIERARCH'] = 'Image scaled by exposure time:'
        reduced.meta['HIERARCH'] = 'Unit: e-/s/pixel'

        #   Set data units to electron / s
        reduced.unit = u.electron / u.s

    #   Write reduced science image to disk
    reduced.write(light_path / file_name, overwrite=True)


def shift_img_apply(
        current_image_ccd: CCDData, reference_image_ccd: CCDData,
        n_images: int, image_shifts: np.ndarray, image_flips: np.ndarray,
        image_id: int, output_path: Path, image_name: str,
        shift_method: str = 'skimage', modify_file_name: bool = False,
        rm_enlarged_keyword: bool = False, instrument: bool = None,
        verbose: bool = False) -> None:
    """
    Apply shift to an individual image

    Parameters
    ----------
    current_image_ccd
        Image data

    reference_image_ccd
        Data of the reference image

    n_images
        Number of images

    image_shifts
        Shifts of the images in X and Y direction

    image_flips
        Flip necessary to account for pier flips

    image_id
        ID of the image

    output_path
        Path to the output directory

    image_name
        Name of the image

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation implemented by
                                   skimage
                       'flow'    = image registration using optical flow
                                   implementation by skimage
        Default is ``skimage``.

    modify_file_name
        It true the trimmed image will be saved, using a modified file
        name.
        Default is ``False``.

    rm_enlarged_keyword
        It true the header keyword 'enlarged' will be removed.
        Default is ``False``.

    instrument
        The instrument used
        Default is ``None``.

    verbose
        If True additional output will be printed to the console
        Default is ``False``.
    """
    #   Trim images
    if shift_method in ['own', 'skimage', 'aa']:
        #   Flip image if pier side changed
        if image_flips[image_id]:
            current_image_ccd = ccdp.transform_image(
                current_image_ccd,
                np.flip,
                axis=(0, 1),
            )

        output_image = utilities.trim_image(
            current_image_ccd,
            image_id,
            n_images,
            image_shifts,
            correlation_method=shift_method,
            verbose=verbose,
        )
    elif shift_method == 'flow':
        output_image = utilities.image_shift_optical_flow_method(
            reference_image_ccd,
            current_image_ccd,
        )

    #   Using astroalign to align the images
    elif shift_method == 'aa_true':
        output_image = utilities.image_shift_astroalign_method(
            reference_image_ccd,
            current_image_ccd,
        )

    else:
        raise RuntimeError(
            f"{style.Bcolors.FAIL} \nThe provided method to determine the "
            f"shifts is not known. Got {shift_method}. Allowed: own, "
            f"skimage, aa, flow, aa_true {style.Bcolors.ENDC}"
        )

    #   Reset the device as it may have been updated
    if instrument is not None and instrument != '':
        output_image.meta['INSTRUME'] = instrument

    #   Add Header keyword to mark the file as trimmed
    output_image.meta['trimmed'] = True
    if rm_enlarged_keyword:
        output_image.meta.remove('enlarged')

    if modify_file_name:
        #   Get filter
        filter_ = output_image.meta['filter']

        #   Define name and write trimmed image to disk
        image_name = 'combined_trimmed_filter_{}.fit'.format(
            filter_.replace("''", "p")
        )

    #   Write trimmed image to disk
    output_image.write(output_path / image_name, overwrite=True)


def detect_outlier(
        data: np.ndarray, filter_window: int = 8, threshold: float | int = 10.
        ) -> np.ndarray:
    """
    Find outliers in a data array

    Parameters
    ----------
    data
        The data

    filter_window
        Width of the median filter window
        Default is ``8``.

    threshold
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    Returns
    -------

        Index of the elements along axis 0 that are below the threshold
    """
    #   Calculate running median
    run_median = median_filter(data, size=(1, filter_window))

    #   Difference compared to median and sum along axis 0
    score = np.sum(np.abs(data - run_median), axis=0)

    #   Return outliers
    return np.argwhere(score > threshold)


def shift_image_core(
        image_file_collection: ccdp.ImageFileCollection, output_path: Path,
        shift_method: str = 'skimage',
        n_cores_multiprocessing: int | None = None,
        reference_image_id: int = 0,
        shift_terminal_comment: str = '\tImage displacement:',
        rm_enlarged_keyword: bool = False, modify_file_name: bool = False,
        rm_outliers: bool = True, filter_window: int = 25,
        threshold: int | float = 10., instrument: str | None = None,
        verbose: bool = False) -> None:
    """
    Core steps of the image shift calculations and trimming to a
    common filed of view

    Parameters
    ----------
    image_file_collection
        Image file collection with all images

    output_path
        Path to the output directory

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation implemented by
                                   skimage
                       'flow'    = image registration using optical flow
                                   implementation by skimage
        Default is ``skimage``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.

    reference_image_id
        ID of the image that should be used as a reference
        Default is ``0``.

    shift_terminal_comment
        Text string that is used to label the output.
        Default is ``Image displacement:``.

    rm_enlarged_keyword
        It True the header keyword 'enlarged' will be removed.
        Default is ``False``.

    modify_file_name
        It True the trimmed image will be saved, using a modified file
        name.
        Default is ``False``.

    rm_outliers
        If True outliers in the image shifts will be detected and removed.
        Default is ``True``.

    filter_window
        Width of the median filter window
        Default is ``25``.

    threshold
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    instrument
        The instrument used
        Default is ``None``.

    verbose
        If True additional output will be printed to the console
        Default is ``False``.
    """
    #   Calculate image shifts
    if shift_method in ['own', 'skimage', 'aa']:
        image_shifts, image_flips = utilities.calculate_image_shifts(
            image_file_collection,
            reference_image_id,
            shift_terminal_comment,
            correlation_method=shift_method,
            n_cores_multiprocessing=n_cores_multiprocessing,
        )
        reference_image_ccd = None
    elif shift_method in ['aa_true', 'flow']:
        reference_file_name = image_file_collection.files[reference_image_id]
        reference_image_ccd = CCDData.read(reference_file_name)
        image_shifts = None
        image_flips = None
    else:
        raise RuntimeError(
            f'{style.Bcolors.FAIL}Method {shift_method} not known '
            f'-> EXIT {style.Bcolors.ENDC}'
        )

    #   Number of images
    n_images = len(image_file_collection.files)

    #   Find IDs of potential outlier
    if rm_outliers and image_shifts is not None:
        outlier_ids = detect_outlier(
            image_shifts,
            filter_window=filter_window,
            threshold=threshold,
        )
        if outlier_ids.size:
            terminal_output.print_to_terminal(
                "The images with the following IDs will be removed "
                f"because of not reliable shifts:\n {outlier_ids.ravel()}.",
                indent=2,
                style_name='WARNING',
            )

            #   Remove outliers from determined shift
            # image_shifts = np.delete(image_shifts, outlier_ids, axis=1)
            #   Set outlier image shifts to 0
            image_shifts[:, outlier_ids] = 0.
    else:
        outlier_ids = []

    #   Trim all images
    for current_image_id, (current_image_ccd, file_name) in enumerate(image_file_collection.ccds(return_fname=True)):
        if current_image_id not in outlier_ids:
            try:
                shift_img_apply(
                    current_image_ccd,
                    reference_image_ccd,
                    n_images,
                    image_shifts,
                    image_flips,
                    current_image_id,
                    output_path,
                    file_name,
                    shift_method=shift_method,
                    modify_file_name=modify_file_name,
                    rm_enlarged_keyword=rm_enlarged_keyword,
                    instrument=instrument,
                    verbose=verbose,
                )
            except (RuntimeError, ValueError, TypeError) as e:
                terminal_output.print_to_terminal(
                    f"WARNING: Failed to calculate image offset for image"
                    f" {file_name} with ERROR code: \n\n {e} \n Skip file.",
                    style_name='WARNING',
                    indent=2,
                )


def shift_image(
        path: str | Path, output_dir: str | Path, image_type_list: list[str],
        reference_image_id: int = 0, shift_method: str = 'skimage',
        n_cores_multiprocessing: int | None = None,
        rm_outliers: bool = True, filter_window: int = 25,
        threshold: int | float = 10., instrument: str | None = None,
        debug: bool = False) -> None:
    """
    Calculate shift between images taken in the same filter
    and trim those to the save field of view

    Parameters
    ----------
    path
        The path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type_list
        Header keyword characterizing the image type for which the
        shifts shall be determined

    reference_image_id
        ID of the image that should be used as a reference
        Default is ``0``.

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation with skimage
        Default is ``skimage``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.

    rm_outliers
        If True outliers in the image shifts will be detected and removed.
        Default is ``True``.

    filter_window
        Width of the median filter window
        Default is ``25``.

    threshold
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    instrument
        The instrument used
        Default is ``None``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(path)
    out_path = checks.check_pathlib_path(output_dir)

    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Check if image_file_collection is not empty
    if not image_file_collection.files:
        raise RuntimeError(
            f"{style.Bcolors.FAIL}No FITS files found in {file_path}. "
            f"=> EXIT {style.Bcolors.ENDC}"
        )

    #   Determine filter
    image_type = utilities.get_image_type(
        image_file_collection,
        image_type_list,
    )
    filters = set(
        h['filter'] for h in image_file_collection.headers(imagetyp=image_type)
    )

    #   Set science image path
    trim_path = Path(out_path / 'shifted_and_trimmed')
    checks.clear_directory(trim_path)

    #   Calculate shifts for the images in the individual filters
    for filter_ in filters:
        #   Restrict image collection to those images with the correct
        #   filter
        ifc_filter = image_file_collection.filter(filter=filter_)

        #   Calculate image shifts and trim images accordingly
        shift_image_core(
            ifc_filter,
            trim_path,
            shift_method=shift_method,
            n_cores_multiprocessing=n_cores_multiprocessing,
            reference_image_id=reference_image_id,
            shift_terminal_comment=f'\tDisplacement for images in filter: {filter_}',
            rm_outliers=rm_outliers,
            filter_window=filter_window,
            instrument=instrument,
            threshold=threshold,
            verbose=debug,
        )

    #   Remove reduced dark files if they exist
    if not debug:
        shutil.rmtree(file_path, ignore_errors=True)


def shift_all_images(
        image_path: str | Path, output_dir: str | Path,
        image_type_list: list[str], reference_image_id: int = 0,
        shift_method: str = 'skimage',
        n_cores_multiprocessing: int | None = None,
        rm_outliers: bool = True, filter_window: int = 25,
        threshold: int | float = 10., instrument: str | None = None,
        debug: bool = False) -> None:
    """
    Calculate shift between images and trim those to the save field of
    view

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type_list
        Header keywords characterizing the image type for which the
        shifts shall be determined

    reference_image_id
        ID of the image that should be used as a reference
        Default is ``0``.

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation with skimage
        Default is ``skimage``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.

    rm_outliers
        If True outliers in the image shifts will be detected and removed.
        Default is ``True``.

    filter_window
        Width of the median filter window
        Default is ``25``.

    threshold
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    instrument
        The instrument used
        Default is ``None``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Check if image_file_collection is not empty
    if not image_file_collection.files:
        raise RuntimeError(
            f"{style.Bcolors.FAIL}No FITS files found in {file_path}. "
            f"=> EXIT {style.Bcolors.ENDC}"
        )

    #   Apply image_file_collection filter to the image collection
    #   -> This is necessary so that the path to the image directory is
    #      added to the file names. This is required for
    #      `shift_img_core`.
    image_type = utilities.get_image_type(
        image_file_collection,
        image_type_list,
    )
    ifc_filtered = image_file_collection.filter(imagetyp=image_type)

    #   Set output path
    trim_path = Path(out_path / 'shifted_and_trimmed')
    checks.clear_directory(trim_path)

    #   Calculate image shifts and trim images accordingly
    shift_image_core(
        ifc_filtered,
        trim_path,
        shift_method=shift_method,
        n_cores_multiprocessing=n_cores_multiprocessing,
        reference_image_id=reference_image_id,
        rm_outliers=rm_outliers,
        filter_window=filter_window,
        instrument=instrument,
        threshold=threshold,
        verbose=debug,
    )

    #   Remove reduced files if they exist
    if not debug:
        shutil.rmtree(file_path, ignore_errors=True)


def shift_stack_astroalign(
        path: str | Path, output_dir: Path, image_type: list[str]) -> None:
    """
    Calculate shift between stacked images and trim those
    to the save field of view

    Parameters
    ----------
    path
        The path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type
        Header keyword characterizing the image type for which the
        shifts shall be determined
    """
    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(path)
    img_type = utilities.get_image_type(image_file_collection, image_type)
    ifc_filtered = image_file_collection.filter(
        combined=True,
        imagetyp=img_type,
    )

    for current_image_id, (current_image_ccd, file_name) in enumerate(ifc_filtered.ccds(return_fname=True)):
        reference_image_ccd: ccdp.CCDData | None = None
        if current_image_id == 0:
            reference_image_ccd = current_image_ccd
            image_out = reference_image_ccd
        else:
            #   Byte order of the system
            sbo = sys.byteorder

            #   Map with endianness symbols
            endian_map = {
                '>': 'big',
                '<': 'little',
                '=': sbo,
                '|': 'not applicable',
            }
            if endian_map[current_image_ccd.data.dtype.byteorder] != sbo:
                current_image_ccd.data = current_image_ccd.data.byteswap().newbyteorder()
                reference_image_ccd.data = reference_image_ccd.data.byteswap().newbyteorder()
                current_image_ccd.uncertainty = StdDevUncertainty(
                    current_image_ccd.uncertainty.array.byteswap().newbyteorder()
                )
                reference_image_ccd.uncertainty = StdDevUncertainty(
                    reference_image_ccd.uncertainty.array.byteswap().newbyteorder()
                )

            #   Determine transformation between the images
            transformation_parameter, (_, _) = aa.find_transform(
                current_image_ccd,
                reference_image_ccd,
                max_control_points=100,
                detection_sigma=3,
            )

            #   Transform image data
            image_data, footprint = aa.apply_transform(
                transformation_parameter,
                current_image_ccd,
                reference_image_ccd,
                propagate_mask=True,
            )

            #   Transform uncertainty array
            image_uncertainty, _ = aa.apply_transform(
                transformation_parameter,
                current_image_ccd.uncertainty.array,
                reference_image_ccd.uncertainty.array,
            )

            #   Build new CCDData object
            image_out = CCDData(
                image_data,
                mask=footprint,
                meta=current_image_ccd.meta,
                unit=current_image_ccd.unit,
                wcs=current_image_ccd.wcs,
                uncertainty=StdDevUncertainty(image_uncertainty),
            )

        #   Get filter
        filter_ = image_out.meta['filter']

        image_out.meta['trimmed'] = True
        image_out.meta.remove('combined')

        #   Define name and write trimmed image to disk
        file_name = 'combined_trimmed_filter_{}.fit'.format(
            filter_.replace("''", "p")
        )
        image_out.write(output_dir / file_name, overwrite=True)


def stack_image(
        image_path: Path, output_dir: Path, image_type_list: list[str],
        stacking_method: str = 'average', dtype: str | np.dtype | None = None,
        new_target_name: str | None = None, debug: bool = False) -> None:
    """
    Combine images

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type_list
        Header keyword characterizing the image type for which the
        shifts shall be determined

    stacking_method
        Method used for combining the images.
        Possibilities: ``median`` or ``average`` or ``sum``
        Default is ``average`.

    dtype
        The dtype that should be used while combining the images.
        Default is ''None'' -> None is equivalent to float64

    new_target_name
        Name of the target. If not None, this target name will be written
        to the FITS header.
        Default is ``None``.

    debug
        If `True` the intermediate files of the data reduction will not
        be removed.
        Default is ``False``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Check if image_file_collection is not empty
    if not image_file_collection.files:
        raise RuntimeError(
            f"{style.Bcolors.FAIL}No FITS files found in {file_path}. "
            f"=> EXIT {style.Bcolors.ENDC}"
        )

    #   Determine filter
    image_type = utilities.get_image_type(
        image_file_collection,
        image_type_list,
    )
    filters = set(h['filter'] for h in image_file_collection.headers(imagetyp=image_type))

    #   Combine images for the individual filters
    for filter_ in filters:
        #   Select images to combine
        images_to_combine = image_file_collection.files_filtered(
            imagetyp=image_type,
            filter=filter_,
            include_path=True,
        )

        #   Combine darks: Average images + sigma clipping to remove
        #                  outliers, set memory limit to 15GB
        combined_image = ccdp.combine(
            images_to_combine,
            method=stacking_method,
            sigma_clip=True,
            sigma_clip_low_thresh=5,
            sigma_clip_high_thresh=5,
            sigma_clip_func=np.ma.median,
            signma_clip_dev_func=mad_std,
            mem_limit=15e9,
            dtype=dtype,
        )

        #   Update Header keywords
        utilities.update_header_information(
            combined_image,
            len(images_to_combine),
            new_target_name,
        )

        #   Define name and write file to disk
        file_name = 'combined_filter_{}.fit'.format(
            filter_.replace("''", "p")
        )
        combined_image.write(out_path / file_name, overwrite=True)

    #   Remove individual reduced images
    if not debug:
        shutil.rmtree(file_path, ignore_errors=True)


def make_big_images(
        image_path: str | Path | None, output_dir: str | Path | None,
        image_type_list: list[str], combined_only: bool = True) -> None:
    """
    Image size unification:
        Find the largest image and use this for all other images

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type_list
        Header keyword characterizing the image type for which the
        shifts shall be determined

    combined_only
        It true the file selection will be restricted to images with a
        header keyword 'combined' that is set to True.
        Default is ``True``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Image list
    image_type = utilities.get_image_type(
        image_file_collection,
        image_type_list,
    )
    img_dict = {
        file_name: ccd for ccd, file_name in image_file_collection.ccds(
            imagetyp=image_type,
            return_fname=True,
            combined=combined_only,
        )
    }

    #   Image list
    image_list = list(img_dict.values())

    #   File name list
    file_names = list(img_dict.keys())

    #   Number of images
    n_images = len(file_names)

    #   Get image dimensions
    image_shape_array_x = np.zeros(n_images, dtype='int')
    image_shape_array_y = np.zeros(n_images, dtype='int')
    for i, current_image in enumerate(image_list):
        #   Original image dimension
        image_shape_array_x[i] = current_image.shape[1]
        image_shape_array_y[i] = current_image.shape[0]

    #   Maximum size
    image_shape_x_max = np.max(image_shape_array_x)
    image_shape_y_max = np.max(image_shape_array_y)

    for i, current_image in enumerate(image_list):
        #   Make big image ans mask
        big_image = np.zeros((image_shape_y_max, image_shape_x_max))
        big_mask = np.ones((image_shape_y_max, image_shape_x_max), dtype=bool)
        big_uncertainty = np.zeros((image_shape_y_max, image_shape_x_max))

        #   Fill image and mask
        big_image[0:image_shape_array_y[i], 0:image_shape_array_x[i]] = current_image.data
        big_mask[0:image_shape_array_y[i], 0:image_shape_array_x[i]] = current_image.mask
        big_uncertainty[0:image_shape_array_y[i], 0:image_shape_array_x[i]] = current_image.uncertainty.array

        #   Replace
        current_image.data = big_image
        current_image.mask = big_mask
        current_image.uncertainty.array = big_uncertainty

        #   Add Header keyword to mark the file as a Master
        current_image.meta['enlarged'] = True
        current_image.meta.remove('combined')

        #   Get filter
        filter_ = current_image.meta['filter']

        #   Define name and write trimmed image to disk
        file_name = 'combined_enlarged_filter_{}.fit'.format(
            filter_.replace("''", "p")
        )
        current_image.write(out_path / file_name, overwrite=True)


def trim_image(
        image_path: str | Path, output_dir: str | Path,
        image_type_list: list[str], reference_image_id: int = 0,
        enlarged_only: bool = True, shift_method: str = 'skimage',
        n_cores_multiprocessing: int | None = None,
        rm_outliers: bool = True, filter_window: int = 25,
        threshold: int | float =10., verbose: bool = False) -> None:
    """
    Trim images to the same field of view

    Parameters
    ----------
    image_path
        Path to the images

    output_dir
        Path to the directory where the master files should be saved to

    image_type_list
        Header keyword characterizing the image type for which the
        shifts shall be determined

    reference_image_id
        ID of the image that should be used as a reference
        Default is ``0``.

    enlarged_only
        It true the file selection will be restricted to images with a
        header keyword 'enlarged' that is set to True.
        Default is ``True``.

    shift_method
        Method to use for image alignment.
        Possibilities: 'aa'      = astroalign module only accounting for
                                   xy shifts
                       'aa_true' = astroalign module with corresponding
                                   transformation
                       'own'     = own correlation routine based on
                                   phase correlation, applying fft to
                                   the images
                       'skimage' = phase correlation with skimage
        Default is ``skimage``.

    n_cores_multiprocessing
        Number of cores to use during calculation of the image shifts.
        Default is ``None``.

    rm_outliers
        If True outliers in the image shifts will be detected and removed.
        Default is ``True``.

    filter_window
        Width of the median filter window
        Default is ``25``.

    threshold
        Difference above the running median above an element is
        considered to be an outlier.
        Default is ``10.``.

    verbose
        If True additional output will be printed to the command line.
        Default is ``False``.
    """
    #   Sanitize the provided paths
    file_path = checks.check_pathlib_path(image_path)
    out_path = checks.check_pathlib_path(output_dir)

    #   New image collection for the images
    image_file_collection = ccdp.ImageFileCollection(file_path)

    #   Restrict image collection to those images with the correct image
    #   type and the 'enlarged' Header keyword
    image_type = utilities.get_image_type(
        image_file_collection,
        image_type_list,
    )
    ifc_filtered = image_file_collection.filter(
        imagetyp=image_type,
        enlarged=enlarged_only,
    )

    #   Calculate image shifts and trim images accordingly
    shift_image_core(
        ifc_filtered,
        out_path,
        shift_method=shift_method,
        n_cores_multiprocessing=n_cores_multiprocessing,
        reference_image_id=reference_image_id,
        shift_terminal_comment='\tDisplacement between the images of the different filters',
        rm_enlarged_keyword=enlarged_only,
        modify_file_name=True,
        rm_outliers=rm_outliers,
        filter_window=filter_window,
        threshold=threshold,
        verbose=verbose,
    )
