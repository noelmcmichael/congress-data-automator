"""
Database optimization utilities for Congressional Data Automation Service.
Implements indexing strategies and query optimization.
"""
import structlog
from sqlalchemy import text, Index, create_engine
from sqlalchemy.pool import QueuePool
from .config import settings
from .database import engine

logger = structlog.get_logger()


class DatabaseOptimizer:
    """Handles database optimization operations."""
    
    def __init__(self):
        self.engine = engine
    
    async def create_performance_indexes(self):
        """Create database indexes for better query performance."""
        indexes_to_create = [
            # Members table indexes
            "CREATE INDEX IF NOT EXISTS idx_members_state_district ON members(state, district);",
            "CREATE INDEX IF NOT EXISTS idx_members_party ON members(party);",
            "CREATE INDEX IF NOT EXISTS idx_members_chamber ON members(chamber);",
            "CREATE INDEX IF NOT EXISTS idx_members_voting_status ON members(voting_status);",
            "CREATE INDEX IF NOT EXISTS idx_members_name_search ON members(first_name, last_name);",
            
            # Committees table indexes
            "CREATE INDEX IF NOT EXISTS idx_committees_chamber ON committees(chamber);",
            "CREATE INDEX IF NOT EXISTS idx_committees_type ON committees(committee_type);",
            "CREATE INDEX IF NOT EXISTS idx_committees_parent ON committees(parent_committee_id);",
            "CREATE INDEX IF NOT EXISTS idx_committees_name_search ON committees(name);",
            
            # Committee memberships indexes
            "CREATE INDEX IF NOT EXISTS idx_committee_memberships_member ON committee_memberships(member_id);",
            "CREATE INDEX IF NOT EXISTS idx_committee_memberships_committee ON committee_memberships(committee_id);",
            "CREATE INDEX IF NOT EXISTS idx_committee_memberships_role ON committee_memberships(role);",
            
            # Hearings table indexes
            "CREATE INDEX IF NOT EXISTS idx_hearings_date ON hearings(date);",
            "CREATE INDEX IF NOT EXISTS idx_hearings_committee ON hearings(committee_id);",
            "CREATE INDEX IF NOT EXISTS idx_hearings_title_search ON hearings(title);",
            
            # Congressional sessions indexes
            "CREATE INDEX IF NOT EXISTS idx_congressional_sessions_number ON congressional_sessions(congress_number);",
            "CREATE INDEX IF NOT EXISTS idx_congressional_sessions_dates ON congressional_sessions(start_date, end_date);",
            
            # Composite indexes for common query patterns
            "CREATE INDEX IF NOT EXISTS idx_members_state_party ON members(state, party);",
            "CREATE INDEX IF NOT EXISTS idx_committees_chamber_type ON committees(chamber, committee_type);",
            "CREATE INDEX IF NOT EXISTS idx_hearings_date_committee ON hearings(date, committee_id);",
        ]
        
        created_count = 0
        failed_count = 0
        
        try:
            with self.engine.begin() as conn:
                for index_sql in indexes_to_create:
                    try:
                        conn.execute(text(index_sql))
                        created_count += 1
                        logger.debug(f"Created index: {index_sql[:50]}...")
                    except Exception as e:
                        failed_count += 1
                        logger.warning(f"Failed to create index: {e}")
            
            logger.info(f"Database indexing complete: {created_count} created, {failed_count} failed")
            return {"created": created_count, "failed": failed_count}
            
        except Exception as e:
            logger.error(f"Database indexing failed: {e}")
            return {"created": 0, "failed": len(indexes_to_create)}
    
    async def analyze_query_performance(self):
        """Analyze database query performance and statistics."""
        try:
            with self.engine.begin() as conn:
                # Get table sizes
                table_stats = {}
                tables = ['members', 'committees', 'committee_memberships', 'hearings', 'congressional_sessions']
                
                for table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    table_stats[table] = count
                
                # Get index usage (SQLite specific)
                index_stats = []
                try:
                    result = conn.execute(text("PRAGMA index_list('members')"))
                    member_indexes = result.fetchall()
                    index_stats.append({"table": "members", "indexes": len(member_indexes)})
                except:
                    # Not SQLite, skip index analysis
                    pass
                
                return {
                    "table_statistics": table_stats,
                    "index_statistics": index_stats,
                    "total_records": sum(table_stats.values())
                }
        
        except Exception as e:
            logger.error(f"Query performance analysis failed: {e}")
            return {"error": str(e)}
    
    async def optimize_connection_pool(self):
        """Optimize database connection pool settings."""
        try:
            # Get current pool status
            pool = self.engine.pool
            pool_stats = {
                "pool_size": getattr(pool, 'size', 'N/A'),
                "checked_in": getattr(pool, 'checkedin', 'N/A'),
                "checked_out": getattr(pool, 'checkedout', 'N/A'),
                "overflow": getattr(pool, 'overflow', 'N/A'),
            }
            
            logger.info(f"Connection pool status: {pool_stats}")
            return pool_stats
            
        except Exception as e:
            logger.error(f"Connection pool optimization failed: {e}")
            return {"error": str(e)}


# Create optimized engine with connection pooling
def create_optimized_engine():
    """Create database engine with optimized connection pooling."""
    return create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=10,  # Number of connections to maintain in pool
        max_overflow=20,  # Additional connections beyond pool_size
        pool_pre_ping=True,  # Validate connections before use
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=settings.database_echo,
    )


# Global database optimizer instance
db_optimizer = DatabaseOptimizer()


async def setup_database_optimization():
    """Setup all database optimizations."""
    logger.info("Starting database optimization setup")
    
    # Create performance indexes
    index_results = await db_optimizer.create_performance_indexes()
    
    # Analyze current performance
    performance_stats = await db_optimizer.analyze_query_performance()
    
    # Optimize connection pool
    pool_stats = await db_optimizer.optimize_connection_pool()
    
    optimization_summary = {
        "indexes": index_results,
        "performance": performance_stats,
        "connection_pool": pool_stats,
        "status": "complete"
    }
    
    logger.info(f"Database optimization complete: {optimization_summary}")
    return optimization_summary