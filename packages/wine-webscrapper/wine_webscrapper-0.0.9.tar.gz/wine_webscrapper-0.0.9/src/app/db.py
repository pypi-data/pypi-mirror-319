from sqlalchemy import orm
import sqlalchemy as sa
from enum import StrEnum, auto


class Base(orm.MappedAsDataclass, orm.DeclarativeBase):
	pass


class WineType(StrEnum):
	RED = auto()
	WHITE = auto()
	SPARKLING = auto()
	ROSE = auto()
	DESSERT = auto()
	FORTIFIED = auto()
	

class Wines(Base):
	__tablename__ = "wines"

	wine_id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, init=False)
	title: orm.Mapped[str] = orm.mapped_column(sa.String(2**8), unique=True, nullable=False, init=True)
	price: orm.Mapped[str] = orm.mapped_column(sa.String(2**8), nullable=False, init=True)
	type: orm.Mapped[WineType] = orm.mapped_column(nullable=False, init=True)
