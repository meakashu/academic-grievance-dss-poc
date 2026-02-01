-- Academic Grievance DSS Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grievances table
CREATE TABLE IF NOT EXISTS grievances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(50) NOT NULL,
    grievance_type VARCHAR(100) NOT NULL,
    narrative TEXT NOT NULL,
    parameters JSONB NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Decisions table
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grievance_id UUID NOT NULL REFERENCES grievances(id) ON DELETE CASCADE,
    outcome VARCHAR(50) NOT NULL, -- ACCEPT, REJECT, PARTIAL_ACCEPT, PENDING_CLARIFICATION
    applicable_rule VARCHAR(200),
    regulatory_source TEXT,
    hierarchy_level VARCHAR(50),
    salience INTEGER,
    reason TEXT NOT NULL,
    explanation TEXT,
    action_required TEXT,
    human_review_required BOOLEAN DEFAULT FALSE,
    decided_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Rule traces table
CREATE TABLE IF NOT EXISTS rule_traces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grievance_id UUID NOT NULL REFERENCES grievances(id) ON DELETE CASCADE,
    decision_id UUID REFERENCES decisions(id) ON DELETE CASCADE,
    rules_evaluated JSONB NOT NULL,
    conflicts_detected JSONB,
    final_decision JSONB NOT NULL,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ambiguity reports table
CREATE TABLE IF NOT EXISTS ambiguity_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grievance_id UUID NOT NULL REFERENCES grievances(id) ON DELETE CASCADE,
    ambiguous_terms JSONB,
    requires_human_review BOOLEAN DEFAULT FALSE,
    clarification_questions JSONB,
    llm_response JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fairness monitoring table
CREATE TABLE IF NOT EXISTS fairness_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grievance_id UUID NOT NULL REFERENCES grievances(id) ON DELETE CASCADE,
    decision_id UUID REFERENCES decisions(id) ON DELETE CASCADE,
    similar_cases JSONB,
    consistency_score DECIMAL(5,4),
    anomaly_detected BOOLEAN DEFAULT FALSE,
    demographic_parity JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Rules catalog table (for documentation)
CREATE TABLE IF NOT EXISTS rules_catalog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id VARCHAR(200) UNIQUE NOT NULL,
    rule_name VARCHAR(300) NOT NULL,
    hierarchy_level VARCHAR(50) NOT NULL,
    authority VARCHAR(300),
    source TEXT,
    source_url TEXT,
    effective_date DATE,
    expiry_date DATE,
    category VARCHAR(100),
    rule_type VARCHAR(50), -- MANDATORY, CONDITIONAL, EXCEPTION
    description TEXT,
    salience INTEGER,
    drl_file VARCHAR(200),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_grievances_student_id ON grievances(student_id);
CREATE INDEX idx_grievances_type ON grievances(grievance_type);
CREATE INDEX idx_grievances_status ON grievances(status);
CREATE INDEX idx_grievances_submitted_at ON grievances(submitted_at);

CREATE INDEX idx_decisions_grievance_id ON decisions(grievance_id);
CREATE INDEX idx_decisions_outcome ON decisions(outcome);
CREATE INDEX idx_decisions_hierarchy_level ON decisions(hierarchy_level);
CREATE INDEX idx_decisions_decided_at ON decisions(decided_at);

CREATE INDEX idx_rule_traces_grievance_id ON rule_traces(grievance_id);
CREATE INDEX idx_rule_traces_decision_id ON rule_traces(decision_id);

CREATE INDEX idx_ambiguity_grievance_id ON ambiguity_reports(grievance_id);
CREATE INDEX idx_ambiguity_requires_review ON ambiguity_reports(requires_human_review);

CREATE INDEX idx_fairness_grievance_id ON fairness_checks(grievance_id);
CREATE INDEX idx_fairness_anomaly ON fairness_checks(anomaly_detected);

CREATE INDEX idx_rules_catalog_rule_id ON rules_catalog(rule_id);
CREATE INDEX idx_rules_catalog_hierarchy ON rules_catalog(hierarchy_level);
CREATE INDEX idx_rules_catalog_active ON rules_catalog(active);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_grievances_updated_at BEFORE UPDATE ON grievances
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rules_catalog_updated_at BEFORE UPDATE ON rules_catalog
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO grievance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO grievance_user;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database schema initialized successfully!';
END $$;
