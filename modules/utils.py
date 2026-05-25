"""Utility functions for data processing and serialization."""


def safe_lines(value: str | None) -> list[str]:
    """Convert multiline string to list of non-empty lines.
    
    Args:
        value: Multiline string or None
        
    Returns:
        List of stripped non-empty lines
    """
    return [line.strip() for line in (value or "").splitlines() if line.strip()]


def parse_metrics(value: str | None) -> list[dict]:
    """Parse metrics from pipe-separated format.
    
    Format: "label|value" or "label|value|suffix"
    
    Args:
        value: Pipe-separated metrics string
        
    Returns:
        List of metric dicts with label, value, and optional suffix
    """
    metrics = []
    for line in safe_lines(value):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) >= 2:
            metric = {"label": parts[0], "value": parts[1]}
            if len(parts) > 2:
                metric["suffix"] = parts[2]
            metrics.append(metric)
    return metrics


def model_to_dict(obj) -> dict:
    """Convert SQLAlchemy model instance to dict, excluding private attributes.
    
    Args:
        obj: SQLAlchemy model instance
        
    Returns:
        Dictionary of model attributes (excludes private/SA internal attributes)
    """
    return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}


def form_to_model(form_data: dict, model_instance, field_mapping: dict | None = None) -> None:
    """Apply form data to model instance.
    
    Handles type conversion for common types and validates field existence.
    
    Args:
        form_data: Dictionary of form fields to apply
        model_instance: SQLAlchemy model to update
        field_mapping: Optional dict mapping form field names to model attribute names
    """
    mapping = field_mapping or {}
    for key, value in form_data.items():
        attr_name = mapping.get(key, key)
        if hasattr(model_instance, attr_name):
            setattr(model_instance, attr_name, value)
