from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_active_user
from app.models.game import User, GameAnalysis

router = APIRouter()


class UserUpdate(BaseModel):
    email: str = None


class UserStats(BaseModel):
    total_analyses: int
    favorite_strategy: str
    subscription_status: str
    credits_remaining: int


@router.get("/profile", response_model=dict)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get detailed user profile"""
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "subscription_status": current_user.subscription_status,
        "credits": current_user.credits,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None
    }


@router.put("/profile")
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    
    if user_update.email:
        # Check if email is already taken
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Profile updated successfully"}


@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user statistics and usage data"""
    
    # Get total analyses
    total_analyses = db.query(GameAnalysis).filter(
        GameAnalysis.user_id == current_user.id
    ).count()
    
    # Get favorite strategy
    strategy_counts = db.query(GameAnalysis.strategy_used).filter(
        GameAnalysis.user_id == current_user.id
    ).all()
    
    if strategy_counts:
        strategies = [s[0] for s in strategy_counts]
        favorite_strategy = max(set(strategies), key=strategies.count)
    else:
        favorite_strategy = "None"
    
    return UserStats(
        total_analyses=total_analyses,
        favorite_strategy=favorite_strategy,
        subscription_status=current_user.subscription_status,
        credits_remaining=current_user.credits
    )


@router.delete("/account")
async def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete user account and all associated data"""
    
    # Delete all analyses
    db.query(GameAnalysis).filter(
        GameAnalysis.user_id == current_user.id
    ).delete()
    
    # Delete user
    db.delete(current_user)
    db.commit()
    
    return {"message": "Account deleted successfully"}


# Admin endpoints (for future use)
@router.get("/admin/users", response_model=List[dict])
async def get_all_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    
    # Simple admin check - in production you'd want proper role-based access
    if current_user.email != "admin@example.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users = db.query(User).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "subscription_status": user.subscription_status,
            "credits": user.credits,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]

