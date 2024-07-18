from pydantic import BaseModel

# Schema for extracting e-commerce related information
digital_marketplace_blueprint = {
    "properties": {
        "product_name": {"type": "string"},
        "product_cost": {"type": "number"},
        "additional_details": {"type": "string"},
    },
    "required": ["product_name", "product_cost", "additional_details"],
}


class NewsPortalSchema(BaseModel):
    headline: str
    brief_summary: str
