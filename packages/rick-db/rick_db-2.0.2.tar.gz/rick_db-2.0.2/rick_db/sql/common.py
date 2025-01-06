class SqlError(Exception):
    pass


class Literal:
    """
    Representation class for literal expressions

    """

    def __init__(self, literal):
        self._literal = literal

    def __str__(self):
        return self._literal


# because Literal is also a typing keyword
class L(Literal):
    pass


class Sql:
    DISTINCT = "distinct"
    COLUMNS = "columns"
    FROM = "from"
    LATERAL = "lateral"
    UNION = "union"
    WHERE = "where"
    GROUP = "group"
    HAVING = "having"
    ORDER = "order"
    LIMIT_OFFSET = "limitoffset"
    FOR_UPDATE = "forupdate"
    ANONYMOUS = "_"

    JOIN = "JOIN"
    INNER_JOIN = "INNER JOIN"
    LEFT_JOIN = "LEFT JOIN"
    RIGHT_JOIN = "RIGHT JOIN"
    FULL_JOIN = "FULL JOIN"
    CROSS_JOIN = "CROSS JOIN"
    NATURAL_JOIN = "NATURAL JOIN"
    INNER_JOIN_LATERAL = "INNER JOIN LATERAL"
    LEFT_JOIN_LATERAL = "LEFT JOIN LATERAL"
    SQL_LATERAL = "LATERAL"

    SQL_WILDCARD = "*"
    SQL_SELECT = "SELECT"
    SQL_UNION = "UNION"
    SQL_UNION_ALL = "UNION ALL"
    SQL_FROM = "FROM"
    SQL_WHERE = "WHERE"
    SQL_DISTINCT = "DISTINCT"
    SQL_GROUP_BY = "GROUP BY"
    SQL_ORDER_BY = "ORDER BY"
    SQL_HAVING = "HAVING"
    SQL_FOR_UPDATE = "FOR UPDATE"
    SQL_AND = "AND"
    SQL_AS = "AS"
    SQL_OR = "OR"
    SQL_ON = "ON"
    SQL_ASC = "ASC"
    SQL_DESC = "DESC"
    SQL_OFFSET = "OFFSET"
    SQL_LIMIT = "LIMIT"
    SQL_INSERT = "INSERT INTO"
    SQL_VALUES = "VALUES"
    SQL_RETURNING = "RETURNING"
    SQL_LIST_DELIMITER_LEFT = "("
    SQL_LIST_DELIMITER_RIGHT = ")"
    SQL_ALL = "ALL"
    SQL_DELETE = "DELETE FROM"
    SQL_CASCADE = "CASCADE"
    SQL_UPDATE = "UPDATE"
    SQL_SET = "SET"
    SQL_WITH = "WITH"
    SQL_NOT_MATERIALIZED = "NOT MATERIALIZED"
    SQL_RECURSIVE = "RECURSIVE"


class SqlStatement:
    def assemble(self) -> tuple:
        pass
