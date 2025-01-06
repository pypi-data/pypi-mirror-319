from __future__ import annotations

import base64
import json

from Crypto.Hash import SHA256, SHA512
from blib import Date
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, TYPE_CHECKING

from .enums import AlgorithmType

if TYPE_CHECKING:
	try:
		from typing import Self

	except ImportError:
		from typing_extensions import Self


HASHES = {
	"sha256": SHA256,
	"sha512": SHA512
}


class Digest:
	"Represents a body digest"

	__slots__ = {"digest", "algorithm"}

	def __init__(self, digest: str, algorithm: str) -> None:
		"""
			Create a new digest object from an already existing digest

			:param digest: Base64 encoded hash
			:param algorithm: Algorithm used for hash in the format of ``{type}-{bytes}``
		"""

		self.digest = digest
		self.algorithm = algorithm


	def __repr__(self) -> str:
		return f"Digest({self.digest}, {self.algorithm})"


	def __str__(self) -> str:
		return self.compile()


	def __eq__(self, value: object) -> bool:
		if isinstance(value, Digest):
			return self.algorithm == value.algorithm and self.digest == value.digest

		if isinstance(value, (dict, str, bytes)):
			return self.validate(value)

		raise TypeError(f"Cannot compare '{type(value).__name__}' to 'Digest'")


	@classmethod
	def new(cls: type[Self],
			body: dict[str, Any] | str | bytes,
			size: int = 256) -> Self:
		"""
			Generate a new body digest

			:param body: Message body to hash
			:param size: SHA hash size
		"""

		if isinstance(body, dict):
			body = json.dumps(body).encode("utf-8")

		elif isinstance(body, str):
			body = body.encode("utf-8")

		if size >= 1024:
			size = int(size / 8)

		raw_hash = HASHES[f"sha{size}"].new(data=body)
		digest = base64.b64encode(raw_hash.digest()).decode("utf-8")

		return cls(digest, f"SHA-{size}")


	@classmethod
	def parse(cls: type[Self], digest: str | None) -> Self | None:
		"""
			Create a new digest from a digest header

			:param digest: Digest header
		"""

		if not digest:
			return None

		alg, digest = digest.split("=", 1)
		return cls(digest, alg)


	@property
	def hashalg(self) -> str:
		"Hash function used when creating the signature as a string"

		return self.algorithm.replace("-", "").lower()


	def compile(self) -> str:
		"Turn the digest object into a ``str`` for the Digest header"

		return "=".join([self.algorithm, self.digest])


	def validate(self, body: dict[str, Any] | str | bytes, hash_size: int = 256) -> bool:
		"""
			Check if the body digest matches the body

			:param body: Message body to verify
			:param hash_size: Size of the hashing algorithm
		"""

		return self == Digest.new(body, hash_size)


class MessageDate(Date):
	"""
		Datetime object with convenience methods for parsing and creating ActivityPub message date
		strings
	"""

	FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
	ALT_FORMATS = ["%Y-%m-%dT%H:%M:%S.%fZ"]


class Signature:
	"""
		Represents a signature header value
	"""

	__slots__ = {"keyid", "algorithm", "headers", "signature", "created", "expires"}

	def __init__(self,
				signature: str,
				keyid: str,
				algorithm: AlgorithmType | str,
				headers: Sequence[str] | str,
				created: Date | datetime | str | int | float | None = None,
				expires: Date | datetime | str | int | float | None = None) -> None:
		"""
			Create a new signature object. This should not be initiated directly.

			:param signature: Generated signature hash
			:param keyid: URL of the public key
			:param algorithm: Hashing and signing algorithms used to create the signature
			:param headers: Header keys used to create the signature
			:param created: Unix timestamp representing the signature creation date
			:param expires: Unix timestamp representing the date the signature expires
		"""

		self.signature: str = signature
		"Generated signature hash"

		self.keyid: str = keyid
		"URL of the public key"

		self.algorithm: AlgorithmType = AlgorithmType.parse(algorithm)
		"Hashing and signing algorithms used to create the signature"

		self.headers: Sequence[str] = headers.split() if isinstance(headers, str) else headers
		"Header keys used to create the signature"

		self.created: Date | None = None
		"Signature creation date"

		self.expires: Date | None = None
		"Signature expiration date"

		self.set_created(created)
		self.set_expires(expires)


	def __repr__(self) -> str:
		data = {
			"keyid": repr(self.keyid),
			"algorithm": self.algorithm,
			"headers": self.headers,
			"created": self.created.timestamp() if self.created is not None else None,
			"expires": self.expires.timestamp() if self.expires is not None else None
		}

		str_data = ", ".join(f"{key}={value}" for key, value in data.items())
		return f"Signature({str_data})"


	@classmethod
	def new_from_headers(cls: type[Self], headers: Mapping[str, str]) -> Self:
		"""
			Parse the signature from a header dict

			:param dict[str,str] headers: Header key/value pairs
			:raises KeyError: When the signature header(s) cannot be found
			:raises NotImplementedError: When a newer unsupported signature standard is provided
		"""

		headers = {key.lower(): value for key, value in headers.items()}

		if "signature-input" in headers:
			raise NotImplementedError("Newer signature spec not supported yet")

		signature = headers["signature"]
		data: dict[str, str] = {}

		for chunk in signature.strip().split(","):
			key, value = chunk.split("=", 1)
			data[key.lower()] = value.strip("\"")

		sig = cls(
			signature = data["signature"],
			keyid = data["keyid"],
			algorithm = data["algorithm"],
			headers = data["headers"]
		)

		sig.set_created(data.get("created"))
		sig.set_expires(data.get("expires"))

		return sig


	@classmethod
	def parse(cls: type[Self], data: str) -> Self:
		"""
			Parse a Signature in string format

			:param str data: Signature string
		"""

		return cls.new_from_headers({"signature": data})


	def _set_date(self, key: str, value:  Date | datetime | str | int | float | None) -> None:
		if value is None:
			setattr(self, key, None)
			return

		if isinstance(value, str):
			try:
				value = int(value)

			except ValueError:
				pass

		setattr(self, key, Date.parse(value))


	def set_created(self, value: Date | datetime | str | int | float | None) -> None:
		"""
			Set the ``created`` property.

			:param value: Date value to be parsed
		"""

		self._set_date("created", value)


	def set_expires(self, value: Date | datetime | str | int | float | None) -> None:
		"""
			Set the ``expires`` property.

			:param value: Date value to be parsed
		"""

		self._set_date("expires", value)


	def compile(self) -> str:
		"Generate a string for a Signature header"

		data = {
			"keyId": self.keyid,
			"algorithm": self.algorithm.value,
			"headers": " ".join(self.headers),
			"created": self.created.timestamp() if self.created is not None else None,
			"expires": self.expires.timestamp() if self.expires is not None else None,
			"signature": self.signature
		}

		return ",".join([f"{k}=\"{v}\"" for k, v in data.items() if v is not None])
