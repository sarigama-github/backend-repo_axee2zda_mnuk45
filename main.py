import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Company, ProductApp, Document

app = FastAPI(title="Dokumen Pintar API", description="AI-powered intelligent document features for company profile and product apps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "Dokumen Pintar", "message": "Welcome to Dokumen Pintar API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Models for simple responses
class CreateResponse(BaseModel):
    id: str

# Company endpoints
@app.post("/api/company", response_model=CreateResponse)
def create_company(company: Company):
    try:
        inserted_id = create_document("company", company)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company", response_model=List[Company])
def list_company():
    try:
        docs = get_documents("company")
        # Convert ObjectId and unknown fields
        return [Company(**{k: v for k, v in d.items() if k in Company.model_fields}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Product apps endpoints
@app.post("/api/products", response_model=CreateResponse)
def create_product(product: ProductApp):
    try:
        inserted_id = create_document("productapp", product)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products", response_model=List[ProductApp])
def list_products():
    try:
        docs = get_documents("productapp")
        return [ProductApp(**{k: v for k, v in d.items() if k in ProductApp.model_fields}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Documents endpoints
@app.post("/api/documents", response_model=CreateResponse)
def create_document_item(doc: Document):
    try:
        inserted_id = create_document("document", doc)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents", response_model=List[Document])
def list_documents():
    try:
        docs = get_documents("document")
        return [Document(**{k: v for k, v in d.items() if k in Document.model_fields}) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
