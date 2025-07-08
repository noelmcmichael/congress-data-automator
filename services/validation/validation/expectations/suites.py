"""Expectation suites for Congressional data validation."""

from typing import List, Dict, Any
from great_expectations.core.expectation_configuration import ExpectationConfiguration

from ..core.logging import get_logger

logger = get_logger(__name__)


class BaseExpectationSuite:
    """Base class for expectation suites."""
    
    def __init__(self, table_name: str):
        """
        Initialize the expectation suite.
        
        Args:
            table_name: Name of the table to validate
        """
        self.table_name = table_name
        self.logger = logger.bind(component=f"{self.__class__.__name__}")
    
    def get_expectations(self) -> List[ExpectationConfiguration]:
        """
        Get list of expectations for the table.
        
        Returns:
            List[ExpectationConfiguration]: List of expectations
        """
        raise NotImplementedError("Subclasses must implement get_expectations")
    
    def get_suite_name(self) -> str:
        """
        Get the name of the expectation suite.
        
        Returns:
            str: Suite name
        """
        return f"{self.table_name}_suite"


class MemberExpectationSuite(BaseExpectationSuite):
    """Expectation suite for Congressional members."""
    
    def get_expectations(self) -> List[ExpectationConfiguration]:
        """Get expectations for members table."""
        return [
            # Required columns should exist
            ExpectationConfiguration(
                expectation_type="expect_table_columns_to_match_ordered_list",
                kwargs={
                    "column_list": [
                        "member_id",
                        "bioguide_id",
                        "first_name",
                        "last_name",
                        "full_name",
                        "chamber",
                        "party",
                        "state",
                        "district",
                        "term_start",
                        "term_end",
                        "in_office",
                        "official_url",
                        "contact_form_url",
                        "source",
                        "created_at",
                        "updated_at",
                    ],
                    "exact_match": False,
                },
            ),
            
            # Member ID should be unique and not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_unique",
                kwargs={"column": "member_id"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "member_id"},
            ),
            
            # Required string fields should not be null or empty
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "first_name"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "last_name"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "full_name"},
            ),
            
            # Chamber should be valid values
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "chamber",
                    "value_set": ["house", "senate"],
                },
            ),
            
            # Party should be valid values
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "party",
                    "value_set": [
                        "Republican",
                        "Democratic", 
                        "Independent",
                        "Libertarian",
                        "Green",
                        "Other",
                    ],
                },
            ),
            
            # State should be valid 2-letter abbreviations
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "state",
                    "regex": "^[A-Z]{2}$",
                },
            ),
            
            # District should be numeric for House members
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "district",
                    "regex": "^[0-9]+$",
                    "mostly": 0.9,  # Allow some nulls for Senate members
                },
            ),
            
            # Senators should not have district numbers
            ExpectationConfiguration(
                expectation_type="expect_column_pair_values_to_be_in_set",
                kwargs={
                    "column_A": "chamber",
                    "column_B": "district",
                    "value_pairs_set": [
                        ("house", "1"), ("house", "2"), ("house", "3"),  # etc.
                        ("senate", None),
                    ],
                    "ignore_row_if": "either_value_is_missing",
                },
            ),
            
            # URLs should be valid HTTP/HTTPS URLs if present
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "official_url",
                    "regex": "^https?://.*",
                    "mostly": 0.8,
                },
            ),
            
            # Source should be specified
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "source"},
            ),
            
            # Term dates should be reasonable
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "term_start",
                    "min_value": "1900-01-01",
                    "max_value": "2030-12-31",
                    "parse_strings_as_datetimes": True,
                },
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "term_end",
                    "min_value": "1900-01-01",
                    "max_value": "2030-12-31",
                    "parse_strings_as_datetimes": True,
                },
            ),
            
            # Data quality checks
            ExpectationConfiguration(
                expectation_type="expect_table_row_count_to_be_between",
                kwargs={
                    "min_value": 400,  # Minimum expected members
                    "max_value": 600,  # Maximum expected members
                },
            ),
        ]


