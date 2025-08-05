/* ==============================
   1️⃣ Banking Service Schema
   ============================== */
CREATE TABLE bank_customer (
    customer_id          BIGINT PRIMARY KEY,
    first_name           VARCHAR(250) NOT NULL,
    last_name            VARCHAR(250) NOT NULL,
    email                VARCHAR(100) UNIQUE NOT NULL,
    phone_number         VARCHAR(32),
    address_line1        VARCHAR(255),
    address_line2        VARCHAR(255),
    city                 VARCHAR(100),
    state                VARCHAR(100),
    postal_code          VARCHAR(20),
    country              VARCHAR(255),
    date_of_birth        DATE,
    gender               CHAR(1) CHECK (gender IN ('M','F','O')),
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE bank_account (
    account_id           BIGINT PRIMARY KEY,
    customer_id          BIGINT REFERENCES bank_customer(customer_id),
    account_type         VARCHAR(20) CHECK (account_type IN ('CHECKING','SAVINGS','LOAN')),
    balance              NUMERIC(18,2) DEFAULT 0.00,
    currency             CHAR(3) DEFAULT 'USD',
    status               VARCHAR(10) CHECK (status IN ('ACTIVE','INACTIVE','CLOSED')) DEFAULT 'ACTIVE',
    opened_at            TIMESTAMP WITH TIME ZONE DEFAULT now(),
    closed_at            TIMESTAMP WITH TIME ZONE
);

CREATE TABLE bank_transaction (
    transaction_id      BIGINT PRIMARY KEY,
    account_id          BIGINT REFERENCES bank_account(account_id),
    type                VARCHAR(20) CHECK (type IN ('DEPOSIT','WITHDRAWAL','TRANSFER')),
    amount              NUMERIC(18,2) NOT NULL,
    currency            CHAR(3) DEFAULT 'USD',
    transaction_date    TIMESTAMP WITH TIME ZONE DEFAULT now(),
    description         TEXT
);

/* ==============================
   2️⃣ E‑commerce Service Schema
   ============================== */
CREATE TABLE ecommerce_customer (
    customer_id          BIGINT PRIMARY KEY,
    first_name           VARCHAR(250) NOT NULL,
    last_name            VARCHAR(250) NOT NULL,
    email                VARCHAR(100) UNIQUE NOT NULL,
    phone_number         VARCHAR(32),
    created_at           TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE ecommerce_address (
    address_id           BIGINT PRIMARY KEY,
    customer_id          BIGINT REFERENCES ecommerce_customer(customer_id),
    address_line1        VARCHAR(255),
    address_line2        VARCHAR(255),
    city                 VARCHAR(100),
    state                VARCHAR(100),
    postal_code          VARCHAR(20),
    country              VARCHAR(250)
);

CREATE TABLE product_category (
    category_id          BIGINT PRIMARY KEY,
    name                 VARCHAR(100) NOT NULL,
    parent_category_id   BIGINT REFERENCES product_category(category_id)
);

CREATE TABLE ecommerce_product (
    product_id           BIGINT PRIMARY KEY,
    sku                  VARCHAR(30) UNIQUE NOT NULL,
    name                 VARCHAR(200) NOT NULL,
    description          TEXT,
    category_id          BIGINT REFERENCES product_category(category_id),
    price                NUMERIC(12,2) NOT NULL,
    cost_price           NUMERIC(12,2),   -- for margin calc
    weight_kg            NUMERIC(6,3),
    stock_quantity       INT DEFAULT 0,
    reorder_point        INT DEFAULT 0,
    discontinued         BOOLEAN DEFAULT FALSE
);

CREATE TABLE ecommerce_order (
    order_id             BIGINT PRIMARY KEY,
    customer_id          BIGINT REFERENCES ecommerce_customer(customer_id),
    order_date           TIMESTAMP WITH TIME ZONE DEFAULT now(),
    status               VARCHAR(20) CHECK (status IN ('PENDING','PROCESSING','SHIPPED','DELIVERED','CANCELLED')),
    shipping_address_id  BIGINT REFERENCES ecommerce_address(address_id),
    billing_address_id   BIGINT REFERENCES ecommerce_address(address_id),
    total_amount         NUMERIC(12,2) NOT NULL,
    payment_method       VARCHAR(30)
);

CREATE TABLE ecommerce_order_item (
    order_item_id        BIGINT PRIMARY KEY,
    order_id             BIGINT REFERENCES ecommerce_order(order_id),
    product_id           BIGINT REFERENCES ecommerce_product(product_id),
    quantity             INT NOT NULL CHECK (quantity > 0),
    unit_price           NUMERIC(12,2) NOT NULL,
    line_total           NUMERIC(12,2) DEFAULT NULL
);

/* ==============================
   3️⃣ Aggregated Analytics Warehouse
   ============================== */
-- Central customer dimension – merge banking & ecommerce customers
CREATE TABLE analytics_customer (
    customer_key         BIGINT PRIMARY KEY,
    first_name           VARCHAR(250),
    last_name            VARCHAR(250),
    email                VARCHAR(100) UNIQUE,
    phone_number         VARCHAR(32),
    created_at_bank      TIMESTAMP WITH TIME ZONE,
    created_at_ecom      TIMESTAMP WITH TIME ZONE
);

-- Fact table for banking transactions
CREATE TABLE analytics_fct_banking (
    transaction_key     BIGINT PRIMARY KEY,
    customer_key        BIGINT REFERENCES analytics_customer(customer_key),
    account_id          BIGINT,
    type                VARCHAR(20),
    amount              NUMERIC(18,2),
    currency            CHAR(3),
    transaction_date    DATE
);

-- Fact table for e‑commerce orders
CREATE TABLE analytics_fct_order (
    order_key           BIGINT PRIMARY KEY,
    customer_key        BIGINT REFERENCES analytics_customer(customer_key),
    order_date          DATE,
    status              VARCHAR(20),
    total_amount        NUMERIC(12,2),
    payment_method      VARCHAR(30)
);

-- Fact table for e‑commerce order items (line‑level)
CREATE TABLE analytics_fct_order_item (
    item_key            BIGINT PRIMARY KEY,
    order_key           BIGINT REFERENCES analytics_fct_order(order_key),
    product_id          BIGINT,
    category_id         BIGINT,
    quantity            INT,
    unit_price          NUMERIC(12,2),
    line_total          NUMERIC(12,2)
);

-- Marketing Campaign Fact Table
CREATE TABLE marketing_campaign (
    campaign_id          BIGINT PRIMARY KEY,
    channel              VARCHAR(250) NOT NULL,      -- e.g., 'EMAIL', 'SOCIAL', 'PPC', 'AFFILIATE'
    month                DATE NOT NULL,             -- first day of the month the spend was recorded
    spend_amount         NUMERIC(15,2) NOT NULL,     -- currency in USD (or your base currency)
    impressions          BIGINT DEFAULT 0,
    clicks               BIGINT DEFAULT 0,
    conversions          BIGINT DEFAULT 0,
    revenue_generated    NUMERIC(15,2) DEFAULT 0.00
);