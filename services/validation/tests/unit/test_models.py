"""Test data models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from validation.models.congressional import (
    Member, Committee, Hearing, ValidationResult, DataPromotion,
    ChamberType, PartyType, HearingStatus
)


class TestMember:
    """Test Member model."""
    
    def test_valid_member(self):
        """Test creating a valid member."""
        member = Member(
            member_id="M123456",
            first_name="John",
            last_name="Doe",
            full_name="John Doe",
            chamber=ChamberType.HOUSE,
            party=PartyType.DEMOCRAT,
            state="CA",
            district="12",
            source="test",
        )
        
        assert member.member_id == "M123456"
        assert member.chamber == ChamberType.HOUSE
        assert member.party == PartyType.DEMOCRAT
        assert member.state == "CA"
        assert member.district == "12"
    
    def test_state_validation(self):
        """Test state validation."""
        # Valid state
        member = Member(
            member_id="M123456",
            first_name="John",
            last_name="Doe", 
            full_name="John Doe",
            chamber=ChamberType.HOUSE,
            party=PartyType.DEMOCRAT,
            state="ca",  # Should be converted to uppercase
            source="test",
        )
        assert member.state == "CA"
        
        # Invalid state
        with pytest.raises(ValidationError):
            Member(
                member_id="M123456",
                first_name="John",
                last_name="Doe",
                full_name="John Doe", 
                chamber=ChamberType.HOUSE,
                party=PartyType.DEMOCRAT,
                state="California",  # Too long
                source="test",
            )
    
    def test_senate_district_validation(self):
        """Test that senators cannot have districts."""
        with pytest.raises(ValidationError):
            Member(
                member_id="S123456",
                first_name="Jane",
                last_name="Smith",
                full_name="Jane Smith",
                chamber=ChamberType.SENATE,
                party=PartyType.REPUBLICAN,
                state="TX",
                district="1",  # Senators shouldn't have districts
                source="test",
            )


class TestCommittee:
    """Test Committee model."""
    
    def test_valid_committee(self):
        """Test creating a valid committee."""
        committee = Committee(
            committee_id="HSAG",
            name="Agriculture",
            full_name="House Committee on Agriculture",
            chamber=ChamberType.HOUSE,
            committee_type="standing",
            source="test",
        )
        
        assert committee.committee_id == "HSAG"
        assert committee.chamber == ChamberType.HOUSE
        assert committee.committee_type == "standing"
        assert committee.is_subcommittee is False
    
    def test_subcommittee_validation(self):
        """Test subcommittee validation."""
        # Valid subcommittee
        subcommittee = Committee(
            committee_id="HSAG01",
            name="Livestock",
            full_name="Subcommittee on Livestock",
            chamber=ChamberType.HOUSE,
            committee_type="subcommittee",
            parent_committee_id="HSAG",
            is_subcommittee=True,
            source="test",
        )
        
        assert subcommittee.is_subcommittee is True
        assert subcommittee.parent_committee_id == "HSAG"
        
        # Invalid: subcommittee without parent
        with pytest.raises(ValidationError):
            Committee(
                committee_id="HSAG01",
                name="Livestock",
                full_name="Subcommittee on Livestock",
                chamber=ChamberType.HOUSE,
                committee_type="subcommittee",
                is_subcommittee=True,
                source="test",
            )


class TestHearing:
    """Test Hearing model."""
    
    def test_valid_hearing(self):
        """Test creating a valid hearing."""
        hearing = Hearing(
            hearing_id="H20250108001",
            title="Budget Oversight Hearing",
            committee_id="HSBU",
            committee_name="Budget",
            chamber=ChamberType.HOUSE,
            status=HearingStatus.SCHEDULED,
            source="test",
        )
        
        assert hearing.hearing_id == "H20250108001"
        assert hearing.chamber == ChamberType.HOUSE
        assert hearing.status == HearingStatus.SCHEDULED
    
    def test_date_validation(self):
        """Test hearing date validation."""
        # Valid date
        hearing = Hearing(
            hearing_id="H20250108001",
            title="Budget Oversight Hearing",
            committee_id="HSBU",
            committee_name="Budget",
            chamber=ChamberType.HOUSE,
            status=HearingStatus.SCHEDULED,
            date=datetime(2025, 1, 15),
            source="test",
        )
        assert hearing.date.year == 2025
        
        # Invalid date (too old)
        with pytest.raises(ValidationError):
            Hearing(
                hearing_id="H18500101001",
                title="Old Hearing",
                committee_id="HSBU",
                committee_name="Budget",
                chamber=ChamberType.HOUSE,
                status=HearingStatus.COMPLETED,
                date=datetime(1850, 1, 1),
                source="test",
            )


class TestValidationResult:
    """Test ValidationResult model."""
    
    def test_validation_result(self):
        """Test creating a validation result."""
        result = ValidationResult(
            table_name="members",
            expectation_suite="members_suite",
            run_id="members_20250108_120000",
            success=True,
            results_count=10,
            successful_expectations=9,
            unsuccessful_expectations=1,
            run_time=datetime.now(),
            duration_seconds=5.5,
        )
        
        assert result.success is True
        assert result.success_rate == 90.0
        assert result.duration_seconds == 5.5
    
    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        # Normal case
        result = ValidationResult(
            table_name="test",
            expectation_suite="test_suite",
            run_id="test_run",
            success=True,
            results_count=20,
            successful_expectations=18,
            unsuccessful_expectations=2,
            run_time=datetime.now(),
            duration_seconds=1.0,
        )
        assert result.success_rate == 90.0
        
        # Zero results case
        result = ValidationResult(
            table_name="test",
            expectation_suite="test_suite",
            run_id="test_run",
            success=False,
            results_count=0,
            successful_expectations=0,
            unsuccessful_expectations=0,
            run_time=datetime.now(),
            duration_seconds=1.0,
        )
        assert result.success_rate == 0.0


class TestDataPromotion:
    """Test DataPromotion model."""
    
    def test_data_promotion(self):
        """Test creating a data promotion."""
        started_at = datetime.now()
        completed_at = datetime.now()
        
        promotion = DataPromotion(
            promotion_id="members_20250108_120000",
            table_name="members",
            source_schema="staging",
            target_schema="public",
            target_table="members_v20250708",
            records_processed=1000,
            records_promoted=950,
            records_failed=50,
            success=True,
            started_at=started_at,
            completed_at=completed_at,
        )
        
        assert promotion.success is True
        assert promotion.success_rate == 95.0
        assert promotion.duration_seconds is not None
    
    def test_promotion_properties(self):
        """Test promotion property calculations."""
        promotion = DataPromotion(
            promotion_id="test_promotion",
            table_name="test",
            source_schema="staging",
            target_schema="public",
            target_table="test_v20250708",
            records_processed=100,
            records_promoted=80,
            records_failed=20,
            success=True,
            started_at=datetime.now(),
        )
        
        # No completed_at, so duration should be None
        assert promotion.duration_seconds is None
        assert promotion.success_rate == 80.0
        
        # Zero records case
        promotion_empty = DataPromotion(
            promotion_id="empty_promotion",
            table_name="empty",
            source_schema="staging",
            target_schema="public",
            target_table="empty_v20250708",
            records_processed=0,
            records_promoted=0,
            records_failed=0,
            success=True,
            started_at=datetime.now(),
        )
        assert promotion_empty.success_rate == 0.0