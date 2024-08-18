from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import NotificationReceived, NotificationOpened, SessionLocal
from models import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notifications/received/")
async def save_notification_received(
    notification_id: str, 
    title: str, 
    message: str, 
    user_id: str, 
    db: Session = Depends(get_db)
):
    db_notification = NotificationReceived(
        notification_id=notification_id,
        title=title,
        message=message,
        user_id=user_id
    )
    try:
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "Notification received saved successfully"}

@app.post("/notifications/opened/")
async def save_notification_opened(
    notification_id: str, 
    user_id: str, 
    db: Session = Depends(get_db)
):
    db_notification = NotificationOpened(
        notification_id=notification_id,
        user_id=user_id
    )
    try:
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "Notification opened saved successfully"}

# Iniciar el servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
