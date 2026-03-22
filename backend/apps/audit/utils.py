from apps.audit.models import AuditLog  # type: ignore


def log_event(event_type, entity_type, entity_id, user,
               field_name=None, old_value=None, new_value=None):
    """Write an immutable audit log entry."""
    try:
        AuditLog.objects.create(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            user=user,
        )
    except Exception as e:
        # Never let audit logging break the main flow
        import logging
        logging.getLogger('plm.audit').error(f'Audit log failed: {e}')
