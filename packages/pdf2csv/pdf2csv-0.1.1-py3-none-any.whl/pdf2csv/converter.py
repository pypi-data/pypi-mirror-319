import logging
import time
from pathlib import Path
from typing import List, Optional, Any

import pandas as pd
from docling.document_converter import DocumentConverter

_log = logging.getLogger(__name__)


def convert(
    pdf_path: str,
    output_dir: Optional[str] = None,
    rtl: bool = False,
    **kwargs: Any,
) -> List[pd.DataFrame]:
    """
    Convert a PDF file into a list of pandas DataFrames using Docling.

    The function extracts tables from the given PDF, optionally reversing text
    if the PDF is in a right-to-left language or if text is incorrectly extracted.
    If `output_dir` is provided, it saves each extracted table to a CSV file.

    Parameters
    ----------
    pdf_path : str
        Path to the input PDF file.
    output_dir : Optional[str], optional
        Directory where CSV files will be saved. If not provided, CSVs won't be saved.
    rtl : bool, optional
        Whether to reverse text for right-to-left format (False). If True, text in cells
        (and column headers) will be reversed. Defaults to False.
    **kwargs : Any
        Additional arguments passed to `pd.DataFrame.to_csv(...)`, such as `index=False`,
        `sep=';'`, etc.

    Returns
    -------
    List[pd.DataFrame]
        A list of DataFrames, one for each table extracted from the PDF.

    Raises
    ------
    FileNotFoundError
        If the PDF file does not exist.
    Exception
        If any unexpected error occurs during the conversion process.
    """
    start_time = time.time()
    pdf_path_obj = Path(pdf_path)

    if not pdf_path_obj.exists():
        _log.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Initialize Docling's converter
    doc_converter = DocumentConverter()

    try:
        conversion_result = doc_converter.convert(pdf_path)
    except Exception as exc:
        _log.error(f"Failed to convert {pdf_path}: {exc}", exc_info=True)
        raise

    tables = conversion_result.document.tables
    dfs: List[pd.DataFrame] = []
    doc_filename = pdf_path_obj.stem  # for naming output CSVs

    # Create output directory if specified
    output_dir_path: Optional[Path] = None
    if output_dir is not None:
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        _log.debug(f"Created/verified output directory: {output_dir_path}")

    if not tables:
        _log.warning(f"No tables were found in {pdf_path}. Returning empty list.")
        return dfs

    for table_idx, table in enumerate(tables, start=1):
        try:
            df: pd.DataFrame = table.export_to_dataframe()

            # Reverse text if rtl=True
            if rtl:
                for col in df.select_dtypes(include=["object"]).columns:
                    df[col] = df[col].apply(
                        lambda x: x[::-1] if isinstance(x, str) else x
                    )
                # Attempt to reverse column headers as well
                try:
                    df.columns = df.columns.str[::-1]
                except Exception as reverse_col_exc:
                    _log.warning(
                        f"Unable to reverse column headers for table {table_idx}: {reverse_col_exc}"
                    )

            # Store DataFrame in the list
            dfs.append(df)

            # Optionally save to CSV
            if output_dir_path is not None:
                csv_filename = output_dir_path / f"{doc_filename}-table-{table_idx}.csv"
                df.to_csv(csv_filename, **kwargs)
                _log.info(f"Saved CSV table #{table_idx} to: {csv_filename}")

        except Exception as table_exc:
            _log.error(
                f"Error processing table #{table_idx} in {pdf_path}: {table_exc}",
                exc_info=True,
            )

    _log.debug(
        f"Finished processing {pdf_path} in {time.time() - start_time:.2f} seconds. "
        f"Extracted {len(dfs)} tables."
    )

    return dfs
