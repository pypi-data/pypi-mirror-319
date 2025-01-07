from typing import Final

from volsite_postgres_common.db.BFn import BFn
from volsite_postgres_common.db.CFn import CFn
from volsite_postgres_common.fn.insert import insert_function

ID_PREFIX: Final = 'i'
ENUM_PREFIX: Final = 'e'


text_2_base64: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.text_2_base64} (_text TEXT) "
    f" RETURNS TEXT "
    f" AS"
    f" $$"
    f"   SELECT {BFn.encode}(_text::BYTEA, 'base64')"
    f" $$ "
    f" STRICT"
    f" LANGUAGE SQL "
    f" IMMUTABLE;")



def insert_util_fn__type(conn):
    insert_function(text_2_base64, CFn.text_2_base64, conn)