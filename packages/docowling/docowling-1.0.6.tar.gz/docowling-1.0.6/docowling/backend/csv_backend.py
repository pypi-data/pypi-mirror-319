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
            return doc

        # Create main section
        self.parents[0] = doc.add_group(
            parent=None,
            label=GroupLabel.SECTION,
            name="CSV Data",
        )

        # Find tables in CSV
        tables = self._find_data_tables()
        
        for csv_table in tables:
            table_data = TableData(
                num_rows=csv_table.num_rows,
                num_cols=csv_table.num_cols,
                table_cells=[],
            )

            for csv_cell in csv_table.data:
                cell = TableCell(
                    text=csv_cell.text,
                    row_span=csv_cell.row_span,
                    col_span=csv_cell.col_span,
                    start_row_offset_idx=csv_cell.row,
                    end_row_offset_idx=csv_cell.row + csv_cell.row_span,
                    start_col_offset_idx=csv_cell.col,
                    end_col_offset_idx=csv_cell.col + csv_cell.col_span,
                    col_header=csv_cell.row == 0,  # First row as header
                    row_header=csv_cell.col == 0,  # First column as header
                )
                table_data.table_cells.append(cell)

            doc.add_table(data=table_data, parent=self.parents[0])

        return doc

    def _find_data_tables(self) -> List[CsvTable]:
        """Find all data tables in CSV"""
        if not self.rows:
            return []

        # For CSV we treat the entire content as one table
        num_rows = len(self.rows)
        num_cols = max(len(row) for row in self.rows)
        
        data = []
        for row_idx, row in enumerate(self.rows):
            for col_idx, cell_value in enumerate(row):
                # Skip empty cells
                if cell_value is None or cell_value.strip() == '':
                    continue
                    
                data.append(
                    CsvCell(
                        row=row_idx,
                        col=col_idx,
                        text=str(cell_value).strip(),
                    )
                )

        return [CsvTable(
            num_rows=num_rows,
            num_cols=num_cols,
            data=data
        )]
