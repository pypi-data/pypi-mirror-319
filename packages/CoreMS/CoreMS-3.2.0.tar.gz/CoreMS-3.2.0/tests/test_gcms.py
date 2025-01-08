import warnings

warnings.filterwarnings("ignore")

import os
import sys
from multiprocessing import Pool

from corems.mass_spectra.calc.GC_RI_Calibration import get_rt_ri_pairs
from corems.mass_spectra.input.andiNetCDF import ReadAndiNetCDF
from corems.molecular_id.search.compoundSearch import LowResMassSpectralMatch
from corems.molecular_id.search.database_interfaces import MetabRefGCInterface


def start_gcms_metabref_sql(normalize=False, url="sqlite://"):
    # Initialize MetabRef interface
    metabref = MetabRefGCInterface()

    # Pull contents into SQLite
    return metabref.get_library(format="sql")


def start_fames_metabref_sql(normalize=False, url="sqlite://"):
    # Initialize MetabRef interface
    metabref = MetabRefGCInterface()

    # Pull contents into SQLite
    return metabref.get_fames(format="sql")


def get_gcms(filepath):
    # Initialize reader
    reader_gcms = ReadAndiNetCDF(filepath)

    # Run reader
    reader_gcms.run()

    # Get GCMS object
    gcms = reader_gcms.get_gcms_obj()

    # # Process chromatogram
    # gcms.process_chromatogram()

    return gcms


def run(args):
    # Unpack arguments
    filepath, ref_dict, cal_filepath = args

    # Parse supplied file
    gcms = get_gcms(filepath)

    # Process chromatogram
    gcms.process_chromatogram()

    # Calibrate retention index
    gcms.calibrate_ri(ref_dict, cal_filepath)

    # Initialize GCMS refeerence database from MetabRef
    sql_obj = start_gcms_metabref_sql()

    # Initialize spectral match
    lowResSearch = LowResMassSpectralMatch(gcms, sql_obj=sql_obj)

    # Run spectral match
    lowResSearch.run()

    return gcms


def test_gcms_workflow():
    # # Define paths
    # filepath = None
    # calibration_filepath = None

    # # Set token
    # TOKEN_PATH = "metabref.token"
    # MetabRefGCInterface().set_token(TOKEN_PATH)

    # # Parse supplied calibration data
    # gcms_ref_obj = get_gcms(calibration_filepath)

    # # Build calibration SQLite database from MetabRef
    # fames_sql_obj = start_fames_metabref_sql()

    # # Determine calibration pairs
    # rt_ri_pairs = get_rt_ri_pairs(gcms_ref_obj, sql_obj=fames_sql_obj)

    # # Execute
    # run((filepath, rt_ri_pairs, calibration_filepath))
    pass
