from __future__ import annotations

import asyncio
import base64
import json
import time

from Crypto import Hash
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from blib import Date, HttpDate, JsonBase, Url
from collections.abc import Callable, Mapping, Sequence
from datetime import timedelta
from functools import wraps
from inspect import iscoroutinefunction
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from .enums import AlgorithmType
from .errors import SignatureFailureError
from .misc import Digest, Signature
from .request_classes import SIGNERS, VALIDATORS

if TYPE_CHECKING:
	try:
		from typing import Self

	except ImportError:
		from typing_extensions import Self


class DataHash(Protocol):
	def update(self, data: bytes) -> None: ...
	def digest(self) -> bytes: ...
	def hexdigest(self) -> str: ...


def build_signing_string(
		headers: Mapping[str, str],
		used_headers: Sequence[str] | None = None) -> tuple[bytes, Sequence[str]]:
	"""
		Create a signing string from HTTP headers

		:param headers: Key/value pair of HTTP headers
		:param used_headers: List of headers to be used in the signing string
	"""

	if used_headers is None:
		used_headers = tuple(headers)

	parsed_headers = tuple(f"{key}: {headers[key]}" for key in used_headers)
	return "\n".join(parsed_headers).encode("ascii"), used_headers


def check_private(func: Callable) -> Callable:
	"Checks if the key is a private key before running a method"

	@wraps(func)  # noqa: ANN201
	def wrapper(key: Signer, *args: Any, **kwargs: Any) -> Any:
		if not key.is_private:
			raise TypeError(f"Cannot use method '{func.__name__}' on Signer with public key")

		return func(key, *args, **kwargs)
	return wrapper


def hash_data(data: bytes | str) -> DataHash:
	if isinstance(data, str):
		data = bytes(data, encoding = "utf-8")

	return Hash.SHA256.new(data = data)


def process_headers_for_signing(
		method: str,
		host: str | None,
		path: str,
		raw_headers: Mapping[str, str],
		body: JsonBase | Mapping[str, Any] | bytes | str | None = None,
		algo: AlgorithmType = AlgorithmType.HS2019) -> dict[str, str]:

	if body is not None:
		if isinstance(body, JsonBase):
			body = body.to_json()

		elif isinstance(body, Mapping):
			body = json.dumps(body)

		if not isinstance(body, bytes):
			body = bytes(body, encoding = "utf-8")

	headers = {"(request-target)": f"{method.lower()} {path}"}
	headers.update({key.lower(): value for key, value in raw_headers.items()})

	if "date" not in headers:
		date = HttpDate.new_utc()

	else:
		date = HttpDate.parse(headers["date"])

	if algo == AlgorithmType.HS2019:
		headers.update({
			"(created)": str(date.timestamp()),
			"(expires)": str((date + timedelta(hours=6)).timestamp())
		})

	if host:
		headers["host"] = host

	if "date" not in headers:
		headers["date"] = date.to_string()

	if body is not None:
		headers.update({
			"digest": Digest.new(body).compile(),
			"content-length": str(len(body))
		})

	return headers


