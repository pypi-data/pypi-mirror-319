"""Export RT-DC measurement data"""
from __future__ import annotations

import codecs
import json
import pathlib
import time
from typing import Dict, List
import uuid
import warnings

import h5py
import hdf5plugin

try:
    import imageio
except ModuleNotFoundError:
    IMAGEIO_AVAILABLE = False
else:
    IMAGEIO_AVAILABLE = True

try:
    import fcswrite
except ModuleNotFoundError:
    FCSWRITE_AVAILABLE = False
else:
    FCSWRITE_AVAILABLE = True

import numpy as np

from .. import definitions as dfn
from .._version import version, version_tuple

from .feat_basin import get_basin_classes
from .writer import RTDCWriter


class LimitingExportSizeWarning(UserWarning):
    pass


class Export(object):
    def __init__(self, rtdc_ds):
        """Export functionalities for RT-DC datasets"""
        self.rtdc_ds = rtdc_ds

    def avi(self, path, filtered=True, override=False):
        """Exports filtered event images to an avi file

        Parameters
        ----------
        path: str
            Path to a .avi file. The ending .avi is added automatically.
        filtered: bool
            If set to `True`, only the filtered data
            (index in ds.filter.all) are used.
        override: bool
            If set to `True`, an existing file ``path`` will be overridden.
            If set to `False`, raises `OSError` if ``path`` exists.

        Notes
        -----
        Raises OSError if current dataset does not contain image data
        """
        if not IMAGEIO_AVAILABLE:
            raise ModuleNotFoundError(
                "Package `imageio` required for avi export!")
        path = pathlib.Path(path)
        ds = self.rtdc_ds
        # Make sure that path ends with .avi
        if path.suffix != ".avi":
            path = path.with_name(path.name + ".avi")
        # Check if file already exist
        if not override and path.exists():
            raise OSError("File already exists: {}\n".format(
                str(path).encode("ascii", "ignore")) +
                "Please use the `override=True` option.")
        # Start exporting
        if "image" in ds:
            # Open video for writing
            vout = imageio.get_writer(uri=path,
                                      format="FFMPEG",
                                      fps=25,
                                      codec="rawvideo",
                                      pixelformat="yuv420p",
                                      macro_block_size=None,
                                      ffmpeg_log_level="error")
            # write the filtered frames to avi file
            for evid in np.arange(len(ds)):
                # skip frames that were filtered out
                if filtered and not ds.filter.all[evid]:
                    continue
                image = ds["image"][evid]
                # Convert image to RGB
                image = image.reshape(image.shape[0], image.shape[1], 1)
                image = np.repeat(image, 3, axis=2)
                vout.append_data(image)
        else:
            msg = "No image data to export: dataset {} !".format(ds.title)
            raise OSError(msg)

    def fcs(self, path, features, meta_data=None, filtered=True,
            override=False):
        """Export the data of an RT-DC dataset to an .fcs file

        Parameters
        ----------
        path: str
            Path to an .fcs file. The ending .fcs is added automatically.
        features: list of str
            The features in the resulting .fcs file. These are strings
            that are defined by `dclab.definitions.scalar_feature_exists`,
            e.g. "area_cvx", "deform", "frame", "fl1_max", "aspect".
        meta_data: dict
            User-defined, optional key-value pairs that are stored
            in the primary TEXT segment of the FCS file; the version
            of dclab is stored there by default
        filtered: bool
            If set to `True`, only the filtered data
            (index in ds.filter.all) are used.
        override: bool
            If set to `True`, an existing file ``path`` will be overridden.
            If set to `False`, raises `OSError` if ``path`` exists.

        Notes
        -----
        Due to incompatibility with the .fcs file format, all events with
        NaN-valued features are not exported.
        """
        if meta_data is None:
            meta_data = {}
        if not FCSWRITE_AVAILABLE:
            raise ModuleNotFoundError(
                "Package `fcswrite` required for fcs export!")

        ds = self.rtdc_ds

        path = pathlib.Path(path)
        # Make sure that path ends with .fcs
        if path.suffix != ".fcs":
            path = path.with_name(path.name + ".fcs")
        # Check if file already exist
        if not override and path.exists():
            raise OSError("File already exists: {}\n".format(
                str(path).encode("ascii", "ignore")) +
                "Please use the `override=True` option.")
        # Check that features are valid
        features = sorted(set(features))
        for c in features:
            if c not in ds.features_scalar:
                msg = "Invalid feature name: {}".format(c)
                raise ValueError(msg)

        # Collect the header
        chn_names = [dfn.get_feature_label(c, rtdc_ds=ds) for c in features]

        # Collect the data
        if filtered:
            data = [ds[c][ds.filter.all] for c in features]
        else:
            data = [ds[c] for c in features]

        data = np.array(data).transpose()
        meta_data["dclab version"] = version
        fcswrite.write_fcs(filename=str(path),
                           chn_names=chn_names,
                           data=data,
                           text_kw_pr=meta_data,
                           )

    def hdf5(self,
             path: str | pathlib.Path,
             features: List[str] = None,
             filtered: bool = True,
             logs: bool = False,
             tables: bool = False,
             basins: bool = False,
             meta_prefix: str = "src_",
             override: bool = False,
             compression_kwargs: Dict = None,
             compression: str = "deprecated",
             skip_checks: bool = False):
        """Export the data of the current instance to an HDF5 file

        Parameters
        ----------
        path: str
            Path to an .rtdc file. The ending .rtdc is added
            automatically.
        features: list of str
            The features in the resulting .rtdc file. These are strings
            that are defined by `dclab.definitions.feature_exists`, e.g.
            "area_cvx", "deform", "frame", "fl1_max", "image".
            Defaults to `self.rtdc_ds.features_innate`.
        filtered: bool
            If set to `True`, only the filtered data
            (index in ds.filter.all) are used.
        logs: bool
            Whether to store the logs of the original file prefixed with
            `source_` to the output file.
        tables: bool
            Whether to store the tables of the original file prefixed with
            `source_` to the output file.
        basins: bool
            Whether to export basins. If filtering is disabled, basins
            are copied directly to the output file. If filtering is enabled,
            then mapped basins are exported.
        meta_prefix: str
            Prefix for log and table names in the exported file
        override: bool
            If set to `True`, an existing file ``path`` will be overridden.
            If set to `False`, raises `OSError` if ``path`` exists.
        compression_kwargs: dict
            Dictionary with the keys "compression" and "compression_opts"
            which are passed to :func:`h5py.H5File.create_dataset`. The
            default is Zstandard compression with the lowest compression
            level `hdf5plugin.Zstd(clevel=1)`.
        compression: str or None
            Compression method used for data storage;
            one of [None, "lzf", "gzip", "szip"].

            .. deprecated:: 0.43.0
                Use `compression_kwargs` instead.
        skip_checks: bool
            Disable checking whether all features have the same length.


        .. versionchanged:: 0.58.0

           The ``basins`` keyword argument was added, and it is now possible
           to pass an empty list to ``features``. This combination results
           in a very small file consisting of metadata and a mapped basin
           referring to the original dataset.
        """
        if compression != "deprecated":
            warnings.warn("The `compression` kwarg is deprecated in favor of "
                          "`compression_kwargs`!",
                          DeprecationWarning)
            if compression_kwargs is not None:
                raise ValueError("You may not specify `compression` and "
                                 "`compression_kwargs` at the same time!")
            # be backwards-compatible
            compression_kwargs = {"compression": compression}
        if compression_kwargs is None:
            compression_kwargs = hdf5plugin.Zstd(clevel=1)
        path = pathlib.Path(path)
        # Make sure that path ends with .rtdc
        if path.suffix not in [".rtdc", ".rtdc~"]:
            path = path.parent / (path.name + ".rtdc")
        # Check if file already exists
        if not override and path.exists():
            raise OSError("File already exists: {}\n".format(path)
                          + "Please use the `override=True` option.")
        elif path.exists():
            path.unlink()

        # make sure the parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # for convenience
        ds = self.rtdc_ds

        if features is None:
            features = ds.features_innate

        # decide which metadata to export
        meta = {}
        # only cfg metadata (no analysis metadata)
        for sec in dfn.CFG_METADATA:
            if sec in ds.config:
                meta[sec] = ds.config[sec].copy()
        # add user-defined metadata
        if "user" in ds.config:
            meta["user"] = ds.config["user"].copy()
        if filtered:
            # Define a new measurement identifier, so that we are not running
            # into any problems with basins being defined for filtered data.
            ds_run_id = ds.get_measurement_identifier()
            random_ap = str(uuid.uuid4())[:4]
            meta["experiment"]["run identifier"] = f"{ds_run_id}-{random_ap}"

        if filtered:
            filter_arr = ds.filter.all
        else:
            filter_arr = None

        features = sorted(set(features))
        if not skip_checks and features:
            # check that all features have same length and use the smallest
            # common length
            lengths = []
            for feat in features:
                if feat == "trace":
                    for tr in list(ds["trace"].keys()):
                        lengths.append(len(ds["trace"][tr]))
                else:
                    lengths.append(len(ds[feat]))
            l_min = np.min(lengths)
            l_max = np.max(lengths)
            if l_min != l_max:
                if filter_arr is None:
                    # we are forced to do filtering
                    filter_arr = np.ones(len(ds), dtype=bool)
                else:
                    # have to create a copy, because rtdc_ds.filter.all is ro!
                    filter_arr = np.copy(filter_arr)
                filter_arr[l_min:] = False
                warnings.warn(
                    "Not all features have the same length! Limiting output "
                    + f"event count to {l_min} (max {l_max}) in '{l_min}'.",
                    LimitingExportSizeWarning)

        # Perform actual export
        with RTDCWriter(path,
                        mode="append",
                        compression_kwargs=compression_kwargs) as hw:
            # write meta data
            hw.store_metadata(meta)

            # write export log
            hw.store_log(time.strftime("dclab-export_%Y-%m-%d_%H.%M.%S"),
                         json.dumps({
                             "dclab version": version_tuple,
                             "kwargs": {
                                 "features": features,
                                 "filtered": filtered,
                                 "logs": logs,
                                 "tables": tables,
                                 "basins": basins,
                                 "meta_prefix": meta_prefix,
                                 "skip_checks": skip_checks
                             }
                         }).split("\n"))

            if logs:
                # write logs
                for log in ds.logs:
                    hw.store_log(f"{meta_prefix}{log}",
                                 ds.logs[log])

            if tables:
                # write tables
                for tab in ds.tables:
                    hw.store_table(f"{meta_prefix}{tab}",
                                   ds.tables[tab])

            # write each feature individually
            for feat in features:
                if (filter_arr is None or
                        # This does not work for the .tdms file format
                        # (and probably also not for DCOR).
                        (np.all(filter_arr) and ds.format == "hdf5")):
                    # We do not have to filter and can be fast
                    if dfn.scalar_feature_exists(feat):
                        shape = (1,)
                    elif feat in ["image", "image_bg", "mask", "trace"]:
                        # known shape
                        shape = None
                    else:
                        shape = np.array(ds[feat][0]).shape
                    hw.store_feature(feat=feat,
                                     data=ds[feat],
                                     shape=shape)
                else:
                    # We have to filter and will be slower
                    store_filtered_feature(rtdc_writer=hw,
                                           feat=feat,
                                           data=ds[feat],
                                           filtarr=filter_arr)

            if basins:
                # We have to store basins. There are three options:
                # - filtering disabled: just copy basins
                # - filtering enabled
                #   - basins with "same" mapping: create new mapping
                #   - mapped basins: correct nested mapping
                # In addition to the basins that we copy from the
                # original dataset, we also create a new basin that
                # refers to the original dataset itself.
                basin_list = [bn.as_dict() for bn in ds.basins]
                # In addition to the upstream basins, also store a reference
                # to the original file from which the export was done.
                if ds.format in get_basin_classes():
                    # The dataset has a format that matches a basin format
                    # directly.
                    basin_is_local = ds.format == "hdf5"
                    basin_locs = [ds.path]
                    if basin_is_local:
                        # So the user can put them into the same directory.
                        basin_locs.append(ds.path.name)
                    basin_list.append({
                        "basin_name": "Exported data",
                        "basin_type": "file" if basin_is_local else "remote",
                        "basin_format": ds.format,
                        "basin_locs": basin_locs,
                        "basin_descr": f"Exported with dclab {version}",
                    })
                elif (ds.format == "hierarchy"
                      and ds.get_root_parent().format in get_basin_classes()):
                    # avoid circular imports
                    from .fmt_hierarchy import map_indices_child2root
                    # The dataset is a hierarchy child, and it is derived
                    # from a dataset that has a matching basin format.
                    # We have to add the indices of the root parent, which
                    # identify the child, to the basin dictionary. Note
                    # that additional basin filtering is applied below
                    # this case for all basins.
                    # For the sake of clarity I wrote this as a separate case,
                    # even if that means duplicating code from the previous
                    # case.
                    ds_root = ds.get_root_parent()
                    basin_is_local = ds_root.format == "hdf5"
                    basin_locs = [ds_root.path]
                    if basin_is_local:
                        # So the user can put them into the same directory.
                        basin_locs.append(ds_root.path.name)
                    basin_list.append({
                        "basin_name": "Exported data (hierarchy)",
                        "basin_type": "file" if basin_is_local else "remote",
                        "basin_format": ds_root.format,
                        "basin_locs": basin_locs,
                        "basin_descr": f"Exported with dclab {version} from a "
                                       f"hierarchy dataset",
                        # This is where this basin differs from the basin
                        # definition in the previous case.
                        "basin_map": map_indices_child2root(
                            child=ds,
                            child_indices=np.arange(len(ds))
                            ),
                    })

                for bn_dict in basin_list:
                    if bn_dict.get("basin_type") == "internal":
                        # Internal basins are only valid for files they were
                        # defined in. Since we are exporting, it does not
                        # make sense to store these basins in the output file.
                        continue
                    basinmap_orig = bn_dict.get("basin_map")
                    if not filtered:
                        # filtering disabled: just copy basins
                        pass
                    elif basinmap_orig is None:
                        # basins with "same" mapping: create new mapping
                        bn_dict["basin_map"] = np.where(filter_arr)[0]
                    else:
                        # mapped basins: correct nested mapping
                        bn_dict["basin_map"] = basinmap_orig[filter_arr]

                    # Do not verify basins, it takes too long.
                    hw.store_basin(**bn_dict, verify=False)

    def tsv(self, path, features, meta_data=None, filtered=True,
            override=False):
        """Export the data of the current instance to a .tsv file

        Parameters
        ----------
        path: str
            Path to a .tsv file. The ending .tsv is added automatically.
        features: list of str
            The features in the resulting .tsv file. These are strings
            that are defined by `dclab.definitions.scalar_feature_exists`,
            e.g. "area_cvx", "deform", "frame", "fl1_max", "aspect".
        meta_data: dict
            User-defined, optional key-value pairs that are stored
            at the beginning of the tsv file - one key-value pair is
            stored per line which starts with a hash. The version of
            dclab is stored there by default.
        filtered: bool
            If set to `True`, only the filtered data
            (index in ds.filter.all) are used.
        override: bool
            If set to `True`, an existing file ``path`` will be overridden.
            If set to `False`, raises `OSError` if ``path`` exists.
        """
        if meta_data is None:
            meta_data = {}
        features = [c.lower() for c in features]
        features = sorted(set(features))
        path = pathlib.Path(path)
        ds = self.rtdc_ds
        # Make sure that path ends with .tsv
        if path.suffix != ".tsv":
            path = path.with_name(path.name + ".tsv")
        # Check if file already exist
        if not override and path.exists():
            raise OSError("File already exists: {}\n".format(
                str(path).encode("ascii", "ignore")) +
                "Please use the `override=True` option.")
        # Check that features exist
        for c in features:
            if c not in ds.features_scalar:
                raise ValueError("Invalid feature name {}".format(c))
        meta_data["dclab version"] = version
        # Write BOM header
        with path.open("wb") as fd:
            fd.write(codecs.BOM_UTF8)
        # Open file
        with path.open("a", encoding="utf-8") as fd:
            # write meta data
            for key in sorted(meta_data.keys()):
                fd.write(f"# {key}: {meta_data[key]}\n")
            fd.write("#\n")
            fd.write("# Original dataset configuration:\n")
            cfg = self.rtdc_ds.config.as_dict()
            for sec in sorted(cfg.keys()):
                for key in sorted(cfg[sec].keys()):
                    fd.write(f"# dc:{sec}:{key} = {cfg[sec][key]}\n")
            fd.write("#\n")
            # write header
            header1 = "\t".join([c for c in features])
            fd.write("# "+header1+"\n")
            labels = [dfn.get_feature_label(c, rtdc_ds=ds) for c in features]
            header2 = "\t".join(labels)
            fd.write("# "+header2+"\n")

        with path.open("ab") as fd:
            # write data
            if filtered:
                data = [ds[c][ds.filter.all] for c in features]
            else:
                data = [ds[c] for c in features]

            np.savetxt(fd,
                       np.array(data).transpose(),
                       fmt=str("%.10e"),
                       delimiter="\t")


