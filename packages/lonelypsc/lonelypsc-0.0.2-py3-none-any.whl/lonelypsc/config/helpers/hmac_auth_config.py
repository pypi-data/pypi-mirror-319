import asyncio
import base64
import hmac
import math
import secrets
import sqlite3
import time
from typing import TYPE_CHECKING, Literal, Optional, Protocol, Tuple, Type, Union, cast

from lonelypsp.stateful.messages.confirm_configure import B2S_ConfirmConfigure
from lonelypsp.stateless.make_strong_etag import StrongEtag

from lonelypsc.config.auth_config import IncomingAuthConfig, OutgoingAuthConfig


class IncomingHmacAuthDBConfig(Protocol):
    async def setup_hmac_auth_db(self) -> None: ...
    async def teardown_hmac_auth_db(self) -> None: ...

    async def mark_token_used(
        self, /, *, token: bytes
    ) -> Literal["conflict", "ok"]: ...


class IncomingHmacAuthNoneDBConfig:
    """Does not store recent tokens and thus cannot check if they've been recently
    used. Technically, this is vulnerable to replay attacks, though the scope is
    rather limited.
    """

    async def setup_hmac_auth_db(self) -> None: ...
    async def teardown_hmac_auth_db(self) -> None: ...

    async def mark_token_used(self, /, *, token: bytes) -> Literal["conflict", "ok"]:
        return "ok"


if TYPE_CHECKING:
    _: Type[IncomingHmacAuthDBConfig] = IncomingHmacAuthNoneDBConfig


class IncomingHmacAuthSqliteDBConfig:
    """Stores recent tokens in a sqlite database, cleaning them in the background
    occassionally. On the subscriber side this is effective for preventing replay
    attacks assuming we only receive requests to our host as there is only one
    subscriber per host
    """

    def __init__(
        self,
        database: str,
        *,
        token_lifetime: int = 180,
        cleanup_batch_delay: float = 10.0,
    ) -> None:
        self.database = database
        """The database url. You can pass `:memory:` to create a SQLite database that
        exists only in memory, otherwise, this is typically the path to a sqlite file
        (usually has the `db` extension).
        """

        self.token_lifetime: int = token_lifetime
        """The minimum time in seconds before we forget about a token, must be at
        least as long as the token is accepted for this to be effective at preventing
        replay attacks.
        """

        self.cleanup_batch_delay: float = cleanup_batch_delay
        """The minimum time in seconds between cleaning up tokens that have expired"""

        self.conn: Optional[sqlite3.Connection] = None
        """The connection to the database"""

        self.cursor: Optional[sqlite3.Cursor] = None
        """The cursor that can be used iff you will be done using it before yielding
        to the event loop
        """

        self.background_task: Optional[asyncio.Task[None]] = None
        """The cleanup task that runs in the background"""

        self.cleanup_wakeup: asyncio.Event = asyncio.Event()
        """An event that is set whenever a token is created and will be waited on
        when there are no tokens in the store
        """

    async def setup_hmac_auth_db(self) -> None:
        assert self.background_task is None, "already entered, not re-entrant"
        conn = sqlite3.connect(self.database)
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS httppubsub_hmac_auth_tokens (token BLOB PRIMARY KEY, expires_at INTEGER NOT NULL) WITHOUT ROWID"
                )
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_httppubsub_hmac_auth_tokens_expires_at ON httppubsub_hmac_auth_tokens (expires_at)"
                )
                conn.commit()
                self.conn = conn
                self.cursor = cursor
                self.background_task = asyncio.create_task(self._cleanup_tokens())
            except BaseException:
                cursor.close()
                raise
        except BaseException:
            conn.close()
            raise

    async def teardown_hmac_auth_db(self) -> None:
        task = self.background_task
        conn = self.conn
        cursor = self.cursor
        self.background_task = None
        self.conn = None
        self.cursor = None
        try:
            if task is not None:
                task.cancel()
                await asyncio.wait([task])
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            finally:
                if conn is not None:
                    conn.close()

    async def mark_token_used(self, /, *, token: bytes) -> Literal["conflict", "ok"]:
        assert self.conn is not None and self.cursor is not None, "not entered"
        self.cursor.execute(
            "SELECT 1 FROM httppubsub_hmac_auth_tokens WHERE token = ?",
            (token,),
        )
        result = self.cursor.fetchone() is not None
        if not result:
            self.cursor.execute(
                "INSERT INTO httppubsub_hmac_auth_tokens (token, expires_at) VALUES (?, ?)",
                (token, math.ceil(time.time() + self.token_lifetime)),
            )
        self.conn.commit()
        if not result:
            self.cleanup_wakeup.set()
        return "conflict" if result else "ok"

    async def _cleanup_tokens(self) -> None:
        assert self.conn is not None and self.cursor is not None, "not entered"
        conn = self.conn
        cursor = self.cursor

        while True:
            now = time.time()
            cursor.execute(
                "DELETE FROM httppubsub_hmac_auth_tokens WHERE expires_at < ?",
                (math.ceil(now),),
            )
            conn.commit()

            cursor.execute(
                "SELECT expires_at FROM httppubsub_hmac_auth_tokens ORDER BY expires_at ASC LIMIT 1"
            )
            next_expires_at = cast(Optional[int], cursor.fetchone())

            if next_expires_at is None:
                self.cleanup_wakeup.clear()
                await self.cleanup_wakeup.wait()
                await asyncio.sleep(self.token_lifetime + self.cleanup_batch_delay)
                continue

            await asyncio.sleep(max(next_expires_at - now, self.cleanup_batch_delay))


