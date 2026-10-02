# services/knowledge/app/graph/migrations/phase11_schema.sql
-- Phase 11 Neo4j schema migrations
-- Create constraints and indexes for new node types used in Phase 11

// Constraint to ensure unique Formulation nodes by name
CREATE CONSTRAINT formulation_name_unique IF NOT EXISTS ON (f:Formulation) ASSERT f.name IS UNIQUE;

// Constraint for RegionalHerb nodes by name
CREATE CONSTRAINT regional_herb_name_unique IF NOT EXISTS ON (h:RegionalHerb) ASSERT h.name IS UNIQUE;

// Constraint for DietItem nodes by food_name (assuming a node label DietItem)
CREATE CONSTRAINT diet_item_name_unique IF NOT EXISTS ON (d:DietItem) ASSERT d.food_name IS UNIQUE;

// Indexes to speed up lookup
CREATE INDEX IF NOT EXISTS FOR (f:Formulation) ON (f.name);
CREATE INDEX IF NOT EXISTS FOR (h:RegionalHerb) ON (h.name);
CREATE INDEX IF NOT EXISTS FOR (d:DietItem) ON (d.food_name);
