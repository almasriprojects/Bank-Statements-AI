from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class ValidationDetails(BaseModel):
    balances_match: bool
    all_transactions_processed: bool
    date_range_covered: str
    missing_transactions: List[str] = []
    rounding_differences: float


class Metadata(BaseModel):
    bank_name: str
    account_number: str
    account_holder: str
    year: str
    month: str
    currency: str
    parsed_by: str = "BankStatementParser v1.0"
    parsed_on: datetime = Field(default_factory=datetime.utcnow)
    processing_duration: str
    timezone: str = "UTC"
    validation_status: str
    validation_details: ValidationDetails


class FileMetadata(BaseModel):
    file_name: str
    file_size: str
    file_hash: str


class TotalTransactions(BaseModel):
    Total_Deposits: float
    Recurring_Deposits: float
    One_Off_Deposits: float
    Total_Withdrawals: float
    Recurring_Withdrawals: float
    Irregular_Withdrawals: float
    Net_Change: float


class CheckingSummary(BaseModel):
    Beginning_Balance: float
    Deposits_and_Additions: float
    Electronic_Withdrawals: float
    Ending_Balance: float


class FlaggedTransaction(BaseModel):
    is_high_value: bool
    reason: str = ""


class TransactionDetail(BaseModel):
    id: int
    Date: str
    Description: str
    Transaction_Type: str
    Category: str
    Amount: float
    Balance: float
    Category_Confidence: float
    Location: str = ""
    Notes: str = ""
    Flagged: FlaggedTransaction


class LargestTransaction(BaseModel):
    Description: str
    Amount: float
    Date: str


class SpendingAnalysis(BaseModel):
    total_spent_on_subscriptions: float
    largest_transaction: LargestTransaction
    average_daily_spending: float


class ErrorTracking(BaseModel):
    unprocessed_sections: List[str] = []
    parsing_errors: List[str] = []


class BankStatementData(BaseModel):
    metadata: Metadata
    file_metadata: FileMetadata
    Total_Transactions: TotalTransactions
    Checking_Summary: CheckingSummary
    Transaction_Detail: List[TransactionDetail]
    spending_analysis: SpendingAnalysis
    error_tracking: ErrorTracking


class ExtractionResponse(BaseModel):
    status: str = "success"
    data: BankStatementData


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheckResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow) 