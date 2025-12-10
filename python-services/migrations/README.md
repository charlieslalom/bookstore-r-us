# Database Migrations

This directory contains database migration scripts for Bookstore-R-Us Python services.

## Migration System

- **Simple, explicit migrations**: Each migration is a numbered Python file
- **Order matters**: Migrations run in numerical order (001, 002, 003, ...)
- **Reversible**: Each migration has `up()` and `down()` functions
- **Tracked**: Applied migrations are recorded in `migrations_history` table

## Usage

### Run all pending migrations
```bash
cd python-services/migrations
python migrate.py up
```

### Run migrations up to a specific version
```bash
python migrate.py up --target 002_add_users
```

### Rollback last migration
```bash
python migrate.py down
```

### Rollback specific migration
```bash
python migrate.py down --migration 002_add_users
```

### Check migration status
```bash
python migrate.py status
```

## Creating a New Migration

1. **Create file**: `NNN_description.py` (e.g., `002_add_user_roles.py`)
2. **Implement functions**:
   ```python
   async def up():
       # Apply migration
       session_maker = get_session_maker()
       async with session_maker() as session:
           await session.execute(text("CREATE TABLE ..."))
           await session.commit()
   
   async def down():
       # Rollback migration
       session_maker = get_session_maker()
       async with session_maker() as session:
           await session.execute(text("DROP TABLE ..."))
           await session.commit()
   ```

## Migration Naming Convention

Format: `NNN_brief_description.py`

Examples:
- `001_initial_schema.py` - Initial database setup
- `002_create_products_table.py` - Products service tables
- `003_create_cart_tables.py` - Cart service tables
- `004_add_user_roles_column.py` - Add roles to users table

## Best Practices

1. **Keep migrations small**: One logical change per migration
2. **Test rollbacks**: Always implement and test `down()` function
3. **Idempotent**: Use `IF NOT EXISTS` where possible
4. **Explicit**: Don't rely on SQLModel auto-creation in migrations
5. **Data migrations**: Separate schema and data migrations

## Migration History

Applied migrations are tracked in the `migrations_history` table:

```sql
CREATE TABLE migrations_history (
    id SERIAL PRIMARY KEY,
    migration VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Integration with Services

Services should:
1. Define SQLModel models in their codebase
2. Create service-specific migrations for table creation
3. Run migrations on deployment
4. Use SQLModel for ORM operations (not raw SQL)

## Environment Setup

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string (YSQL)

Example:
```bash
export DATABASE_URL="postgresql+asyncpg://yugabyte:yugabyte@localhost:5433/yugabyte"
```
