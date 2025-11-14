"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

class Company(BaseModel):
    """
    Company profile schema
    Collection name: "company"
    """
    name: str = Field(..., description="Company name")
    tagline: Optional[str] = Field(None, description="Short tagline")
    description: Optional[str] = Field(None, description="About the company")
    mission: Optional[str] = Field(None, description="Company mission")
    vision: Optional[str] = Field(None, description="Company vision")
    website: Optional[HttpUrl] = Field(None, description="Website URL")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    address: Optional[str] = Field(None, description="Address")
    logo_url: Optional[HttpUrl] = Field(None, description="Logo URL")

class ProductApp(BaseModel):
    """
    Product apps schema
    Collection name: "productapp"
    """
    name: str = Field(..., description="Product/app name")
    short_description: Optional[str] = Field(None, description="Brief description")
    category: Optional[str] = Field(None, description="Category or type")
    pricing: Optional[str] = Field(None, description="Pricing info")
    website: Optional[HttpUrl] = Field(None, description="Product URL")

class Document(BaseModel):
    """
    Intelligent document schema
    Collection name: "document"
    """
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Raw text content of the document")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for the document")