class CommitteeExpectationSuite(BaseExpectationSuite):
    """Expectation suite for Congressional committees."""
    
    def get_expectations(self) -> List[ExpectationConfiguration]:
        """Get expectations for committees table."""
        return [
            # Required columns should exist
            ExpectationConfiguration(
                expectation_type="expect_table_columns_to_match_ordered_list",
                kwargs={
                    "column_list": [
                        "committee_id",
                        "name",
                        "full_name",
                        "chamber",
                        "committee_type",
                        "parent_committee_id",
                        "is_subcommittee",
                        "official_url",
                        "hearings_url",
                        "members_url",
                        "documents_url",
                        "active",
                        "source",
                        "created_at",
                        "updated_at",
                    ],
                    "exact_match": False,
                },
            ),
            
            # Committee ID should be unique and not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_unique",
                kwargs={"column": "committee_id"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "committee_id"},
            ),
            
            # Required string fields should not be null or empty
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "name"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "full_name"},
            ),
            
            # Chamber should be valid values
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "chamber",
                    "value_set": ["house", "senate"],
                },
            ),
            
            # Committee type should be valid
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "committee_type",
                    "value_set": [
                        "standing",
                        "subcommittee",
                        "select",
                        "joint",
                        "special",
                    ],
                },
            ),
            
            # Subcommittee validation
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_of_type",
                kwargs={
                    "column": "is_subcommittee",
                    "type_": "bool",
                },
            ),
            
            # Parent committee validation for subcommittees
            ExpectationConfiguration(
                expectation_type="expect_column_pair_values_to_be_in_set",
                kwargs={
                    "column_A": "is_subcommittee",
                    "column_B": "parent_committee_id",
                    "value_pairs_set": [
                        (True, "not_null"),
                        (False, None),
                    ],
                    "ignore_row_if": "either_value_is_missing",
                },
            ),
            
            # URLs should be valid HTTP/HTTPS URLs if present
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "official_url",
                    "regex": "^https?://.*",
                    "mostly": 0.7,
                },
            ),
            
            # Active should be boolean
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_of_type",
                kwargs={
                    "column": "active",
                    "type_": "bool",
                },
            ),
            
            # Source should be specified
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "source"},
            ),
            
            # Data quality checks
            ExpectationConfiguration(
                expectation_type="expect_table_row_count_to_be_between",
                kwargs={
                    "min_value": 20,   # Minimum expected committees
                    "max_value": 200,  # Maximum expected committees
                },
            ),
        ]


class HearingExpectationSuite(BaseExpectationSuite):
    """Expectation suite for Congressional hearings."""
    
    def get_expectations(self) -> List[ExpectationConfiguration]:
        """Get expectations for hearings table."""
        return [
            # Required columns should exist
            ExpectationConfiguration(
                expectation_type="expect_table_columns_to_match_ordered_list",
                kwargs={
                    "column_list": [
                        "hearing_id",
                        "title",
                        "description",
                        "committee_id",
                        "committee_name",
                        "chamber",
                        "date",
                        "time",
                        "location",
                        "status",
                        "hearing_url",
                        "transcript_url",
                        "video_url",
                        "witnesses",
                        "source",
                        "created_at",
                        "updated_at",
                    ],
                    "exact_match": False,
                },
            ),
            
            # Hearing ID should be unique and not null
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_unique",
                kwargs={"column": "hearing_id"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "hearing_id"},
            ),
            
            # Required string fields should not be null or empty
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "title"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "committee_id"},
            ),
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "committee_name"},
            ),
            
            # Chamber should be valid values
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "chamber",
                    "value_set": ["house", "senate"],
                },
            ),
            
            # Status should be valid
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "status",
                    "value_set": [
                        "scheduled",
                        "completed",
                        "cancelled",
                        "postponed",
                    ],
                },
            ),
            
            # Hearing dates should be reasonable
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_between",
                kwargs={
                    "column": "date",
                    "min_value": "1900-01-01",
                    "max_value": "2030-12-31",
                    "parse_strings_as_datetimes": True,
                },
            ),
            
            # URLs should be valid HTTP/HTTPS URLs if present
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "hearing_url",
                    "regex": "^https?://.*",
                    "mostly": 0.6,
                },
            ),
            
            # Source should be specified
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": "source"},
            ),
            
            # Committee ID should reference valid committees
            # Note: This would require a foreign key constraint or lookup table
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_match_regex",
                kwargs={
                    "column": "committee_id",
                    "regex": "^[A-Z0-9_-]+$",
                },
            ),
            
            # Data quality checks
            ExpectationConfiguration(
                expectation_type="expect_table_row_count_to_be_between",
                kwargs={
                    "min_value": 0,      # Minimum expected hearings
                    "max_value": 10000,  # Maximum expected hearings
                },
            ),
        ]


def get_expectation_suite(table_name: str) -> BaseExpectationSuite:
    """
    Get the appropriate expectation suite for a table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        BaseExpectationSuite: Expectation suite for the table
        
    Raises:
        ValueError: If table name is not recognized
    """
    suite_map = {
        "members": MemberExpectationSuite,
        "committees": CommitteeExpectationSuite,
        "hearings": HearingExpectationSuite,
    }
    
    if table_name not in suite_map:
        raise ValueError(f"Unknown table name: {table_name}")
    
    return suite_map[table_name](table_name)


def create_all_expectation_suites(expectation_manager) -> None:
    """
    Create all expectation suites.
    
    Args:
        expectation_manager: ExpectationManager instance
    """
    tables = ["members", "committees", "hearings"]
    
    for table_name in tables:
        logger.info(f"Creating expectation suite for {table_name}")
        
        suite = get_expectation_suite(table_name)
        expectations = suite.get_expectations()
        
        # Convert ExpectationConfiguration objects to dictionaries
        expectation_dicts = []
        for exp in expectations:
            expectation_dicts.append({
                "expectation_type": exp.expectation_type,
                "kwargs": exp.kwargs,
            })
        
        expectation_manager.create_expectation_suite(
            suite_name=suite.get_suite_name(),
            table_name=table_name,
            expectations=expectation_dicts,
            overwrite=True,
        )
        
        logger.info(f"Created expectation suite for {table_name} with {len(expectations)} expectations")