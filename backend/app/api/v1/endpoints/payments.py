from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import stripe
from typing import Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.game import User, Payment
from app.core.config import settings

router = APIRouter()

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutRequest(BaseModel):
    payment_type: str  # "per_game" or "subscription"
    quantity: Optional[int] = 1


class CheckoutResponse(BaseModel):
    checkout_url: str


@router.post("/create-checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CreateCheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session for payments"""
    
    try:
        if request.payment_type == "per_game":
            # Pay-per-game: $1 per analysis
            line_items = [{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Monopoly Deal Analysis",
                        "description": "AI-powered game analysis"
                    },
                    "unit_amount": settings.PAY_PER_GAME_PRICE,
                },
                "quantity": request.quantity,
            }]
            
            success_url = "http://localhost:3000/dashboard?success=true"
            cancel_url = "http://localhost:3000/dashboard?canceled=true"
            
        elif request.payment_type == "subscription":
            # Monthly subscription: $15/month
            line_items = [{
                "price_data": {
                    "currency": "usd",
                    "recurring": {
                        "interval": "month",
                    },
                    "product_data": {
                        "name": "Monopoly Deal Analyzer Pro",
                        "description": "Unlimited game analyses"
                    },
                    "unit_amount": settings.MONTHLY_SUBSCRIPTION_PRICE,
                },
                "quantity": 1,
            }]
            
            success_url = "http://localhost:3000/dashboard?subscription=success"
            cancel_url = "http://localhost:3000/dashboard?subscription=canceled"
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment type"
            )
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment" if request.payment_type == "per_game" else "subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=current_user.email,
            metadata={
                "user_id": current_user.id,
                "payment_type": request.payment_type,
                "quantity": request.quantity
            }
        )
        
        return CheckoutResponse(checkout_url=checkout_session.url)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events"""
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_completed(session, db)
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        await handle_subscription_payment(invoice, db)
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_cancelled(subscription, db)
    
    return {"status": "success"}


async def handle_checkout_completed(session: dict, db: Session):
    """Handle completed checkout session"""
    
    user_id = session["metadata"]["user_id"]
    payment_type = session["metadata"]["payment_type"]
    quantity = int(session["metadata"]["quantity"])
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    # Record payment
    payment = Payment(
        user_id=user_id,
        stripe_payment_intent_id=session["payment_intent"],
        amount=session["amount_total"],
        currency=session["currency"],
        status="succeeded",
        payment_type=payment_type
    )
    db.add(payment)
    
    # Update user based on payment type
    if payment_type == "per_game":
        user.credits += quantity
    elif payment_type == "subscription":
        user.subscription_status = "active"
    
    db.commit()


async def handle_subscription_payment(invoice: dict, db: Session):
    """Handle successful subscription payment"""
    
    customer_id = invoice["customer"]
    # You might want to store customer_id in your User model for this
    
    # For now, we'll just ensure the subscription is active
    # In production, you'd want to look up the user by Stripe customer ID
    pass


async def handle_subscription_cancelled(subscription: dict, db: Session):
    """Handle cancelled subscription"""
    
    customer_id = subscription["customer"]
    # Update user subscription status to inactive
    # In production, you'd want to look up the user by Stripe customer ID
    pass


@router.get("/credits")
async def get_user_credits(current_user: User = Depends(get_current_user)):
    """Get current user's credit balance and subscription status"""
    
    return {
        "credits": current_user.credits,
        "subscription_status": current_user.subscription_status,
        "free_analyses_today": settings.FREE_ANALYSES_PER_DAY
    }

