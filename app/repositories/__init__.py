"""Persistence repositories."""

from app.repositories.domain_repository import DomainRepository
from app.repositories.obesity_record_repository import ObesityRecordRepository

__all__ = ["DomainRepository", "ObesityRecordRepository"]
