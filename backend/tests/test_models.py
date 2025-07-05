"""
Tests for database models.
"""
import pytest
from datetime import datetime
from app.models import Member, Committee, CommitteeMembership, Hearing, Witness, HearingDocument


def test_member_model():
    """Test Member model creation and properties."""
    member = Member(
        bioguide_id="A000001",
        first_name="John",
        last_name="Doe",
        party="Democratic",
        chamber="House",
        state="CA",
        district="1",
        is_current=True
    )
    
    assert member.bioguide_id == "A000001"
    assert member.full_name == "John Doe"
    assert member.display_name == "John Doe"
    assert member.chamber == "House"
    assert member.is_current is True


def test_member_with_nickname():
    """Test Member model with nickname."""
    member = Member(
        bioguide_id="A000002",
        first_name="Robert",
        last_name="Smith",
        nickname="Bob",
        party="Republican",
        chamber="Senate",
        state="TX",
    )
    
    assert member.full_name == "Robert Smith"
    assert member.display_name == "Bob Smith"


def test_member_with_suffix():
    """Test Member model with suffix."""
    member = Member(
        bioguide_id="A000003",
        first_name="John",
        last_name="Johnson",
        suffix="Jr.",
        party="Independent",
        chamber="House",
        state="NY",
        district="15"
    )
    
    assert member.full_name == "John Johnson Jr."


def test_committee_model():
    """Test Committee model creation and properties."""
    committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing",
        is_subcommittee=False,
        is_active=True
    )
    
    assert committee.name == "Committee on Agriculture"
    assert committee.full_name == "Committee on Agriculture"
    assert committee.chamber == "House"
    assert committee.is_subcommittee is False
    assert committee.is_active is True


def test_subcommittee_model():
    """Test subcommittee model and relationships."""
    parent_committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing",
        is_subcommittee=False
    )
    
    subcommittee = Committee(
        name="Subcommittee on Livestock",
        chamber="House",
        committee_type="Standing",
        is_subcommittee=True,
        parent_committee=parent_committee
    )
    
    assert subcommittee.is_subcommittee is True
    assert subcommittee.parent_committee == parent_committee
    assert subcommittee.full_name == "Committee on Agriculture - Subcommittee on Livestock"


def test_committee_membership():
    """Test CommitteeMembership model."""
    member = Member(
        bioguide_id="A000004",
        first_name="Jane",
        last_name="Doe",
        party="Democratic",
        chamber="House",
        state="CA"
    )
    
    committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing"
    )
    
    membership = CommitteeMembership(
        member=member,
        committee=committee,
        position="Chair",
        is_current=True
    )
    
    assert membership.member == member
    assert membership.committee == committee
    assert membership.position == "Chair"
    assert membership.is_current is True


def test_hearing_model():
    """Test Hearing model."""
    committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing"
    )
    
    hearing = Hearing(
        title="Hearing on Agricultural Policy",
        committee=committee,
        scheduled_date=datetime(2025, 1, 15, 10, 0),
        location="Room 1100",
        hearing_type="Hearing",
        status="Scheduled"
    )
    
    assert hearing.title == "Hearing on Agricultural Policy"
    assert hearing.committee == committee
    assert hearing.location == "Room 1100"
    assert hearing.status == "Scheduled"


def test_witness_model():
    """Test Witness model."""
    committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing"
    )
    
    hearing = Hearing(
        title="Hearing on Agricultural Policy",
        committee=committee,
        status="Scheduled"
    )
    
    witness = Witness(
        hearing=hearing,
        name="Dr. John Expert",
        title="Professor of Agriculture",
        organization="University of Agriculture"
    )
    
    assert witness.name == "Dr. John Expert"
    assert witness.title == "Professor of Agriculture"
    assert witness.organization == "University of Agriculture"
    assert witness.hearing == hearing


def test_hearing_document_model():
    """Test HearingDocument model."""
    committee = Committee(
        name="Committee on Agriculture",
        chamber="House",
        committee_type="Standing"
    )
    
    hearing = Hearing(
        title="Hearing on Agricultural Policy",
        committee=committee,
        status="Scheduled"
    )
    
    document = HearingDocument(
        hearing=hearing,
        title="Witness Testimony",
        document_type="Testimony",
        url="https://example.com/testimony.pdf",
        file_type="pdf"
    )
    
    assert document.title == "Witness Testimony"
    assert document.document_type == "Testimony"
    assert document.url == "https://example.com/testimony.pdf"
    assert document.file_type == "pdf"
    assert document.hearing == hearing