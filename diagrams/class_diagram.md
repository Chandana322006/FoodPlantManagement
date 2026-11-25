
classDiagram
    class User {
        +int user_id
        +str username
        +str password_hash
        +str role
        +login()
        +logout()
    }

    class Product {
        +int product_id
        +str product_name
        +create_product()
        +update_product()
    }

    class ProductionLine {
        +int line_id
        +str line_name
        +update_line()
    }

    class Supplier {
        +int supplier_id
        +str supplier_name
        +str contact
    }

    class RawMaterial {
        +int material_id
        +str material_name
        +float quantity
    }

    class Batch {
        +int batch_id
        +str legacy_batch_number
        +date production_date
        +str shift
        +str status
        +create_batch()
        +update_status()
    }

    class ProductionRecord {
        +int record_id
        +float input_quantity
        +float output_quantity
        +float wastage_quantity
        +float moisture_reading
        +calculate_yield()
        +calculate_wastage()
    }

    class QualityTest {
        +int test_id
        +date test_date
        +datetime recorded_at
        +str result
        +check_quality()
    }

    class Approval {
        +int approval_id
        +str status
        +str comments
        +approve()
        +reject()
    }

    class AuditLog {
        +int log_id
        +str action
        +datetime timestamp
        +record_change()
    }

    class ImportService {
        +import_data()
        +validate_row()
        +generate_validation_report()
    }

    class ReportService {
        +generate_yield_report()
        +generate_wastage_report()
        +generate_quality_report()
        +export_csv()
        +export_pdf()
    }

    User --> Batch : creates
    Product --> Batch : produces
    ProductionLine --> Batch : processes
    Batch --> ProductionRecord : has
    Batch --> QualityTest : undergoes
    Batch --> Approval : requires
    User --> Approval : reviews
    User --> AuditLog : performs
    Supplier --> RawMaterial : supplies
    ImportService --> Batch : imports
    ReportService --> ProductionRecord : analyzes
    ReportService --> QualityTest : analyzes
