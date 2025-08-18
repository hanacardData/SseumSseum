import base64
import hashlib
import hmac


def verify_signature(body: str, received_signature: str, secret: str) -> bool:
    """Verify the HMAC signature of the request body."""
    hash_digest = hmac.new(
        key=secret.encode("utf-8"),
        msg=body.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    expected_signature = base64.b64encode(hash_digest).decode("utf-8")
    return hmac.compare_digest(expected_signature, received_signature)
