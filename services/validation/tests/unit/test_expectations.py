"""Test expectation suites."""

import pytest
from great_expectations.core.expectation_configuration import ExpectationConfiguration

from validation.expectations.suites import (
    MemberExpectationSuite,
    CommitteeExpectationSuite,
    HearingExpectationSuite,
    get_expectation_suite,
)


class TestMemberExpectationSuite:
    """Test Member expectation suite."""
    
    def test_suite_creation(self):
        """Test creating member expectation suite."""
        suite = MemberExpectationSuite("members")
        expectations = suite.get_expectations()
        
        assert len(expectations) > 0
        assert suite.get_suite_name() == "members_suite"
        
        # Check that all expectations are valid ExpectationConfiguration objects
        for expectation in expectations:
            assert isinstance(expectation, ExpectationConfiguration)
            assert hasattr(expectation, 'expectation_type')
            assert hasattr(expectation, 'kwargs')
    
    def test_required_expectations(self):
        """Test that required expectations are present."""
        suite = MemberExpectationSuite("members")
        expectations = suite.get_expectations()
        
        expectation_types = [exp.expectation_type for exp in expectations]
        
        # Should have column uniqueness check
        assert "expect_column_values_to_be_unique" in expectation_types
        
        # Should have not null checks
        assert "expect_column_values_to_not_be_null" in expectation_types
        
        # Should have value set checks for chamber and party
        assert "expect_column_values_to_be_in_set" in expectation_types
        
        # Should have regex checks for state
        assert "expect_column_values_to_match_regex" in expectation_types
        
        # Should have row count check
        assert "expect_table_row_count_to_be_between" in expectation_types


class TestCommitteeExpectationSuite:
    """Test Committee expectation suite."""
    
    def test_suite_creation(self):
        """Test creating committee expectation suite."""
        suite = CommitteeExpectationSuite("committees")
        expectations = suite.get_expectations()
        
        assert len(expectations) > 0
        assert suite.get_suite_name() == "committees_suite"
    
    def test_committee_specific_expectations(self):
        """Test committee-specific expectations."""
        suite = CommitteeExpectationSuite("committees")
        expectations = suite.get_expectations()
        
        expectation_types = [exp.expectation_type for exp in expectations]
        
        # Should have boolean type check for is_subcommittee
        assert "expect_column_values_to_be_of_type" in expectation_types
        
        # Should have pair validation for subcommittee relationships
        assert "expect_column_pair_values_to_be_in_set" in expectation_types


class TestHearingExpectationSuite:
    """Test Hearing expectation suite."""
    
    def test_suite_creation(self):
        """Test creating hearing expectation suite."""
        suite = HearingExpectationSuite("hearings")
        expectations = suite.get_expectations()
        
        assert len(expectations) > 0
        assert suite.get_suite_name() == "hearings_suite"
    
    def test_hearing_specific_expectations(self):
        """Test hearing-specific expectations."""
        suite = HearingExpectationSuite("hearings")
        expectations = suite.get_expectations()
        
        expectation_types = [exp.expectation_type for exp in expectations]
        
        # Should have date range validation
        assert "expect_column_values_to_be_between" in expectation_types
        
        # Should have status validation
        assert "expect_column_values_to_be_in_set" in expectation_types


class TestSuiteFactory:
    """Test expectation suite factory function."""
    
    def test_get_expectation_suite_valid_tables(self):
        """Test getting expectation suites for valid tables."""
        members_suite = get_expectation_suite("members")
        assert isinstance(members_suite, MemberExpectationSuite)
        assert members_suite.table_name == "members"
        
        committees_suite = get_expectation_suite("committees")
        assert isinstance(committees_suite, CommitteeExpectationSuite)
        assert committees_suite.table_name == "committees"
        
        hearings_suite = get_expectation_suite("hearings")
        assert isinstance(hearings_suite, HearingExpectationSuite)
        assert hearings_suite.table_name == "hearings"
    
    def test_get_expectation_suite_invalid_table(self):
        """Test getting expectation suite for invalid table."""
        with pytest.raises(ValueError, match="Unknown table name"):
            get_expectation_suite("invalid_table")


class TestExpectationContent:
    """Test specific expectation content."""
    
    def test_member_chamber_validation(self):
        """Test member chamber validation expectations."""
        suite = MemberExpectationSuite("members")
        expectations = suite.get_expectations()
        
        # Find chamber validation expectation
        chamber_expectations = [
            exp for exp in expectations
            if exp.expectation_type == "expect_column_values_to_be_in_set"
            and exp.kwargs.get("column") == "chamber"
        ]
        
        assert len(chamber_expectations) == 1
        chamber_exp = chamber_expectations[0]
        assert set(chamber_exp.kwargs["value_set"]) == {"house", "senate"}
    
    def test_member_party_validation(self):
        """Test member party validation expectations."""
        suite = MemberExpectationSuite("members")
        expectations = suite.get_expectations()
        
        # Find party validation expectation
        party_expectations = [
            exp for exp in expectations
            if exp.expectation_type == "expect_column_values_to_be_in_set"
            and exp.kwargs.get("column") == "party"
        ]
        
        assert len(party_expectations) == 1
        party_exp = party_expectations[0]
        expected_parties = {
            "Republican", "Democratic", "Independent", 
            "Libertarian", "Green", "Other"
        }
        assert set(party_exp.kwargs["value_set"]) == expected_parties
    
    def test_hearing_status_validation(self):
        """Test hearing status validation expectations."""
        suite = HearingExpectationSuite("hearings")
        expectations = suite.get_expectations()
        
        # Find status validation expectation
        status_expectations = [
            exp for exp in expectations
            if exp.expectation_type == "expect_column_values_to_be_in_set"
            and exp.kwargs.get("column") == "status"
        ]
        
        assert len(status_expectations) == 1
        status_exp = status_expectations[0]
        expected_statuses = {"scheduled", "completed", "cancelled", "postponed"}
        assert set(status_exp.kwargs["value_set"]) == expected_statuses