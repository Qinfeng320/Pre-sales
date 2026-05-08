"""客户行为 API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import ActionCreate
from ..services.policy_service import PolicyService

router = APIRouter(prefix="/api/v1/customer-actions", tags=["客户行为"])


@router.post("", response_model=dict)
async def create_customer_action(
    action_data: ActionCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """记录客户在政策下的行为"""
    service = PolicyService(db)

    policy = await service.get_policy_by_id(action_data.policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="政策不存在")

    action = await service.create_customer_action(action_data)

    return {
        "success": True,
        "action": {
            "id": action.id,
            "policy_id": action.policy_id,
            "action_type": action.action_type,
            "created_at": action.created_at.isoformat() if action.created_at else None
        }
    }


@router.get("/policy/{policy_id}", response_model=dict)
async def get_policy_customer_actions(
    policy_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """获取政策下的客户行为"""
    service = PolicyService(db)
    actions = await service.get_policy_customer_actions(policy_id)

    return {
        "success": True,
        "total": len(actions),
        "actions": [
            {
                "customer": a.customer,
                "industry": a.industry,
                "action": a.action,
                "detail": a.detail,
                "date": a.date.isoformat() if a.date else None,
                "section": a.section
            }
            for a in actions
        ]
    }
