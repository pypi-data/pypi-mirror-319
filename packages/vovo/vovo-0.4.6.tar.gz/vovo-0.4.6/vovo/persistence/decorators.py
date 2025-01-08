from functools import wraps

from sqlmodel.ext.asyncio.session import AsyncSession


def transactional(f: Callable):
    """定义事务装饰器"""

    @wraps(f)
    def wrapper(*args, db: AsyncSession, **kwargs):
        try:
            # 调用被装饰的函数
            result = f(*args, db=db, **kwargs)
            # 提交事务
            db.commit()
            return result
        except Exception as e:
            # 回滚事务
            db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred during the transaction") from e

    return wrapper
