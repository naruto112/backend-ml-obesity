"""Request and response schemas."""

from app.schemas.domain_schema import DomainFieldSchema, DomainListSchema, StatusSchema
from app.schemas.obesity_record_schema import (
    ObesityRecordCreatedSchema,
    ObesityRecordCreateSchema,
    ObesityRecordPageSchema,
    ObesityRecordReadSchema,
    PageQuerySchema,
    PaginationMetaSchema,
)
from app.schemas.problem_schema import ProblemSchema

__all__ = [
    "DomainFieldSchema",
    "DomainListSchema",
    "ObesityRecordCreateSchema",
    "ObesityRecordCreatedSchema",
    "ObesityRecordPageSchema",
    "ObesityRecordReadSchema",
    "PageQuerySchema",
    "PaginationMetaSchema",
    "ProblemSchema",
    "StatusSchema",
]
