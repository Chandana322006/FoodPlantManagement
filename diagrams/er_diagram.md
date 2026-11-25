
erDiagram
    ROLE ||--o{ USER : assigns
    USER ||--o{ BATCH : creates
    PRODUCT ||--o{ BATCH : produces
    PRODUCTION_LINE ||--o{ BATCH : processes
    SUPPLIER ||--o{ RAW_MATERIAL : supplies
    BATCH ||--o{ PRODUCTION_RECORD : has
    BATCH ||--o{ MATERIAL_USAGE : consumes
    BATCH ||--o{ QUALITY_TEST : undergoes
    BATCH ||--o{ APPROVAL : requires
    USER ||--o{ APPROVAL : reviews
    USER ||--o{ AUDIT_LOG : performs
    USER ||--o{ IMPORT_JOB : starts
    IMPORT_JOB ||--o{ IMPORT_ISSUE : contains

    ROLE {
        int role_id PK
        string role_name
    }

    USER {
        int user_id PK
        string username
        string password_hash
        int role_id FK
    }

    PRODUCT {
        int product_id PK
        string product_name
    }

    PRODUCTION_LINE {
        int line_id PK
        string line_name
    }

    SUPPLIER {
        int supplier_id PK
        string supplier_name
    }

    RAW_MATERIAL {
        int material_id PK
        string material_name
        int supplier_id FK
    }

    BATCH {
        int batch_id PK
        string legacy_batch_number
        date production_date
        string shift
        int product_id FK
        int line_id FK
    }

    PRODUCTION_RECORD {
        int record_id PK
        int batch_id FK
        float input_quantity
        float output_quantity
        float wastage_quantity
        float moisture_reading
    }

    MATERIAL_USAGE {
        int usage_id PK
        int batch_id FK
        int material_id FK
        float quantity_used
    }

    QUALITY_TEST {
        int test_id PK
        int batch_id FK
        date test_date
        datetime recorded_at
        string result
    }

    APPROVAL {
        int approval_id PK
        int batch_id FK
        int user_id FK
        string status
    }

    AUDIT_LOG {
        int log_id PK
        int user_id FK
        string action
        datetime timestamp
    }

    IMPORT_JOB {
        int import_id PK
        int user_id FK
        string filename
    }

    IMPORT_ISSUE {
        int issue_id PK
        int import_id FK
        int row_number
        string reason
    }
