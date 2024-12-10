from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import UUID, Decimal, Text, DateTime
import uuid
from datetime import datetime

class Payment(Model):
    __table_name__ = 'payment'

    id = UUID(primary_key=True, default=uuid.uuid4)
    order_id = UUID(index=True)  # Secondary index for order_id
    payment_method = Text()
    amount = Decimal()
    status = Text(index=True)  # Secondary index for status
    created_at = DateTime(default=datetime.now)
    updated_at = DateTime(default=datetime.now)
