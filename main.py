from fastapi import FastAPI, HTTPException, status

from database import engine, SessionLocal
from models import Base, InventoryModel
from schemas import InventoryCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/inventories", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: InventoryCreate):

    db = SessionLocal()

    try:
        existing_inventory = (
            db.query(InventoryModel)
            .filter(
                InventoryModel.warehouse_code == inventory.warehouse_code
            )
            .first()
        )

        if existing_inventory:
            raise HTTPException(
                status_code=400,
                detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
            )

        new_inventory = InventoryModel(
            warehouse_code=inventory.warehouse_code,
            location=inventory.location
        )

        db.add(new_inventory)

        db.commit()

        db.refresh(new_inventory)

        return {
            "message": "Tạo phiếu kho vận thành công",
            "data": {
                "id": new_inventory.id,
                "warehouse_code": new_inventory.warehouse_code,
                "location": new_inventory.location
            }
        }

    finally:
        db.close()