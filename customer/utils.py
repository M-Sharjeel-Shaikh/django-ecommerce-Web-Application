from datetime import datetime
from store.models import Coupon
import pytz

utc=pytz.UTC

def coupon(coupon_code):
    try:
        coupon = Coupon.objects.get(code = coupon_code)
        if coupon and coupon.expire > utc.localize(datetime.now()):
            return coupon
    except Coupon.DoesNotExist:
        return None
    except Exception as e:
        print(e)