# import hashlib
# import urllib.parse
# from datetime import datetime

# VNPAY_CONFIG = {
#     "vnp_TmnCode": "2QXUI4J4",  # Mã TMN mặc định cho test
#     "vnp_HashSecret": "SECRETKEYTEST",  # Hash secret test
#     "vnp_Url": "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html",
#     "vnp_ReturnUrl": "http://localhost:8000/payment/callback"
# }


# def create_vnpay_url(request, amount: int, txn_ref: str):
#     vnp_params = {
#         "vnp_Version": "2.1.0",
#         "vnp_Command": "pay",
#         "vnp_TmnCode": VNPAY_CONFIG["vnp_TmnCode"],
#         "vnp_Amount": amount * 100,
#         "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
#         "vnp_CurrCode": "VND",
#         "vnp_IpAddr": request.client.host,
#         "vnp_Locale": "vn",
#         "vnp_OrderType": "other",
#         "vnp_ReturnUrl": VNPAY_CONFIG["vnp_ReturnUrl"],
#         "vnp_TxnRef": txn_ref
#     }

#     sorted_keys = sorted(vnp_params)
#     hash_data = '&'.join([f"{key}={vnp_params[key]}" for key in sorted_keys])
#     secure_hash = hashlib.sha256((VNPAY_CONFIG["vnp_HashSecret"] + hash_data).encode()).hexdigest()
#     vnp_params["vnp_SecureHash"] = secure_hash
#     query = urllib.parse.urlencode(vnp_params)
#     return f"{VNPAY_CONFIG['vnp_Url']}?{query}"

import hashlib
import urllib.parse
from datetime import datetime

def create_vnpay_url(order_id: str, amount: int, txn_ref: str):
    vnp_url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    vnp_return_url = "http://localhost:8000/payment/callback"
    vnp_tmn_code = "2QXUI4J4"
    vnp_hash_secret = "SECRETKEYTEST"

    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": vnp_tmn_code,
        "vnp_Amount": str(amount * 100),  # nhân 100 theo yêu cầu VNPAY
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": order_id,
        "vnp_OrderInfo": f"Thanh toan don hang {order_id}",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": vnp_return_url,
        "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
        "vnp_IpAddr": "127.0.0.1",
    }

    # Sắp xếp các key theo thứ tự tăng dần
    sorted_keys = sorted(vnp_params.keys())
    query_string = "&".join(
        [f"{key}={vnp_params[key]}" for key in sorted_keys]
    )

    # Tạo secure hash
    hash_data = "&".join(
        [f"{key}={vnp_params[key]}" for key in sorted_keys]
    )
    secure_hash = hashlib.sha256(
        (vnp_hash_secret + hash_data).encode("utf-8")
    ).hexdigest()

    # Hoàn tất URL
    payment_url = f"{vnp_url}?{query_string}&vnp_SecureHashType=SHA256&vnp_SecureHash={secure_hash}"
    return payment_url