class IncomingHmacAuth:
    """Verifies that the authorization header is a recently generated, not
    recently used, HMAC token. These tokens can only be generated if the
    sender knows the shared secret.

    The authorization header is formatted as follows: `X-HMAC <timestamp>:<nonce>:<token>`,
    where timestamp is integer seconds from the epoch.

    This is a secure way to verify requests even if the underlying message
    and headers are not encrypted, as the shared secret cannot be discovered
    by an attacker who can only see the messages. However, it will not do
    anything to prevent the contents of the messages from being read

    Generally, this is an appropriate defense-in-depth measure to use in
    internal networks where you cannot setup TLS. It is also effective when TLS
    is available, though token authorization will require less CPU time for both
    broadcasters and subscribers and is secure if headers are encrypted.
    """

    def __init__(
        self,
        secret: str,
        *,
        token_lifetime: float = 120,
        db_config: IncomingHmacAuthDBConfig,
    ) -> None:
        self.secret = base64.urlsafe_b64decode(secret + "==")
        """The shared secret used to generate the HMAC tokens"""
        assert len(self.secret) == 64, "secret must be 64 bytes long"
        self.token_lifetime = token_lifetime
        """How long after a token is created that we still accept it"""
        self.db_config = db_config
        """The configuration for the database"""

    async def setup_incoming_auth(self) -> None:
        await self.db_config.setup_hmac_auth_db()

    async def teardown_incoming_auth(self) -> None:
        await self.db_config.teardown_hmac_auth_db()

    def _get_token(self, authorization: Optional[str], now: float) -> Union[
        Tuple[Literal["unauthorized", "forbidden"], None],
        Tuple[Literal["found"], Tuple[int, str, bytes]],
    ]:
        if authorization is None:
            return "unauthorized", None

        if not authorization.startswith("X-HMAC "):
            return "forbidden", None

        timestamp_nonce_and_token = authorization[len("X-HMAC ") :]
        sep_index = timestamp_nonce_and_token.find(":")
        if sep_index == -1:
            return "forbidden", None

        timestamp_str = timestamp_nonce_and_token[:sep_index]
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            return "forbidden", None

        # clock drift means the time could be in the future
        if abs(now - timestamp) > self.token_lifetime:
            return "forbidden", None

        nonce_and_token = timestamp_nonce_and_token[sep_index + 1 :]
        sep_index = nonce_and_token.find(":")
        if sep_index == -1:
            return "forbidden", None

        nonce = nonce_and_token[:sep_index]

        hmac_token_str = nonce_and_token[sep_index + 1 :]
        try:
            hmac_token = base64.b64decode(hmac_token_str + "==")
        except ValueError:
            return "forbidden", None

        if len(hmac_token) != 64:
            return "forbidden", None

        return "found", (timestamp, nonce, hmac_token)

    async def _check_token(
        self, to_sign: bytes, hmac_token: bytes
    ) -> Literal["ok", "forbidden"]:
        expected_hmac = hmac.new(self.secret, to_sign, "sha512").digest()
        if not hmac.compare_digest(hmac_token, expected_hmac):
            return "forbidden"

        if await self.db_config.mark_token_used(token=hmac_token) == "conflict":
            return "forbidden"

        return "ok"

    async def is_receive_allowed(
        self,
        /,
        *,
        url: str,
        topic: bytes,
        message_sha512: bytes,
        now: float,
        authorization: Optional[str],
    ) -> Literal["ok", "unauthorized", "forbidden", "unavailable"]:
        assert len(message_sha512) == 64, "message_sha512 must be 64 bytes long"
        result = self._get_token(authorization, now)
        if result[0] != "found":
            return result[0]

        timestamp, nonce, hmac_token = result[1]
        encoded_url = url.encode("utf-8")
        encoded_timestamp = timestamp.to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")
        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_url).to_bytes(2, "big"),
                encoded_url,
                len(topic).to_bytes(2, "big"),
                topic,
                message_sha512,
            ]
        )
        return await self._check_token(to_sign, hmac_token)

    async def is_missed_allowed(
        self,
        /,
        *,
        recovery: str,
        topic: bytes,
        now: float,
        authorization: Optional[str],
    ) -> Literal["ok", "unauthorized", "forbidden", "unavailable"]:
        result = self._get_token(authorization, now)
        if result[0] != "found":
            return result[0]

        timestamp, nonce, hmac_token = result[1]
        encoded_recovery = recovery.encode("utf-8")
        encoded_timestamp = timestamp.to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_recovery).to_bytes(2, "big"),
                encoded_recovery,
                len(topic).to_bytes(2, "big"),
                topic,
            ]
        )
        return await self._check_token(to_sign, hmac_token)

    async def is_websocket_confirm_configure_allowed(
        self, /, *, message: B2S_ConfirmConfigure, now: float
    ) -> Literal["ok", "unauthorized", "forbidden", "unavailable"]:
        result = self._get_token(message.authorization, now)
        if result[0] != "found":
            return result[0]

        timestamp, nonce, hmac_token = result[1]
        encoded_timestamp = timestamp.to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(message.broadcaster_nonce).to_bytes(1, "big"),
                message.broadcaster_nonce,
            ]
        )
        return await self._check_token(to_sign, hmac_token)


