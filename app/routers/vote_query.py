#===== Product Rating and review query functions =====#
#short cut for query to be able to view products alongside ratings
from ..models import ProductRating


def rating_query(db, product_id: int, current_user):
    return db.query(ProductRating).filter(
        ProductRating.product_id == product_id, ProductRating.user_id == current_user.id).first()