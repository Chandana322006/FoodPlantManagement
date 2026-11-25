
from app.models.role import Role
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.audit_service import create_audit_log


def test_create_audit_log(db_session):
    # Create a user role
    role = Role(role_name="Admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    # Create a test user
    user = User(
        username="audit_test_user",
        email="audit_test@example.com",
        password_hash="test_hash",
        role_id=role.role_id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create an audit entry
    audit = create_audit_log(
        db=db_session,
        user_id=user.user_id,
        action="CREATE",
        entity_type="Batch",
        entity_id=101,
        details="Test batch created"
    )

    # Verify the audit entry
    saved_audit = db_session.query(AuditLog).filter(
        AuditLog.log_id == audit.log_id
    ).first()

    assert saved_audit is not None
    assert saved_audit.user_id == user.user_id
    assert saved_audit.action == "CREATE"
    assert saved_audit.entity_type == "Batch"
    assert saved_audit.entity_id == 101
    assert saved_audit.details == "Test batch created"
