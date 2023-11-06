import os
from pathlib import Path
import csv
import re
import uuid
import pandas as pd
from pydicom import dcmread
from tqdm import tqdm
from typing import List, Dict, Generator

# Constants
# Constants
TAGS_TO_ANONYMIZE = [
    "PatientSex", "PatientAge", "InstitutionName", "InstitutionAddress",
    "InstitutionalDepartmentName", "ReferringPhysicianName", "ReferringPhysicianTelephoneNumbers",
    "ReferringPhysicianAddress", "PhysiciansOfRecord", "OperatorsName", "IssuerOfPatientID",
    "OtherPatientIDs", "OtherPatientNames", "OtherPatientIDsSequence", "PatientBirthName", "PatientSize",
    "PatientWeight", "PatientAddress", "PatientMotherBirthName", "CountryOfResidence", "RegionOfResidence",
    "CurrentPatientLocation", "PatientTelephoneNumbers", "SmokingStatus", "PregnancyStatus",
    "PatientReligiousPreference", "RequestingPhysician", "PerformingPhysicianName", "NameOfPhysiciansReadingStudy",
    "MilitaryRank", "EthnicGroup", "AdditionalPatientHistory", "PatientComments", "PersonName",
    "ScheduledPatientInstitutionResidence",
]

dst_path = None
csv_path = None

def read_csv_mapping(path: str) -> Dict[str, str]:
    df = pd.read_csv(path)
    return dict(zip(map(str, df.mrn), map(str, df.id)))

def get_dcm_paths(src_dcm_dir: Path) -> List[Path]:
    return list(src_dcm_dir.rglob("*[!.zip]"))

def prepare_output_dir(parent_dir: Path, src_dcm_dir_name: str, subj: str) -> Path:
    deid_dcm_dir = parent_dir / f"{parent_dir.name}_deid" / f"{subj}_{src_dcm_dir_name}"
    deid_dcm_dir.mkdir(parents=True, exist_ok=True)
    return deid_dcm_dir

def analyze_dcm_series(dcm_paths: List[Path], subj: str) -> Dict[str, Dict[str, str]]:
    series_metadata = {}
    for dcm_path in tqdm(dcm_paths, desc="Analyzing series", position=1, leave=False):
        dcm = dcmread(dcm_path, force=True)
        series_uid = dcm.SeriesInstanceUID
        if series_uid not in series_metadata:
            series_metadata[series_uid] = {
                'subj': subj,
                'ct_date': getattr(dcm, "AcquisitionDate", ""),
                'MRN': getattr(dcm, "PatientID", ""),
            }
    return series_metadata

def export_series_metadata(series_metadata: Dict[str, Dict[str, str]], output_dir: Path):
    csv_path = output_dir / "dcm_metadata.csv"
    with csv_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["subj", "MRN", "ct_date"])
        writer.writeheader()
        writer.writerows(series_metadata.values())

def parse_series_description(description: str) -> str:
    clean_description = description.strip().replace(".", "P")
    return re.sub(r"\W+", "_", clean_description)

def deidentify_dcm_file(dcm: dcmread, subj: str) -> None:
    dcm.PatientID = subj
    dcm.PatientName = f"{subj}_{dcm.AcquisitionDate}"
    dcm.PatientBirthDate = dcm.PatientBirthDate[:-4] + "0101"
    for tag in TAGS_TO_ANONYMIZE:
        if tag in dcm:
            delattr(dcm, tag)
    dcm.remove_private_tags()

def process_dcm_file(dcm_path: Path, output_dir: Path, subj: str) -> None:
    dcm = dcmread(dcm_path)
    parsed_description = parse_series_description(dcm.SeriesDescription)
    deid_series_dir = output_dir / f"DCM_{subj}_{parsed_description}"
    deid_series_dir.mkdir(parents=True, exist_ok=True)

    deidentify_dcm_file(dcm, subj)

    deid_dcm_path = deid_series_dir / dcm_path.name
    dcm.save_as(deid_dcm_path)

def run_deidentifier(src_dcm_dir: Path, mrn_id_mapping: Dict[str, str], dst_path: Path = None):
    dcm_paths = get_dcm_paths(src_dcm_dir)
    subj = mrn_id_mapping.get(src_dcm_dir.name, str(uuid.uuid4()))
    output_dir = prepare_output_dir(src_dcm_dir.parent, src_dcm_dir.name, subj) if dst_path is None else dst_path

    series_metadata = analyze_dcm_series(dcm_paths, subj)
    export_series_metadata(series_metadata, output_dir)

    for dcm_path in tqdm(dcm_paths, desc="De-identifying", position=1, leave=False):
        process_dcm_file(dcm_path, output_dir, subj)

def update_progress(processed: int, total: int, current: int, current_total: int) -> float:
    return (processed + (current / current_total)) / total

def process_directory(src_path: Path, mrn_id_mapping: dict, processed_dirs: int, total_count: int) -> bool:
    deid_performed = False
    dir_count = len(list(filter(Path.is_dir, src_path.iterdir())))

    for dir_index, src_dcm_dir in enumerate(src_path.iterdir(), start=1):
        if src_dcm_dir.is_dir() and src_dcm_dir.name.startswith('DCM'):
            run_deidentifier(src_dcm_dir, mrn_id_mapping)
            deid_performed = True

        progress = update_progress(processed_dirs, total_count, dir_index, dir_count)
        yield progress, deid_performed

    return deid_performed

def count_directories_and_files(src_paths: List[str]) -> (int, int):
    total_dirs = sum(1 for src_path in src_paths if Path(src_path).is_dir())
    total_files = sum(1 for src_path in src_paths if not Path(src_path).is_dir())
    return total_dirs, total_files

def main(src_paths: List[str]) -> Generator:
    total_dirs, total_files = count_directories_and_files(src_paths)
    total_count = total_dirs + total_files
    processed_dirs = 0
    deid_performed = False

    for src_path in src_paths:
        src_path = Path(src_path).resolve()
        mrn_id_mapping = read_csv_mapping(csv_path) if csv_path else {}

        if src_path.is_dir():
            for progress, dir_deid_performed in process_directory(src_path, mrn_id_mapping, processed_dirs, total_count):
                deid_performed = deid_performed or dir_deid_performed
                yield progress
            processed_dirs += 1
        else:
            yield "🔴 Invalid DICOM directory"

    if not deid_performed:
        yield "🔴 De-identification has not been performed. Please provide a valid DICOM directory."
    else:
        yield f"✅ De-identification process completed. Please check the file path for confirmation."
