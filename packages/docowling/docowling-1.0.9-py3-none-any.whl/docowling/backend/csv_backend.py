import csv
from io import BytesIO, StringIO
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union
import logging

from docling_core.types.doc import GroupItem
from docling_core.types.doc import (
    DoclingDocument,
    DocumentOrigin,
    GroupLabel,
    TableCell,
    TableData,
)
from pydantic import BaseModel
from docowling.backend.abstract_backend import DeclarativeDocumentBackend
from docowling.datamodel.base_models import InputFormat
from docowling.datamodel.document import InputDocument

_log = logging.getLogger(__name__)

class CsvCell(BaseModel):
    row: int
    col: int
    text: str
    row_span: int = 1
    col_span: int = 1

class CsvTable(BaseModel):
    num_rows: int
    num_cols: int
    data: List[CsvCell]

class CsvDocumentBackend(DeclarativeDocumentBackend):
    def __init__(self, in_doc: "InputDocument", path_or_stream: Union[BytesIO, Path]):
        super().__init__(in_doc, path_or_stream)
        self.rows = []
        self.parents: Dict[int, GroupItem] = {}
        self.file = path_or_stream if isinstance(path_or_stream, Path) else None
        self.max_levels = 10
        
        for i in range(-1, self.max_levels):
            self.parents[i] = None
        
        try:
            # Load the CSV data
            if isinstance(self.path_or_stream, Path):
                with self.path_or_stream.open(mode="r", encoding="utf-8") as file:
                    self.rows = list(csv.reader(file))
            elif isinstance(self.path_or_stream, BytesIO):
                # Convert BytesIO to StringIO for CSV reading
                text_content = self.path_or_stream.read().decode("utf-8")
                self.rows = list(csv.reader(StringIO(text_content)))
            
            # Add debug logging
            _log.info(f"Loaded {len(self.rows)} rows from CSV file")
            self.valid = True
        except Exception as e:
            self.valid = False
            raise RuntimeError(
                f"CsvDocumentBackend could not load document with hash {self.document_hash}"
            ) from e

    def is_valid(self) -> bool:
        return self.valid

    @classmethod
    def supports_pagination(cls) -> bool:
        return False  # Typically, CSV files do not support pagination.

    def unload(self):
        self.path_or_stream = None

    @classmethod
    def supported_formats(cls) -> Set[InputFormat]:
        return {InputFormat.CSV}

    def convert(self) -> DoclingDocument:
        # Handle the filename for both Path and BytesIO cases
        if isinstance(self.path_or_stream, Path):
            filename = self.path_or_stream.name
            stem = self.path_or_stream.stem
        else:
            filename = "file.csv"
            stem = "file"

        origin = DocumentOrigin(
            filename=filename,
            mimetype="text/csv",
            binary_hash=self.document_hash,
        )
        doc = DoclingDocument(name=stem, origin=origin)

        if self.is_valid():
            doc = self._convert_csv_to_document(doc)
        else:
            raise RuntimeError(
                f"Cannot convert doc with {self.document_hash} because the backend failed to init."
            )

        return doc
    
    def _convert_csv_to_document(self, doc: DoclingDocument) -> DoclingDocument:
        if not self.rows:
            _log.info(f"no self.rows")
            return doc
            
        # Find separator 
        separator = None
        with self.path_or_stream.open(mode="r", encoding="utf-8") as file:
            sample = file.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            separator = dialect.delimiter
        if separator is None:
            separator = ","

        # Create table data structure
        num_rows = len(self.rows)
        num_cols = max(len(row) for row in self.rows)
        
        data = TableData(num_rows=num_rows, num_cols=num_cols, table_cells=[])

        # Convert CSV cells to TableCell objects
        for row_idx, row in enumerate(self.rows):
            for col_idx, cell_text in enumerate(row):
                cell = TableCell(
                    text=str(cell_text).strip(),
                    row_span=1,  # CSV cells don't typically have spans
                    col_span=1,
                    start_row_offset_idx=row_idx,
                    end_row_offset_idx=row_idx + 1,
                    start_col_offset_idx=col_idx, 
                    end_col_offset_idx=col_idx + 1,
                    col_header=(row_idx == 0),  # First row as header
                    row_header=(col_idx == 0)   # First column as header
                )
                data.table_cells.append(cell)

        # Add table to document
        doc.add_table(data=data, parent=None)  # Top level table

        return doc