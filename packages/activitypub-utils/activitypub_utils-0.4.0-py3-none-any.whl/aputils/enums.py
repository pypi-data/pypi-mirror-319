from __future__ import annotations

from blib import StrEnum
from collections.abc import Callable
from typing import Any, Generic, TypeVar


T = TypeVar("T")
V = TypeVar("V")


class classproperty(Generic[T, V]):
	def __init__(self, func: Callable[[type[T]], V]) -> None:
		self.func: Callable[[type[T]], V] = getattr(func, "__wrapped__", func)


	def __get__(self, obj: Any, cls: type[T]) -> V:
		return self.func(cls)


class AlgorithmType(StrEnum):
	"Algorithm type"

	RSASHA256 = "rsa-sha256"
	"Old signing standard"

	HS2019 = "hs2019"
	"Current signing standard"


class NodeinfoProtocol(StrEnum):
	"Protocols for nodeinfo"

	ACTIVITYPUB = "activitypub"
	BUDDYCLOUD = "buddycloud"
	DFRN = "dfrn"
	DIASPORA = "diaspora"
	LIBERTREE = "libertree"
	OSTATUS = "ostatus"
	PUMPIO = "pumpio"
	TENT = "tent"
	XMPP = "xmpp"
	ZOT = "zot"


class NodeinfoServiceInbound(StrEnum):
	"Nodeinfo inbound services"

	ATOM = "atom1.0"
	GNUSOCIAL = "gnusocial"
	IMAP = "imap"
	PNUT = "pnut"
	POP3 = "pop3"
	PUMPIO = "pumpio"
	RSS = "rss2.0"
	TWITTER = "twitter"


class NodeinfoServiceOutbound(StrEnum):
	"Nodeinfo outbound services"

	ATOM = "atom1.0"
	BLOGGER = "blogger"
	BUDDYCLOUD = "buddycloud"
	DIASPORA = "diaspora"
	DREAMWIDTH = "dreamwidth"
	DRUPAL = "drupal"
	FACEBOOK = "facebook"
	FRIENDICA = "friendica"
	GNUSOCIAL = "gnusocial"
	GOOGLE = "google"
	INSANEJOURNAL = "insanejournal"
	LIBERTREE = "libertree"
	LINKEDIN = "linkedin"
	LIVEJOURNAL = "livejournal"
	MEDIAGOBLIN = "mediagoblin"
	MYSPACE = "myspace"
	PINTEREST = "pinterest"
	PNUT = "pnut"
	POSTEROUS = "posterous"
	PUMPIO = "pumpio"
	REDMATRIX = "redmatrix"
	RSS = "rss2.0"
	SMTP = "smtp"
	TENT = "tent"
	TUMBLR = "tumblr"
	TWITTER = "twitter"
	WORDPRESS = "wordpress"
	XMPP = "xmpp"


class NodeinfoVersion(StrEnum):
	"Namespace URLs for the different Nodeinfo versions"

	V20 = "http://nodeinfo.diaspora.software/ns/schema/2.0"
	V21 = "http://nodeinfo.diaspora.software/ns/schema/2.1"


