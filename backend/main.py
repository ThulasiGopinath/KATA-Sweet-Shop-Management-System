# backend/main.py
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from . import models, database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

# Define the data model for creating a sweet
class SweetCreate(BaseModel):
    name: str
    price: float
    category: str
    quantity: int

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    # Add this line to update the user's is_admin status from the token payload
    user.is_admin = payload.get("is_admin", False)
    return user

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sweets")
def read_sweets(db: Session = Depends(database.get_db)):
    return db.query(models.Sweet).all()

@app.post("/add-sweet")
def add_sweet(sweet: SweetCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_sweet = models.Sweet(name=sweet.name, price=sweet.price, category=sweet.category, quantity=sweet.quantity)
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Sweet added successfully"}

@app.put("/update-sweet/{sweet_id}")
def update_sweet(sweet_id: int, sweet: SweetCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db_sweet.name = sweet.name
    db_sweet.price = sweet.price
    db_sweet.category = sweet.category
    db_sweet.quantity = sweet.quantity
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Sweet updated successfully"}

@app.post("/sweets/purchase/{sweet_id}")
def purchase_sweet(sweet_id: int, quantity: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if db_sweet.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough sweets in stock")
    
    db_sweet.quantity -= quantity
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Purchase successful", "new_quantity": db_sweet.quantity}

@app.post("/sweets/restock/{sweet_id}")
def restock_sweet(sweet_id: int, quantity: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db_sweet.quantity += quantity
    db.commit()
    db.refresh(db_sweet)
    return {"message": "Restock successful", "new_quantity": db_sweet.quantity}

@app.delete("/delete-sweet/{sweet_id}")
def delete_sweet(sweet_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet is None:
        raise HTTPException(status_code=404, detail="Sweet not found")
    db.delete(db_sweet)
    db.commit()
    return {"message": "Sweet deleted successfully"}

# backend/main.py
# ...
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # Check if the username is 'admin' to set the is_admin flag
    is_admin_user = user.username.lower() == 'admin'
    
    new_user = models.User(username=user.username, hashed_password=hashed_password, is_admin=is_admin_user)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}
# ...
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/sweets/search")
def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(database.get_db),
):
    query = db.query(models.Sweet)
    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price:
        query = query.filter(models.Sweet.price <= max_price)
    return query.all()