"""
MilvusDB connector

By default, connects to an existing collection with the _default or specified
partition or creates a new one. To drop an earlier created collection,
in the code, use:

    if utility.has_collection(<collection_name>):
        utility.drop_collection(<collection_name>)
"""

import operator

from pymilvus import (
    Collection,
    CollectionSchema,
    Partition,
    SearchResult,
    connections,
    utility,
)

from lego.db.redis import RedisContext
from lego.lego_types import EmbedModel
from lego.settings import MilvusDBSettings


class MilvusDBConnector:
    """
    A Vector index that works with just one partition.

    If no partition is specified, it will use the default partition.
    """

    def __init__(
        self,
        schema: CollectionSchema,
        settings: MilvusDBSettings,
        embed_model: EmbedModel,
        cache: RedisContext,
        embedding_field: str = "embedding",
    ):
        self._check_embeddings(settings, embed_model)
        self.embedding_field = embedding_field
        self.cache = cache

        self.search_param = settings.search_param
        self.sim_threshold_to_add = settings.sim_threshold_to_add
        self._more_similar_op = settings.more_similar_op

        connections.connect(uri=settings.uri, token=settings.token)
        self.embed_model = embed_model

        self.collection = Collection(settings.collection, schema)
        self.partition = Partition(self.collection, settings.partition)
        self._create_index(settings.index_param)

    def register_item(
        self,
        key_text_pair: tuple[str, str],
        item: dict[str, str],
        embedding: list[float],
        expr: str | None = None,
    ):
        """Make an entry for adding it to a data batch."""
        key, value = key_text_pair
        safe_text = str(value).replace("'", r"\'")

        query_expr = f"{key} == '{safe_text}'"
        if expr:
            query_expr = f"{expr} && {query_expr}"

        if self.partition.query(query_expr):  # DO NOT ADD IF ALREADY PRESENT.
            ## Unfortunately, primary key can be duplicated in the current
            ## version of Milvus (2.3.6) - what will affect search results:
            ## `partition.search(..., limit=N)` will return less than N if
            ## there are duplicates in the partition (that is, it will take N,
            ## remove all duplicates among them, and return ≤ N).
            return

        if not self.similar_one(
            key_text_pair, expr, self.sim_threshold_to_add
        ):
            self.partition.insert({**item, self.embedding_field: embedding})

    def query(self, key_text_pair: tuple[str, str], expr: str):
        """Query the partition."""
        key, value = key_text_pair
        safe_text = str(value).replace("'", r"\'")
        query_expr = f"{key} == '{safe_text}'"
        if expr:
            query_expr = f"{expr} && {query_expr}"

        return self.partition.query(query_expr)

    def search(
        self,
        query_texts: list[str],
        limit: int,
        expr: str | None = None,
        output_fields: list[str] | None = None,
    ) -> SearchResult:
        """Search for similar items in the collection."""
        if not query_texts:
            return []

        if "" in query_texts:
            raise ValueError("Empty query text is not allowed.")

        return self.partition.search(
            self.embed_model(query_texts),
            anns_field=self.embedding_field,
            param=self.search_param,
            limit=limit,
            expr=expr,
            output_fields=output_fields,
        )

    def similar_one(
        self,
        query: tuple[str, str],
        expr: str | None = None,
        sim_threshold: float | None = None,
    ) -> str | None:
        """Find the most similar item in the collection."""
        if self.partition.query(query_expr):  # DO NOT ADD IF ALREADY PRESENT.
            ## Unfortunately, primary key can be duplicated in the current
            ## version of Milvus (2.3.6) - what will affect search results:
            ## `partition.search(..., limit=N)` will return less than N if
            ## there are duplicates in the partition (that is, it will take N,
            ## remove all duplicates among them, and return ≤ N).
            return

        if sim_threshold is None:
            return None

        key, value = query
        similar = self.search([value], 1, expr)
        if getattr(operator, self._more_similar_op)(
            similar[0][0].distance, sim_threshold
        ):
            if key == "id":
                return similar[0][0].id

            return similar[0][0].entity.get(key)

    def _create_index(self, index_param) -> None:
        """Create index for the collection."""
        if (
            self.collection.has_index(field_name=self.embedding_field)
            and index_param != self.collection.index().params
        ):
            self.collection.release()
            self.collection.drop_index()

        self.collection.create_index(
            field_name=self.embedding_field, index_params=index_param
        )
        self.partition.load()
        utility.wait_for_index_building_complete(self.collection.name)
        ## `collection.create_index` is async. Just in case, let's wait
        ## for it to finish before inserting or searching data.

    def _check_embeddings(
        self, settings: MilvusDBSettings, embed_model: EmbedModel
    ) -> None:
        """Check if the settings match the embedding model."""
        if settings.embed_dim != embed_model.embed_dim:
            raise ValueError(
                f"Embedding dimension mismatch: {settings.embed_dim} != "
                f"{embed_model.embed_dim}\n Declared: {settings.embed_dim}\n"
                f"Actual: {embed_model.embed_dim}"
            )
        if settings.embed_model != embed_model.model_name:
            raise ValueError(
                f"Embedding model mismatch: {settings.embed_model} != "
                f"{embed_model.model_name}"
            )