class ObjectType(StrEnum):
	"ActivityPub object types"

	ACCEPT = "Accept"
	ADD = "Add"
	ANNOUNCE = "Announce"
	APPLICATION = "Application"
	ARRIVE = "Arrive"
	ARTICLE = "Article"
	AUDIO = "Audio"
	BLOCK = "Block"
	COLLECTION = "Collection"
	COLLECTION_PAGE = "CollectionPage"
	CREATE = "Create"
	DELETE = "Delete"
	DISLIKE = "Dislike"
	DOCUMENT = "Document"
	EMOJI = "Emoji"
	EVENT = "Event"
	FLAG = "Flag"
	FOLLOW = "Follow"
	GROUP = "Group"
	IGNORE = "Ignore"
	IMAGE = "Image"
	INVITE = "Invite"
	JOIN = "Join"
	LEAVE = "Leave"
	LIKE = "Like"
	LISTEN = "Listen"
	MOVE = "Move"
	NOTE = "Note"
	OBJECT = "Object"
	OFFER = "Offer"
	ORDERED_COLLECTION = "OrderedCollection"
	ORDERED_COLLECTION_PAGE = "OrderedCollectionPage"
	ORGANIZATION = "Organization"
	PAGE = "Page"
	PERSON = "Person"
	PLACE = "Place"
	PROFILE = "Profile"
	QUESTION = "Question"
	REJECT = "Reject"
	READ = "Read"
	RELATIONSHIP = "Relationship"
	REMOVE = "Remove"
	SERVICE = "Service"
	TENTATIVE_ACCEPT = "TentativeAccept"
	TENTATIVE_REJECT = "TentativeReject"
	TOMBSTONE = "Tombstone"
	TRAVEL = "Travel"
	UNDO = "Undo"
	UPDATE = "Update"
	VIDEO = "Video"
	VIEW = "View"


	@classproperty
	@classmethod
	def Activity(cls: type[ObjectType]) -> tuple[ObjectType, ...]:
		return (
			cls.ACCEPT,
			cls.ADD,
			cls.ANNOUNCE,
			cls.ARRIVE,
			cls.BLOCK,
			cls.CREATE,
			cls.DELETE,
			cls.DISLIKE,
			cls.FLAG,
			cls.FOLLOW,
			cls.IGNORE,
			cls.INVITE,
			cls.JOIN,
			cls.LEAVE,
			cls.LIKE,
			cls.LISTEN,
			cls.MOVE,
			cls.OFFER,
			cls.QUESTION,
			cls.REJECT,
			cls.READ,
			cls.REMOVE,
			cls.TENTATIVE_ACCEPT,
			cls.TENTATIVE_REJECT,
			cls.TRAVEL,
			cls.UNDO,
			cls.UPDATE,
			cls.VIEW
		)


	@classproperty
	@classmethod
	def Actor(cls: type[ObjectType]) -> tuple[ObjectType, ...]:
		return (
			cls.APPLICATION,
			cls.GROUP,
			cls.ORGANIZATION,
			cls.PERSON,
			cls.SERVICE
		)


	@classproperty
	@classmethod
	def Collection(cls: type[ObjectType]) -> tuple[ObjectType, ...]:
		return (
			cls.COLLECTION,
			cls.COLLECTION_PAGE,
			cls.ORDERED_COLLECTION,
			cls.ORDERED_COLLECTION_PAGE
		)


	@classproperty
	@classmethod
	def Media(cls: type[ObjectType]) -> tuple[ObjectType, ...]:
		return (
			cls.AUDIO,
			cls.EMOJI,
			cls.IMAGE,
			cls.VIDEO
		)


	@classproperty
	@classmethod
	def Object(cls: type[ObjectType]) -> tuple[ObjectType, ...]:
		return (
			cls.APPLICATION,
			cls.ARTICLE,
			cls.AUDIO,
			cls.COLLECTION,
			cls.COLLECTION_PAGE,
			cls.DOCUMENT,
			cls.EMOJI,
			cls.EVENT,
			cls.GROUP,
			cls.IMAGE,
			cls.NOTE,
			cls.OBJECT,
			cls.ORGANIZATION,
			cls.ORDERED_COLLECTION,
			cls.ORDERED_COLLECTION_PAGE,
			cls.PAGE,
			cls.PERSON,
			cls.PLACE,
			cls.PROFILE,
			cls.RELATIONSHIP,
			cls.SERVICE,
			cls.TOMBSTONE,
			cls.VIDEO
		)


class SignatureAlgorithm(StrEnum):
	"Algorithm specified in the ``algorithm`` field in the signature"

	HS2019 = "hs2019"
	RSA_SHA1 = "rsa-sha1"
	RSA_SHA256 = "rsa-sha256"
	ECDSA_SHA256 = "ecdsa-sha256"