class Signer:
	"Used to sign or verify HTTP headers"

	_test_mode: bool = False
	__slots__: tuple[str, ...] = ("_key", "keyid")


	def __init__(self, key: str | Path | RSA.RsaKey, keyid: str) -> None:
		"""
			Create a new signer object. The key can be an ``RsaKey`` object, ``str``, or ``Path`` to
			an exported key

			:param key: RSA key to use for signing or verifying
			:param keyid: Url to a web resource which hosts the public key
		"""

		self._key: RSA.RsaKey = None # type: ignore[assignment]
		self._parse_key(key)

		self.keyid: str = keyid
		"Url to a web resource which hosts the public key"


	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(type='RSA', bits={self.bits}, keyid='{self.keyid}')"


	@classmethod
	def new(cls: type[Self], keyid: str) -> Self:
		"""
			Create a new signer with a generated ``RsaKey`` of the specified size

			:param keyid: Url to a web resource which hosts the public key
		"""

		return cls(RSA.generate(4096), keyid)


	@classmethod
	def new_from_actor(cls: type[Self], actor: dict[str, Any]) -> Self:
		"""
			Create a signer object from an ActivityPub actor dict

			:param dict actor: ActivityPub Actor object
		"""

		return cls(actor["publicKey"]["publicKeyPem"], actor["publicKey"]["id"])


	@property
	def key(self) -> RSA.RsaKey:
		"Key to use for signing or verifying"

		return self._key


	def _parse_key(self, value: RSA.RsaKey | Path | str) -> None:
		if isinstance(value, Path):
			with value.open("r") as fd:
				value = fd.read()

		if isinstance(value, str):
			if not value.startswith("-"):
				with Path(value).expanduser().resolve().open("r", encoding = "utf-8") as fd:
					value = fd.read()

			try:
				value = RSA.import_key(value)

			except ValueError:
				raise TypeError("Invalid RSA key") from None

		if not isinstance(value, RSA.RsaKey):
			raise TypeError(
				"Key must be an RsaKey, Path, or a string representation of a key"
			)

		self._key = value


	@property
	def bits(self) -> int:
		"Size of the RSA key in bits"

		return self.key.size_in_bits()


	@property
	def is_private(self) -> bool:
		"Return ``True`` if the key is private"

		return self.key.has_private()


	@property
	@check_private
	def pubkey(self) -> str:
		"Export the public key to a str"

		key_data = self.key.public_key().export_key(format="PEM")
		return key_data.decode("utf-8") if isinstance(key_data, bytes) else key_data


	def export(self, path: Path | str | None = None) -> str:
		"""
			Export the key to a str

			:param path: Path to dump the key in text form to if specified
		"""

		key_data = self.key.export_key(format = "PEM")
		key = key_data.decode("utf-8") if isinstance(key_data, bytes) else key_data

		if path:
			path = Path(path)

			with path.open("w", encoding = "utf-8") as fd:
				fd.write(key)

		return key


	@check_private
	def sign_headers(self,
					method: str,
					url: Url | str,
					body: dict[str, Any] | bytes | str | None = None,
					headers: dict[str, str] | None = None,
					algorithm: AlgorithmType = AlgorithmType.HS2019) -> dict[str, Any]:
		"""
			Generate a signature and return the headers with a "Signature" key

			Note: HS2019 is the only supported algorithm, so only use others when you absolutely
			have to

			:param method: HTTP method of the request
			:param url: URL of the request
			:param body: ActivityPub message for a POST request
			:param headers: Request headers
			:param algorithm: Type of algorithm to use for hashing the headers. HS2019 is the only
				non-deprecated algorithm.
		"""

		if not isinstance(url, Url):
			url = Url.parse(url)

		headers = process_headers_for_signing(
			method, url.hostname, url.path, headers or {}, body, algorithm
		)

		hash_bytes, used_headers = build_signing_string(headers, None)
		signed_data = PKCS1_v1_5.new(self.key).sign(hash_data(hash_bytes))
		signature = Signature(
			base64.b64encode(signed_data).decode("utf-8"),
			self.keyid,
			algorithm,
			used_headers
		)

		if algorithm == AlgorithmType.HS2019:
			signature.created = Date.parse(int(headers["(created)"]))
			signature.expires = Date.parse(int(headers["(expires)"]))

		for key in {"(request-target)", "(created)", "(expires)", "host"}:
			headers.pop(key, None)

		headers["signature"] = signature.compile()
		return headers


	@check_private
	def sign_request(self, request: Any, algorithm: AlgorithmType = AlgorithmType.HS2019) -> Any:
		"""
			Convenience function to sign a request.

			Supported frameworks:

			* `Urllib <https://docs.python.org/3/library/urllib.request.html>`_
			* `Requests <https://pypi.org/project/requests>`_

			:param request: Request object to sign
			:param algorithm: Type of algorithm to use for signing and hashing the headers. HS2019
				is the only non-deprecated algorithm.

			:raises TypeError: If the Request class is not supported
		"""

		for rtype, func in SIGNERS.items():
			if not isinstance(request, rtype):
				continue

			if iscoroutinefunction(func):
				raise TypeError(f"Signer function cannot be a coroutine: {func.__name__}")

			return func(self, request, algorithm)

		raise TypeError(f"Request from module not supported: {type(request).__module__}")


	def validate_signature(self,
						method: str,
						path: str,
						headers: Mapping[str, Any],
						body: bytes | str | None = None) -> bool:
		"""
			Check to make sure the Signature and Digest headers match

			:param method: Request method
			:param path: Request path
			:param headers: Request headers
			:param body: Request body if it exists

			:raises aputils.SignatureFailureError: When any step of the validation process fails
		"""

		if not (signature := Signature.new_from_headers(headers)):
			raise SignatureFailureError("Missing 'signature' header")

		headers = {key.lower(): value for key, value in headers.items()}

		for key in signature.headers:
			if not key.startswith("(") and key not in headers:
				raise SignatureFailureError(f"Header key does not exist: {key}")

		headers["(request-target)"] = f"{method.lower()} {path}"

		if signature.created is not None:
			if not self._test_mode and signature.created > Date.new_utc():
				raise SignatureFailureError("Signature creation date is in the future")

			headers["(created)"] = str(signature.created.timestamp())

		if signature.expires is not None:
			if not self._test_mode and signature.expires < Date.new_utc():
				raise SignatureFailureError("Signature has expired")

			headers["(expires)"] = str(signature.expires.timestamp())

		if (digest := Digest.parse(headers.get("digest"))) is not None:
			if body is None:
				raise SignatureFailureError("A digest was added with an empty body")

			if not digest.validate(body):
				raise SignatureFailureError("Body digest does not match")

		sig_hash, _ = build_signing_string(headers, signature.headers)

		return PKCS1_v1_5.new(self.key).verify(
			hash_data(sig_hash),
			base64.b64decode(signature.signature)
		)


	def validate_request(self, request: Any) -> bool:
		"""
			Validate the signature of a server request object.

			Supported frameworks:

			* `AioHTTP <https://pypi.org/project/aiohttp>`_
			* `Flask <https://pypi.org/project/Flask>`_
			* `Sanic <https://pypi.org/project/sanic>`_

			:param request: Server request to validate
		"""

		for rtype, func in VALIDATORS.items():
			if not isinstance(request, rtype):
				continue

			if not iscoroutinefunction(func):
				return func(self, request)

			task = asyncio.create_task(func(self, request))
			elapsed = 0.0

			while not task.done():
				time.sleep(0.1)
				elapsed += 0.1

				if elapsed >= 5.0:
					task.cancel()
					raise TimeoutError(f"Validator function took too long: {func.__name__}")

			return task.result()

		raise TypeError(f"Unsupported request type: {type(request).__name__}")


	async def validate_request_async(self, request: Any) -> bool:
		"""
			Validate the signature of a server request object. Uses async when possible.

			:param request: Server request to validate
		"""

		for rtype, func in VALIDATORS.items():
			if not isinstance(request, rtype):
				continue

			if not iscoroutinefunction(func):
				return func(self, request)

			return await func(self, request)

		raise TypeError(f"Unsupported request type: {type(request).__name__}")
