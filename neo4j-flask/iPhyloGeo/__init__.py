# We don’t want any duplicate :Nucleotide, :Protein, :Lineage, :Location, :LocationDay, :Continent
# :User, :Input, or :Analysis nodes

from .views import app
from .models import graph

# graph.schema.create_uniqueness_constraint("User", "username")


def create_uniqueness_constraint(label, property):
    query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
    query = query.format(label=label, property=property)
    graph.cypher.execute(query)


create_uniqueness_constraint("User", "username")


# With a uniqueness constraint on the :User label by the username property, Neo4j ensures there are never :User labeled nodes that share the same username.
