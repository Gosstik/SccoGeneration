# Table Configuration with Declarative:
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm
# -declarative-table
import inspect
# Data types.
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase

# Actual database schema:
# https://miro.com/app/board/uXjVKZsS6Io=/

################################################################################
# Imports.
################################################################################

# Types.
from typing import Optional

from sqlalchemy.types import TypeEngine

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# Tables.
from sqlalchemy import ForeignKey

from sqlalchemy import MetaData

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import UniqueConstraint

import dbapi

import datetime
import decimal
import uuid

from type_map import Text
from type_map import QueryId
from type_map import CustomerId
from type_map import ClientId
from type_map import ChannelId
from type_map import BlackList
from type_map import MessageGroupId
from type_map import Attitude
from type_map import OfferFile
from type_map import ServiceId
from type_map import ServiceErrorId
from type_map import ServiceRejectionId
from type_map import LogId
from type_map import MessageDatetime
from type_map import type_map

import json

################################################################################
# Setup.
################################################################################

# metadata_obj = MetaData(schema="scco_schema")
metadata_obj = MetaData()

# bigint = Annotated[int, "bigint"]


class Base(DeclarativeBase):
    # metadata = metadata_obj
    registry = registry(
        type_annotation_map=type_map,
        # type_annotation_map={
        #     # str_30: String(30),
        #     # str_50: String(50),
        #     # num_12_4: Numeric(12, 4),
        #     # num_6_2: Numeric(6, 2),
        # }
    )

################################################################################
# Models.
################################################################################


from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from crud.json_util import dict_get_or_panic


class Query(Base):
    __tablename__ = "query"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["client_id"], ["client.client_id"]),
        ForeignKeyConstraint(["customer_id"], ["customer.customer_id"]),
        # UniqueConstraint("foo"),
    )

    query_id: Mapped[QueryId] = mapped_column(autoincrement=True)
    customer_id: Mapped[CustomerId]
    client_id: Mapped[ClientId]
    channel_id: Mapped[ChannelId]
    message: Mapped[Text]
    message_group_id: Mapped[MessageGroupId]
    message_date: Mapped[MessageDatetime]

    # Relationships.
    customer: Mapped["Customer"] = relationship(
        back_populates="queries",
    )
    client: Mapped["Client"] = relationship(
        back_populates="queries"
    )
    offer: Mapped["Offer"] = relationship(
        back_populates="query"
    )

    def set_val(self, name: str, value: any):
        if name == "query_id":
            self.query_id = value
        elif name == "customer_id":
            self.customer_id = value
        elif name == "client_id":
            self.client_id = value
        elif name == "channel_id":
            self.channel_id = value
        elif name == "message":
            self.message = value
        elif name == "message_group_id":
            self.message_group_id = value
        elif name == "message_date":
            self.message_date = value
        else:
            raise AttributeError(f"Unknown attribute: name = {name}, "
                                 f"value = {value}")

    def __repr__(self) -> str:
        return (inspect.cleandoc(f"""Query(
                query_id={self.query_id!r}, 
                customer_id={self.customer_id!r},
                client_id={self.client_id!r},
                channel_id={self.channel_id!r},
                message={self.message!r},
                message_group_id={self.message_group_id!r},
                message_date={self.message_date!r},
                )"""))


class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[CustomerId] = mapped_column(primary_key=True)
    black_list: Mapped[BlackList]

    # Relationships.
    queries: Mapped["Query"] = relationship(
        back_populates="customer"
    )

    def __repr__(self) -> str:
        return (inspect.cleandoc(f"""Customer(
                customer_id={self.customer_id!r}, 
                black_list={self.black_list!r},
                )"""))


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[ClientId] = mapped_column(primary_key=True)
    attitude: Mapped[Attitude]

    # Relationships.
    queries: Mapped["Query"] = relationship(
        back_populates="client"
    )

    def __repr__(self) -> str:
        return (inspect.cleandoc(f"""Client(
                query_id={self.client_id!r}, 
                attitude={self.attitude!r},
                )"""))


class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
    )

    query_id: Mapped[QueryId]
    file: Mapped[OfferFile]

    # Relationships.
    query: Mapped["Query"] = relationship(
        back_populates="offer"
    )

    def __repr__(self) -> str:
        return (inspect.cleandoc(f"""Offer(
                query_id={self.query_id!r}, 
                file={self.file!r},
                )"""))

#############################################################################



#############################################################################


# class Service(Base):
#     __tablename__ = "service"
#
#     service_id: Mapped[ServiceIdMapType] = mapped_column(primary_key=True)
#     service_name: Mapped[TextMapType]
#
#
# class ServiceLog(Base):
#     __tablename__ = "service_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["error_id"], ["service_error.error_id"]),
#         ForeignKeyConstraint(
#             ["rejection_id"],
#             ["service_rejection.rejection_id"]
#         ),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     log_date: Mapped[datetime.date]
#     service_log_status: Mapped[ServiceLogStatus]
#     error_id: Mapped[Optional[ServiceErrorIdMapType]]
#     rejection_id: Mapped[Optional[ServiceRejectionIdMapType]]
#
#
# class ServiceError(Base):
#     __tablename__ = "service_error"
#
#     error_id: Mapped[ServiceErrorIdMapType] = mapped_column(primary_key=True)
#     error_message: Mapped[TextMapType]
#
#
# class ServiceRejection(Base):
#     __tablename__ = "service_rejection"
#     __table_args__ = (
#         PrimaryKeyConstraint("rejection_id"),
#     )
#
#     rejection_id: Mapped[ServiceRejectionIdMapType]
#     rejection_message: Mapped[TextMapType]


################################################################################

# class ServiceErrorLog(Base):
#     __tablename__ = "service_error_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["error_id"], ["service_error.error_id"]),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     error_id: Mapped[ServiceErrorIdMapType]
#     error_date: Mapped[datetime.date]


# class ServiceRejectionLog(Base):
#     __tablename__ = "service_rejection_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["rejection_id"], ["service_rejection.rejection_id"]),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     rejection_id: Mapped[ServiceRejectionIdMapType]
#     rejection_date: Mapped[datetime.date]


################################################################################
