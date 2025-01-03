from models.base_model import BaseModel


def update_return_data_with_params(params: dict, data: dict, model_instance: BaseModel):
    """Update the return data for a medical practitioner"""
    for key, value in params.items():
        update_data(key, value, data, model_instance)


def update_data(param_key: str, param_value: bool, data: dict, model_instance: BaseModel):
    """Update data dictionary based on the param"""
    if param_value:  # Only update if the parameter is True
        attribute = param_key.replace('get_', '')  # Extract the attribute name
        items = getattr(model_instance, attribute, None)
        if items is not None and isinstance(items, list):
            data[attribute] = [item.to_dict() for item in items]
        else:
            data[attribute] = items.to_dict() if items is not None else None
    else:
        attribute = param_key.replace('get_', '')
        data.pop(attribute, None)  # Safely remove the key if it exists
