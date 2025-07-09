# Plan: Wikipedia Data Integration for 119th Congress

This plan outlines the step-by-step process for integrating Wikipedia as a data source to enhance the accuracy and completeness of the congressional data, focusing on member, committee, and leadership information.

### Phase 1: Develop a Wikipedia Scraping Service (2-3 hours)

**Goal**: Create a new, independent service to scrape and structure data from the 119th Congress Wikipedia pages.

- **Step 1.1: Create Scraper File**: Create a new file `wikipedia_scraper.py` in `backend/app/services/`. This scraper will be responsible for fetching and parsing the HTML from the provided Wikipedia URLs.
- **Step 1.2: Scrape Member Data**: Implement a function to parse the House and Senate member tables, extracting each member's name, state, party, and district/class.
- **Step 1.3: Scrape Committee & Leadership Data**: Implement a function to parse the committee tables, extracting the committee name, chamber, and the explicitly listed Chair and Ranking Member for each.
- **Step 1.4: Structure and Store Scraped Data**: The scraper will output the collected data into a structured JSON file (e.g., `wikipedia_data.json`) for use by the reconciliation service.
- **Step 1.5: Commit Initial Scraper**: Commit the first version of the `wikipedia_scraper.py` and the initial JSON output.

### Phase 2: Create a Data Reconciliation & Update Service (2-3 hours)

**Goal**: Develop a service that compares data from the `congress.gov` API with the new Wikipedia data and updates the database.

- **Step 2.1: Create Reconciliation Service**: Create a new file `data_reconciler.py` in `backend/app/services/`. This service will be responsible for the core logic of comparing and merging the two data sources.
- **Step 2.2: Implement Member Reconciliation**: Write logic to match members from both sources (e.g., using name and state). This will serve as the basis for validating committee assignments.
- **Step 2.3: Implement Leadership Reconciliation**: For each committee, compare the leadership roles. The Wikipedia data (with its explicit "Chair" and "Ranking Member" labels) will be treated as the authoritative source for these specific titles. The service will generate SQL update statements to correct leadership roles in the database.
- **Step 2.4: Implement Committee Roster Validation**: Compare the member rosters for each committee between the two sources. Log any discrepancies for manual review (e.g., members present in one source but not the other).
- **Step 2.5: Execute Database Updates**: The reconciliation service will execute the generated SQL statements to update the database, correcting committee leadership information.
- **Step 2.6: Commit Reconciliation Service**: Commit the new service and a report of the initial updates made.

### Phase 3: Integration and Automation (1-2 hours)

**Goal**: Integrate the new scraping and reconciliation process into the project's existing automated workflows.

- **Step 3.1: Update Main Data Processor**: Modify the existing `data_processor.py` or create a new orchestration script to run the `wikipedia_scraper.py` and `data_reconciler.py` after the main `congress_api.py` runs.
- **Step 3.2: Integrate with Monitoring**: Ensure that the new services are integrated with the existing monitoring and alerting system. The system should generate an alert if the Wikipedia pages change structure or if significant data discrepancies are found.
- **Step 3.3: Full System Test**: Run the entire data pipeline end-to-end to ensure all services work together correctly and the database is populated with accurate, validated data.
- **Step 3.4: Documentation**: Update the `README.md` to reflect the new data sources and the enhanced validation process.

### Phase 4: Final Review and Validation

**Goal**: Verify that the data inaccuracies have been resolved and the system is stable.

- **Step 4.1: Manual Data Verification**: Manually check the data for a few key committees (e.g., Senate Judiciary) via the API or frontend to confirm that the leadership and member rosters are now accurate.
- **Step 4.2: Review Discrepancy Reports**: Analyze the discrepancy logs to identify any remaining data quality issues that may require further attention.
- **Step 4.3: Final Commit**: Commit any final code changes and documentation updates.
