CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE beneficiaries (
    beneficiary_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    beneficiary_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    beneficiary_id VARCHAR(20) NOT NULL,
    amount NUMERIC(15,2) NOT NULL CHECK (amount > 0),
    device_id VARCHAR(50) NOT NULL,
    transaction_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(beneficiary_id)
);

CREATE TABLE model_predictions (
    prediction_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    ml_score NUMERIC(6,4) NOT NULL CHECK (ml_score >= 0 AND ml_score <= 1),
    rule_score NUMERIC(5,2) NOT NULL CHECK (rule_score >= 0 AND rule_score <= 100),
    risk_score NUMERIC(5,2) NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    risk_level VARCHAR(10) NOT NULL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    risk_level VARCHAR(10) NOT NULL CHECK (risk_level IN ('MEDIUM', 'HIGH')),
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN'
        CHECK (status IN ('OPEN', 'UNDER_REVIEW', 'CLOSED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50),
    details TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);