def yield_filtered_array_stacks(data, indices):
    """Generator returning chunks with the filtered feature data

    Parameters
    ----------
    data: np.ndarray or h5py.Dataset
        The full, unfiltered input feature data. Must implement
        the `shape` and `dtype` properties. If it implements the
        `__array__` method, fast slicing is used.
    indices: np.ndarray or list
        The indices (integer values) for `data` (first axis), indicating
        which elements should be returned by this generator.

    Notes
    -----
    This method works with any feature dimension (e.g. it
    works for image (2D) data and for trace data (1D)). It
    is just important that `data` is indexable using integers
    and that the events in `data` all have the same shape.
    The dtype of the returned chunks is determined by the first
    item in `data`.

    This method works with sliceable (e.g. np.ndarray) and
    non-sliceable (e.g. tdms-format-based images) input data. If the
    input data is sliceable (which is determined by the availability
    of the `__array__` method, then fast numpy sclicing is used. If the
    input data does not support slicing (`__array__` not defined), then
    a slow iteration over `indices` is done.

    In the slow iteration case, the returned array data are overridden
    in-place. If you need to retain a copy of the `yield`ed chunks,
    apply `np.array(.., copy=True)` to the returned chunks.
    """
    chunk_shape = RTDCWriter.get_best_nd_chunks(item_shape=data.shape[1:],
                                                item_dtype=data.dtype)
    chunk_size = chunk_shape[0]

    if hasattr(data, "__array__"):
        # We have an array-like object and can do slicing with the indexing
        # array. This speeds up chunk creation for e.g. the HDF5 file format
        # where all data are present in an array-like fashion.
        indices = np.array(indices)
        stop = 0
        for kk in range(len(indices) // chunk_size):
            start = chunk_size * kk
            stop = chunk_size * (kk + 1)
            yield data[indices[start:stop]]
        if stop < len(indices):
            yield data[indices[stop:]]
    else:
        # assemble filtered image stacks
        chunk = np.zeros(chunk_shape, dtype=data.dtype)
        jj = 0
        for ii in indices:
            chunk[jj] = data[ii]
            if (jj + 1) % chunk_size == 0:
                jj = 0
                yield chunk
            else:
                jj += 1
        # yield remainder
        if jj:
            yield chunk[:jj]


def store_filtered_feature(rtdc_writer, feat, data, filtarr):
    """Append filtered feature data to an HDF5 file

    Parameters
    ----------
    rtdc_writer: dclab.rtdc_dataset.writer.RTDCWriter
        an open writer object
    feat: str
        feature name
    data: object or list or np.ndarray or dict
        feature data
    filtarr: boolean np.ndarray
        filtering array (same as RTDCBase.filter.all)

    Notes
    -----
    This code is somewhat redundant to the code of RTDCWriter.
    """
    indices = np.where(filtarr)[0]
    if indices.size == 0:
        warnings.warn(f"No data to export to '{rtdc_writer.path}'")
        return

    hw = rtdc_writer
    if not hw.mode == "append":
        raise ValueError("The `rtdc_writer` object must be created with"
                         + f"`mode='append'`, got '{hw.mode}' for '{hw}'!")
    # event-wise, because
    # - tdms-based datasets don't allow indexing with numpy
    # - there might be memory issues
    if feat == "contour":
        for ii in indices:
            hw.store_feature("contour", data[ii])
    elif feat in ["mask", "image", "image_bg"]:
        # assemble filtered image stacks
        for imstack in yield_filtered_array_stacks(data, indices):
            hw.store_feature(feat, imstack)
    elif feat == "trace":
        # assemble filtered trace stacks
        for tr in data.keys():
            for trstack in yield_filtered_array_stacks(data[tr], indices):
                hw.store_feature("trace", {tr: trstack})
    elif dfn.scalar_feature_exists(feat):
        hw.store_feature(feat, data[filtarr])
    else:
        # Special case of plugin or temporary features.
        shape = data[0].shape
        for dstack in yield_filtered_array_stacks(data, indices):
            hw.store_feature(feat, dstack, shape=shape)


def hdf5_append(h5obj, rtdc_ds, feat, compression, filtarr=None,
                time_offset=0):
    """Append feature data to an HDF5 file

    Parameters
    ----------
    h5obj: h5py.File
        Opened HDF5 file
    rtdc_ds: dclab.rtdc_dataset.RTDCBase
        Instance from which to obtain the data
    feat: str
        Valid feature name in `rtdc_ds`
    compression: str or None
        Compression method for "contour", "image", and "trace" data
        as well as logs; one of [None, "lzf", "gzip", "szip"].
    filtarr: None or 1d boolean np.ndarray
        Optional boolean array used for filtering. If set to
        `None`, all events are saved.
    time_offset: float
        Do not use! Please use `dclab.cli.task_join.join` instead.

    Notes
    -----
    Please update the "experiment::event count" attribute manually.
    You may use
    :func:`dclab.rtdc_dataset.writer.RTDCWriter.rectify_metadata`
    for that or use the `RTDCWriter` context manager where it is
    automatically run during `__exit__`.
    """
    # optional array for filtering events
    if filtarr is None:
        filtarr = np.ones(len(rtdc_ds), dtype=bool)
        no_filter = True
    else:
        no_filter = False

    warnings.warn("`hdf5_append` is deptecated; please use "
                  " the dclab.RTDCWriter context manager or the "
                  " export.store_filtered_feature function.",
                  DeprecationWarning)

    if time_offset != 0:
        raise ValueError("Setting `time_offset` not supported anymore! "
                         "Please use `dclab.cli.task_join.join` instead.")

    # writer instance
    hw = RTDCWriter(h5obj, mode="append", compression=compression)
    if no_filter:
        hw.store_feature(feat, rtdc_ds[feat])
    else:
        store_filtered_feature(rtdc_writer=hw,
                               feat=feat,
                               data=rtdc_ds[feat],
                               filtarr=filtarr)


def hdf5_autocomplete_config(path_or_h5obj):
    """Autocomplete the configuration of the RTDC-measurement

    The following configuration keys are updated:

    - experiment:event count
    - fluorescence:samples per event
    - imaging: roi size x (if image or mask is given)
    - imaging: roi size y (if image or mask is given)

    The following configuration keys are added if not present:

    - fluorescence:channel count

    Parameters
    ----------
    path_or_h5obj: pathlib.Path or str or h5py.File
        Path to or opened RT-DC measurement
    """
    warnings.warn("`hdf5_autocomplete_config` is deptecated; please use "
                  " the dclab.RTDCWriter context manager or the "
                  " dclab.RTDCWriter.rectify_metadata function.",
                  DeprecationWarning)
    if not isinstance(path_or_h5obj, h5py.File):
        close = True
    else:
        close = False

    hw = RTDCWriter(path_or_h5obj, mode="append")
    hw.rectify_metadata()

    if close:
        path_or_h5obj.close()
