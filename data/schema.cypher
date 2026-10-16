// GIS交通路网教学知识图谱平台 V1.0
// Neo4j schema constraints and indexes.

CREATE CONSTRAINT module_id_unique IF NOT EXISTS
FOR (node:Module) REQUIRE node.module_id IS UNIQUE;

CREATE CONSTRAINT knowledge_point_id_unique IF NOT EXISTS
FOR (node:KnowledgePoint) REQUIRE node.kp_id IS UNIQUE;

CREATE CONSTRAINT tool_id_unique IF NOT EXISTS
FOR (node:Tool) REQUIRE node.tool_id IS UNIQUE;

CREATE CONSTRAINT media_id_unique IF NOT EXISTS
FOR (node:Media) REQUIRE node.media_id IS UNIQUE;

CREATE INDEX module_name_index IF NOT EXISTS
FOR (node:Module) ON (node.name);

CREATE INDEX knowledge_point_name_index IF NOT EXISTS
FOR (node:KnowledgePoint) ON (node.name);

CREATE INDEX knowledge_point_module_index IF NOT EXISTS
FOR (node:KnowledgePoint) ON (node.kp_id);