class OutgoingHmacAuth:
    """Signs requests such that they can be verified by the subscriber but an
    eavesdropper cannot extract the secret.

    Specifically, the authorization header is formatted as follows:
    `X-HMAC <timestamp>:<nonce>:<token>`, where timestamp is integer seconds
    from the epoch, the nonce is to ensure uniqueness, and the token incorporates the
    relevant information and is signed with the shared secret.
    """

    def __init__(self, secret: str) -> None:
        self.secret = base64.urlsafe_b64decode(secret + "==")
        """The shared secret used to generate the HMAC tokens"""
        assert len(self.secret) == 64, "secret must be 64 bytes long"

    async def setup_outgoing_auth(self) -> None: ...
    async def teardown_outgoing_auth(self) -> None: ...

    def _make_nonce(self) -> str:
        return secrets.token_urlsafe(4)

    def _sign(self, to_sign: bytes, nonce: str, now: float) -> str:
        hmac_token = hmac.new(self.secret, to_sign, "sha512").digest()
        return (
            f"X-HMAC {int(now)}:{nonce}:{base64.b64encode(hmac_token).decode('ascii')}"
        )

    async def setup_subscribe_exact_authorization(
        self, /, *, url: str, recovery: Optional[str], exact: bytes, now: float
    ) -> Optional[str]:
        nonce = self._make_nonce()
        encoded_url = url.encode("utf-8")
        encoded_recovery = b"" if recovery is None else recovery.encode("utf-8")
        encoded_timestamp = int(now).to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_url).to_bytes(2, "big"),
                encoded_url,
                len(encoded_recovery).to_bytes(2, "big"),
                encoded_recovery,
                len(exact).to_bytes(2, "big"),
                exact,
            ]
        )
        return self._sign(to_sign, nonce, now)

    async def setup_subscribe_glob_authorization(
        self, /, *, url: str, recovery: Optional[str], glob: str, now: float
    ) -> Optional[str]:
        nonce = self._make_nonce()
        encoded_url = url.encode("utf-8")
        encoded_recovery = b"" if recovery is None else recovery.encode("utf-8")
        encoded_glob = glob.encode("utf-8")
        encoded_timestamp = int(now).to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_url).to_bytes(2, "big"),
                encoded_url,
                len(encoded_recovery).to_bytes(2, "big"),
                encoded_recovery,
                len(encoded_glob).to_bytes(2, "big"),
                encoded_glob,
            ]
        )
        return self._sign(to_sign, nonce, now)

    async def setup_notify_authorization(
        self, /, *, topic: bytes, message_sha512: bytes, now: float
    ) -> Optional[str]:
        assert len(message_sha512) == 64, "message_sha512 must be 64 bytes long"
        nonce = self._make_nonce()
        encoded_timestamp = int(now).to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(topic).to_bytes(2, "big"),
                topic,
                message_sha512,
            ]
        )
        return self._sign(to_sign, nonce, now)

    async def setup_check_subscriptions_authorization(
        self, /, *, url: str, now: float
    ) -> Optional[str]:
        nonce = self._make_nonce()
        encoded_url = url.encode("utf-8")
        encoded_timestamp = int(now).to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_url).to_bytes(2, "big"),
                encoded_url,
            ]
        )
        return self._sign(to_sign, nonce, now)

    async def setup_set_subscriptions_authorization(
        self, /, *, url: str, strong_etag: StrongEtag, now: float
    ) -> Optional[str]:
        nonce = self._make_nonce()
        encoded_url = url.encode("utf-8")
        encoded_etag = strong_etag.format.to_bytes(1, "big") + strong_etag.etag
        encoded_timestamp = int(now).to_bytes(8, "big")
        encoded_nonce = nonce.encode("utf-8")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(encoded_url).to_bytes(2, "big"),
                encoded_url,
                encoded_etag,
            ]
        )
        return self._sign(to_sign, nonce, now)

    async def setup_websocket_configure(
        self,
        /,
        *,
        subscriber_nonce: bytes,
        enable_zstd: bool,
        enable_training: bool,
        initial_dict: int,
    ) -> Optional[str]:
        nonce = self._make_nonce()
        encoded_nonce = nonce.encode("utf-8")
        encoded_timestamp = int(time.time()).to_bytes(8, "big")

        to_sign = b"".join(
            [
                encoded_timestamp,
                len(encoded_nonce).to_bytes(1, "big"),
                encoded_nonce,
                len(subscriber_nonce).to_bytes(1, "big"),
                subscriber_nonce,
                b"\1" if enable_zstd else b"\0",
                b"\1" if enable_training else b"\0",
                initial_dict.to_bytes(2, "big"),
            ]
        )
        return self._sign(to_sign, nonce, time.time())


if TYPE_CHECKING:
    __: Type[IncomingAuthConfig] = IncomingHmacAuth
    ___: Type[OutgoingAuthConfig] = OutgoingHmacAuth
