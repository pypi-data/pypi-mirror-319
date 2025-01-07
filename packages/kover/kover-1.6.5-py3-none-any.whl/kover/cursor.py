from __future__ import annotations

from collections import deque
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Generic,
    TypeVar,
    Type,
    cast,
    Any,
    Union
)

from bson import Int64
from typing_extensions import Self

from .typings import xJsonT
from .schema import filter_non_null
from .session import Transaction
from .models import Collation

if TYPE_CHECKING:
    from .collection import Collection
    from .schema import Document

T = TypeVar("T")


class Cursor(Generic[T]):
    def __init__(
        self,
        filter: xJsonT,
        collection: Collection,
        cls: Optional[Type[Document]] = None,
        transaction: Optional[Transaction] = None
    ) -> None:
        self._id: Optional[Int64] = None
        self._collection = collection
        self._limit = 0
        self._filter = filter
        self._projection: Optional[xJsonT] = None
        self._sort: Optional[xJsonT] = None
        self._skip: int = 0
        self._limit: int = 0
        self._hint: Optional[Union[str, xJsonT]] = None
        self._batch_size: int = 101
        self._comment: Optional[str] = None
        self._retrieved: int = 0
        self._killed: bool = False
        self._second_iteration: bool = False
        self._docs: deque[T] = deque()
        self._cls = cls
        self._transaction = transaction
        self._collation: Optional[Collation] = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: tuple[Any]) -> None:
        await self.close()

    def sort(self, mapping: xJsonT) -> Self:
        self._sort = mapping
        return self

    def skip(self, value: int) -> Self:
        self._skip = value
        return self

    def limit(self, value: int) -> Self:
        self._limit = value
        return self

    def batch_size(self, value: int) -> Self:
        self._batch_size = value
        return self

    def projection(self, mapping: xJsonT) -> Self:
        self._projection = mapping
        return self

    def comment(self, comment: str) -> Self:
        self._comment = comment
        return self

    def hint(self, hint: Union[str, xJsonT]) -> Self:
        self._hint = hint
        return self

    def get_query(self) -> xJsonT:
        collation = self._collation.to_dict() if self._collation else None
        return filter_non_null({
            "find": self._collection.name,
            "filter": self._filter,
            "skip": self._skip,
            "limit": self._limit,
            "projection": self._projection,
            "sort": self._sort,
            "batchSize": self._batch_size,
            "comment": self._comment,
            "collation": collation,
            "hint": self._hint
        })

    def _map_docs(
        self,
        documents: List[xJsonT]
    ) -> List[T]:
        if self._cls is not None:
            documents = [
                self._cls.from_document(doc) for doc in documents
            ]  # type: ignore
        return cast(List[T], documents)

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        if self._docs:
            return self._docs.popleft()
        if self._id is None:
            query = self.get_query()
            request = await self._collection.database.command(
                query,
                transaction=self._transaction
            )
            docs = request["cursor"]["firstBatch"]
            self._retrieved += len(docs)
            self._id = request["cursor"]["id"]
            self._docs.extend(self._map_docs(docs))
        else:
            if int(self._id) == 0 or self._second_iteration:
                await self.close()
                raise StopAsyncIteration
            self._second_iteration = True
            command: xJsonT = {
                "getMore": Int64(self._id),
                "collection": self._collection.name
            }
            request = await self._collection.database.command(
                command,
                transaction=self._transaction
            )
            docs = request["cursor"]["nextBatch"]
            self._retrieved += len(docs)
            self._docs.extend(self._map_docs(docs))
        if self._docs:
            return self._docs.popleft()
        raise StopAsyncIteration

    async def close(self) -> None:
        if not self._killed:
            self._killed = True
            if self._id is not None and int(self._id) > 0 and self._limit != 0:
                command: xJsonT = {
                    "killCursors": self._collection.name, "cursors": [self._id]
                }
                await self._collection.database.command(command)
            self._docs.clear()

    async def to_list(self) -> List[T]:
        return [doc async for doc in self]
