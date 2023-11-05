import os
from pathlib import Path
import csv
import re
import uuid
import pandas as pd
from pydicom import dcmread
from tqdm import tqdm
from loguru import logger
from typing import List, Dict

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

# 주어진 CSV파일 읽어서 MRN (Medical Record Number), ID (Identifier)로 이루어진 딕셔너리를 생성하는 함수
def read_csv_mapping(path: Path) -> Dict[str, str]:
    df = pd.read_csv(path)
    return {str(mrn): str(id) for mrn, id in zip(df.mrn, df.id)}

# src_dcm_dir 디렉토리 내에서 ".zip" 확장자를 제외한 모든 파일과 폴더의 경로를 재귀적으로 검색하여 반환
def get_dcm_paths(src_dcm_dir: Path) -> List[Path]:
    return list(src_dcm_dir.rglob("*[!.zip]"))

def prepare_output_dir(src_dcm_dir: Path, subj: str) -> Path:
    deid_dcm_dir_name = src_dcm_dir.parent.name + "_deid"
    deid_dcm_dir = src_dcm_dir.parent / deid_dcm_dir_name / f"{subj}_{src_dcm_dir.name}"
    deid_dcm_dir.mkdir(parents=True, exist_ok=True)
    return deid_dcm_dir

def analyze_dcm_series(dcm_paths: List[Path], subj: str) -> Dict[str, Dict[str, str]]:
    series_metadata = {}
    for dcm_path in tqdm(dcm_paths, desc="Analyzing series", position=1, leave=False):
        dcm = dcmread(dcm_path, force=True)
        try:
            series_uid = dcm.SeriesInstanceUID
        except AttributeError:
            logger.error(f"{dcm_path} - No SeriesInstanceUID")
            continue

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
        for series_data in series_metadata.values():
            writer.writerow(series_data)

def parse_series_description(description: str) -> str:
    clean_description = description.strip().replace(".", "P")
    return re.sub(r"\W+", "_", clean_description)

def deidentify(dcm_path: Path, output_dir: Path, subj: str):
    dcm = dcmread(dcm_path)
    parsed_description = parse_series_description(dcm.SeriesDescription)
    deid_series_dir = output_dir / f"DCM_{subj}_{parsed_description}"
    deid_series_dir.mkdir(parents=True, exist_ok=True)

    # Overwrite PatientID, PatientName, Patient BirthDate
    dcm.PatientID = subj
    dcm.PatientName = f"{subj}_{dcm.AcquisitionDate}"
    dcm.PatientBirthDate = dcm.PatientBirthDate[:-4] + "0101"

    # Remove PHI, private tags
    for tag in TAGS_TO_ANONYMIZE:
        if tag in dcm:
            delattr(dcm, tag)
    dcm.remove_private_tags()

    deid_dcm_path = deid_series_dir / dcm_path.name
    dcm.save_as(deid_dcm_path)

def run_deidentifier(src_dcm_dir: Path, mrn_id_mapping: Dict[str, str]):
    dcm_paths = get_dcm_paths(src_dcm_dir)
    subj = str(uuid.uuid4())
    output_dir = prepare_output_dir(src_dcm_dir, subj) if dst_path is None else Path(dst_path)
    series_metadata = analyze_dcm_series(dcm_paths, subj)
    export_series_metadata(series_metadata, output_dir)

    for dcm_path in tqdm(dcm_paths, desc="De-identifying", position=1, leave=False):
        deidentify(dcm_path, output_dir, subj)

def main(src_paths: List[str]):
    total_dirs = sum(1 for src_path in src_paths if Path(src_path).is_dir())
    total_files = sum(1 for src_path in src_paths if not Path(src_path).is_dir())
    total_count = total_dirs + total_files
    progress = 0
    processed_dirs = 0
    processed_files = 0
    dir_index = 0
    deid_performed = False

    for src_path in src_paths:
        src_path = Path(src_path).resolve()
        mrn_id_mapping = read_csv_mapping(csv_path) if csv_path else {}

        if src_path.is_dir():
            dir_count = len(list(filter(Path.is_dir, src_path.iterdir())))

            for dir_index, src_dcm_dir in enumerate(src_path.iterdir(), start=1):
                if src_dcm_dir.is_dir() and src_dcm_dir.name.startswith('DCM'):
                    run_deidentifier(src_dcm_dir, mrn_id_mapping)
                    deid_performed = True
                # Update progress percentage
                progress = (processed_dirs + dir_index / dir_count) / total_count
                print(f"Progress: {progress:.2%}")
                yield progress
            processed_dirs += 1
            print(processed_dirs)
        else:
            yield "Invalid DICOM directory"

    if not deid_performed:
        yield "De-identification has not been performed. Please provide a valid DICOM directory."
    else:
        yield f"De-identification completed with {progress:.2%} progress."
