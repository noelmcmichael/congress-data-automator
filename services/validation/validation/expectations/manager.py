"""Great Expectations manager for validation service."""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
from datetime import datetime

import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context import DataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.exceptions import DataContextError
from great_expectations.checkpoint import SimpleCheckpoint

from ..core.config import settings
from ..core.logging import get_logger
from ..core.database import db_manager
from ..models.congressional import ValidationResult

logger = get_logger(__name__)


class ExpectationManager:
    """Manager for Great Expectations data validation."""

    def __init__(self, data_context_root: Optional[str] = None):
        """
        Initialize the expectation manager.
        
        Args:
            data_context_root: Root directory for Great Expectations context
        """
        self.data_context_root = Path(data_context_root or settings.ge_data_context_root)
        self.data_context: Optional[DataContext] = None
        self.logger = logger.bind(component="expectation_manager")

    def initialize_data_context(self) -> DataContext:
        """
        Initialize Great Expectations data context.
        
        Returns:
            DataContext: Initialized data context
        """
        try:
            if self.data_context_root.exists():
                self.logger.info("Loading existing Great Expectations context")
                self.data_context = gx.get_context(
                    context_root_dir=str(self.data_context_root)
                )
            else:
                self.logger.info("Creating new Great Expectations context")
                self.data_context = self._create_data_context()
                
            return self.data_context
            
        except Exception as e:
            self.logger.error("Failed to initialize Great Expectations context", error=str(e))
            raise

    def _create_data_context(self) -> DataContext:
        """
        Create a new Great Expectations data context.
        
        Returns:
            DataContext: Newly created data context
        """
        # Create data context directory
        self.data_context_root.mkdir(parents=True, exist_ok=True)
        
        # Create data context configuration
        data_context_config = DataContextConfig(
            config_version=3.0,
            plugins_directory="plugins/",
            stores={
                "expectations_store": {
                    "class_name": "ExpectationsStore",
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": "expectations/",
                    },
                },
                "validations_store": {
                    "class_name": "ValidationsStore",
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": "validations/",
                    },
                },
                "evaluation_parameter_store": {
                    "class_name": "EvaluationParameterStore",
                },
                "checkpoint_store": {
                    "class_name": "CheckpointStore",
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": "checkpoints/",
                    },
                },
            },
            expectations_store_name="expectations_store",
            validations_store_name="validations_store",
            evaluation_parameter_store_name="evaluation_parameter_store",
            checkpoint_store_name="checkpoint_store",
            data_docs_sites={
                "local_site": {
                    "class_name": "SiteBuilder",
                    "show_how_to_buttons": True,
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": "data_docs/",
                    },
                    "site_index_builder": {
                        "class_name": "DefaultSiteIndexBuilder",
                    },
                },
            },
            config_variables_file_path="config_variables.yml",
            anonymous_usage_statistics={
                "enabled": False,
            },
        )
        
        # Create the data context
        context = DataContext(
            data_context_config,
            context_root_dir=str(self.data_context_root),
        )
        
        # Create necessary directories
        for directory in ["expectations", "validations", "checkpoints", "data_docs", "plugins"]:
            (self.data_context_root / directory).mkdir(exist_ok=True)
            
        self.logger.info("Created Great Expectations data context")
        return context

    def create_datasource(self, datasource_name: str = "postgresql_datasource") -> None:
        """
        Create a PostgreSQL datasource for Great Expectations.
        
        Args:
            datasource_name: Name of the datasource
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        # Check if datasource already exists
        try:
            existing_datasource = self.data_context.get_datasource(datasource_name)
            self.logger.info("PostgreSQL datasource already exists", datasource_name=datasource_name)
            return
        except DataContextError:
            pass  # Datasource doesn't exist, we'll create it
        
        # Create datasource configuration
        datasource_config = {
            "name": datasource_name,
            "class_name": "Datasource",
            "execution_engine": {
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": settings.database_url,
            },
            "data_connectors": {
                "default_runtime_data_connector": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["default_identifier_name"],
                },
            },
        }
        
        # Add datasource to context
        self.data_context.add_datasource(**datasource_config)
        
        self.logger.info("Created PostgreSQL datasource", datasource_name=datasource_name)

    def create_expectation_suite(
        self,
        suite_name: str,
        table_name: str,
        expectations: List[Dict[str, Any]],
        overwrite: bool = False,
    ) -> None:
        """
        Create an expectation suite.
        
        Args:
            suite_name: Name of the expectation suite
            table_name: Name of the table to validate
            expectations: List of expectation configurations
            overwrite: Whether to overwrite existing suite
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        # Check if suite already exists
        try:
            existing_suite = self.data_context.get_expectation_suite(suite_name)
            if not overwrite:
                self.logger.info("Expectation suite already exists", suite_name=suite_name)
                return
            else:
                self.logger.info("Overwriting existing expectation suite", suite_name=suite_name)
        except DataContextError:
            pass  # Suite doesn't exist, we'll create it
        
        # Create expectation suite
        suite = self.data_context.create_expectation_suite(
            suite_name, overwrite_existing=overwrite
        )
        
        # Add expectations to suite
        for expectation_config in expectations:
            suite.add_expectation(expectation_config)
        
        # Save the suite
        self.data_context.save_expectation_suite(suite)
        
        self.logger.info(
            "Created expectation suite",
            suite_name=suite_name,
            table_name=table_name,
            expectations_count=len(expectations),
        )

    def validate_table(
        self,
        table_name: str,
        suite_name: str,
        schema_name: str = "staging",
        datasource_name: str = "postgresql_datasource",
    ) -> ValidationResult:
        """
        Validate a table using an expectation suite.
        
        Args:
            table_name: Name of the table to validate
            suite_name: Name of the expectation suite
            schema_name: Database schema name
            datasource_name: Name of the datasource
            
        Returns:
            ValidationResult: Validation results
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        start_time = datetime.now()
        run_id = f"{table_name}_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Create batch request
            batch_request = RuntimeBatchRequest(
                datasource_name=datasource_name,
                data_connector_name="default_runtime_data_connector",
                data_asset_name=f"{schema_name}.{table_name}",
                runtime_parameters={"query": f"SELECT * FROM {schema_name}.{table_name}"},
                batch_identifiers={"default_identifier_name": run_id},
            )
            
            # Create validator
            validator = self.data_context.get_validator(
                batch_request=batch_request,
                expectation_suite_name=suite_name,
            )
            
            # Run validation
            results = validator.validate()
            
            # Calculate metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            validation_result = ValidationResult(
                table_name=table_name,
                expectation_suite=suite_name,
                run_id=run_id,
                success=results.success,
                results_count=len(results.results),
                successful_expectations=len([r for r in results.results if r.success]),
                unsuccessful_expectations=len([r for r in results.results if not r.success]),
                run_time=start_time,
                duration_seconds=duration,
                validation_details=results.to_json_dict(),
            )
            
            self.logger.info(
                "Table validation completed",
                table_name=table_name,
                suite_name=suite_name,
                success=results.success,
                duration_seconds=duration,
                success_rate=validation_result.success_rate,
            )
            
            return validation_result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.error(
                "Table validation failed",
                table_name=table_name,
                suite_name=suite_name,
                error=str(e),
                duration_seconds=duration,
            )
            
            # Return failed validation result
            return ValidationResult(
                table_name=table_name,
                expectation_suite=suite_name,
                run_id=run_id,
                success=False,
                results_count=0,
                successful_expectations=0,
                unsuccessful_expectations=1,
                run_time=start_time,
                duration_seconds=duration,
                validation_details={"error": str(e)},
            )

    def create_checkpoint(
        self,
        checkpoint_name: str,
        suite_name: str,
        table_name: str,
        schema_name: str = "staging",
        datasource_name: str = "postgresql_datasource",
    ) -> None:
        """
        Create a checkpoint for automated validation.
        
        Args:
            checkpoint_name: Name of the checkpoint
            suite_name: Name of the expectation suite
            table_name: Name of the table to validate
            schema_name: Database schema name
            datasource_name: Name of the datasource
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        # Create checkpoint configuration
        checkpoint_config = {
            "name": checkpoint_name,
            "config_version": 1.0,
            "template_name": None,
            "module_name": "great_expectations.checkpoint",
            "class_name": "SimpleCheckpoint",
            "run_name_template": f"{table_name}_%Y%m%d_%H%M%S",
            "validations": [
                {
                    "batch_request": {
                        "datasource_name": datasource_name,
                        "data_connector_name": "default_runtime_data_connector",
                        "data_asset_name": f"{schema_name}.{table_name}",
                        "runtime_parameters": {
                            "query": f"SELECT * FROM {schema_name}.{table_name}"
                        },
                        "batch_identifiers": {"default_identifier_name": "default_identifier"},
                    },
                    "expectation_suite_name": suite_name,
                }
            ],
            "profilers": [],
            "ge_cloud_id": None,
            "expectation_suite_ge_cloud_id": None,
        }
        
        # Add checkpoint to context
        self.data_context.add_checkpoint(**checkpoint_config)
        
        self.logger.info(
            "Created checkpoint",
            checkpoint_name=checkpoint_name,
            suite_name=suite_name,
            table_name=table_name,
        )

    def run_checkpoint(self, checkpoint_name: str) -> ValidationResult:
        """
        Run a checkpoint.
        
        Args:
            checkpoint_name: Name of the checkpoint to run
            
        Returns:
            ValidationResult: Validation results
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        start_time = datetime.now()
        run_id = f"{checkpoint_name}_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Get checkpoint
            checkpoint = self.data_context.get_checkpoint(checkpoint_name)
            
            # Run checkpoint
            results = checkpoint.run()
            
            # Calculate metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Extract validation results
            validation_results = results.list_validation_results()
            if validation_results:
                validation_result = validation_results[0]
                
                return ValidationResult(
                    table_name=checkpoint_name,
                    expectation_suite=validation_result.expectation_suite_name,
                    run_id=run_id,
                    success=validation_result.success,
                    results_count=len(validation_result.results),
                    successful_expectations=len([r for r in validation_result.results if r.success]),
                    unsuccessful_expectations=len([r for r in validation_result.results if not r.success]),
                    run_time=start_time,
                    duration_seconds=duration,
                    validation_details=validation_result.to_json_dict(),
                )
            else:
                # No validation results
                return ValidationResult(
                    table_name=checkpoint_name,
                    expectation_suite="unknown",
                    run_id=run_id,
                    success=False,
                    results_count=0,
                    successful_expectations=0,
                    unsuccessful_expectations=1,
                    run_time=start_time,
                    duration_seconds=duration,
                    validation_details={"error": "No validation results"},
                )
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.error(
                "Checkpoint run failed",
                checkpoint_name=checkpoint_name,
                error=str(e),
                duration_seconds=duration,
            )
            
            return ValidationResult(
                table_name=checkpoint_name,
                expectation_suite="unknown",
                run_id=run_id,
                success=False,
                results_count=0,
                successful_expectations=0,
                unsuccessful_expectations=1,
                run_time=start_time,
                duration_seconds=duration,
                validation_details={"error": str(e)},
            )

    def build_data_docs(self) -> None:
        """Build Great Expectations data documentation."""
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        try:
            self.data_context.build_data_docs()
            self.logger.info("Built Great Expectations data documentation")
        except Exception as e:
            self.logger.error("Failed to build data documentation", error=str(e))
            raise

    def get_validation_results(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent validation results.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of validation results
        """
        if not self.data_context:
            self.data_context = self.initialize_data_context()
            
        try:
            # Get validation results from store
            validations_store = self.data_context.validations_store
            validation_keys = validations_store.list_keys()
            
            # Limit results
            validation_keys = validation_keys[:limit]
            
            results = []
            for key in validation_keys:
                try:
                    validation_result = validations_store.get(key)
                    results.append(validation_result.to_json_dict())
                except Exception as e:
                    self.logger.warning("Failed to load validation result", key=str(key), error=str(e))
                    
            return results
            
        except Exception as e:
            self.logger.error("Failed to get validation results", error=str(e))
            return []


# Global expectation manager instance
expectation_manager = ExpectationManager()