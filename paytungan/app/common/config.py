from typing import Dict
import os

from paytungan.app.base.constants import (
    DB_CONFIG,
    FIREBASE_PRIVATE_KEY,
    FIREBASE_PRIVATE_KEY_ID,
)

from .exceptions import BaseException


def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise BaseException(f"Config Key {key} is not configured")

    return value


def get_db_config() -> Dict[str, str]:
    db_config = get_env(DB_CONFIG)

    db_config = db_config.split("|")
    db_config = {
        "DB_HOST": db_config[0],
        "DB_USER": db_config[1],
        "DB_PASS": db_config[2],
        "DB_NAME": db_config[3],
    }

    return db_config


def get_firebase_config() -> Dict[str, str]:
    return {
        "type": "service_account",
        "project_id": "paytungan",
        "private_key_id": "f05fa6f1d225e9c89e346ec0bbff18d84dd82cd6",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxqNN13DW7EU9y\npL+i31p1kJRIfc4NYjfsjnw5NpNCTBBxtL9WxlPW5QYPYdhe75LLI8lCo8/lr6e/\nDS6nwfWiSr7L44RfmZaPYsS2Hj6n4WpsHMiVA+1ZdOiFyg4DdWoIEpyAXgD7FMcE\nR9veb61n/zn5tBnbPRByFcmKB9UmesabBQBzsApY+nrMhy/mr9kpNAVe2W/mh1Ic\nb7PnyOVKCgPxo+8msclAkZu29ND+chiuu21k8JXxY6qxWrKv+WmJgu0feTUxRcfX\nKnk3eMlCCXQriaAxNI2jsJSw3gzN1WCykSvROiggotPiYWNB+biGfPrC2CKqW6Ov\nKkqKvhv3AgMBAAECggEAA9QyT9cTlO5QzHieunvl1k9BKf0FAvTUumONFkd3uJGe\nqRvOzouEJNWB4iaKlevgVglZL759ZlT5CzXx9wZIAk2i+4Aq54SOGwc6W27mGsu1\nWT1edVCaIWKLo+vbVQQx6UOEiGbTlbIqRhqtemsdvvZD4ZsoE4CnME5CkbRULXne\nug4VOhv6zkKjRSOFqrfIXnKpgf16VBi0QjpaHjtwQj+W8/T1Y0enHj/Zix4os1eH\n+y77LOMQojyIYzRy7TTwdIA1OHKMhPtt/P1VT64r1FWlpwOJcWqvuCXFVqWWsDQP\nAS0PQpjtcaAkCHGT+Vs7NLaJ+doIYmro1wK1L/29wQKBgQDa16UEm7Fb72rTPsF7\njLJoX8nzR9qhKjPpJjspfjR6+yOYfV+U1XWE6GUuH7Wtw6SXAvQHIoNUNkjy7/Z3\nBpqAYh/ByU7MkH76VZBONWVxUi3CaWdgjtKjhGghujUj+49lBnW7G7mEiE6P23Fv\nOE2pko0IoMdLTnFuEQFl2qP3LQKBgQDP0xjngmOcSNYadsqsdDq/FWQeIp4qcVgt\nyYINIDw9nggI26IyKIc7DuVBjcuTaSjljI0NwTcXNEmbm/GKdyEloWMEtozAMchb\n2XLDUBCc65AY0/ZYMQUSXmikluooYDHTvElwIHGmCEDftlVLeH8/x1ECVYm//1NO\nPdGeHe4WMwKBgAaojQLI4eqULEHlJOnna/40++YFB6fjqtSrLx2iE2KyhXC8T84t\neHfkwj9XA6YXz8gwdNBKwogrZqjNmEgi0Uyar7CruVQMCXEAbXWTtlRuVaoWnuiX\nL919x9VO3xMLMl+2hJp+y3Q22X0TBi6GHgbMyLG8gpPN/TGGHu7Eajy5AoGBAMub\nZmfSH+MKnPBad5/TU4bH30mC4vB0EU7yf/56GWrIu9hpzZNUj4B1zHeYAt2OBmo2\ndC8In/+U05SniFH++rOSVJ9WdbkKTOBnvn7Jny0NwCQC7fNjOzPO2Lh/vjMGY2qs\nqko3DwD6Twyd5xzEle6XSK9/vDAlZqld+VLuwcZvAoGASOG93jYl8140SacNdGg6\nyHTmDbFN4QzkKGr1h/xDi0/PIXMkMz/eVBPEWYCeTsZzlke6revZV58BSaeZEZev\ntWUIny7zZIgRrNiK1fxoFsRFem0kBMDG/qLvfklfwRDlLrkRjEht+YjxZgg2yfY+\nmZTKfxurTLyguL8xNqguzsc=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-4v672@paytungan.iam.gserviceaccount.com",
        "client_id": "113476718206995380065",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4v672%40paytungan.iam.gserviceaccount.com",
    }
