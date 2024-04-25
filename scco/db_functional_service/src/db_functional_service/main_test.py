import sys

import crud.dbapi as dbapi
from crud.models import Base

from db_functional_service.broker.host_broker import HostBroker
from db_functional_service.dispatcher import Dispatcher

################################################################################

# Requests.

from db_functional_service.data.data_preproc.filter_new_queries import (
    request_1 as fnq_request_1,
)
from db_functional_service.data.data_preproc.insert_new_queries_csv import (
    request_1 as inq_csv_request_1,
)
from db_functional_service.data.data_preproc.get_customers_lists import (
    request_1 as gcl_request_1,
)
from db_functional_service.data.data_preproc.insert_preprocessed_queries import (
    request_1 as ipq_request_1,
)
from db_functional_service.data.pdf_co_gen.insert_offers import (
    request_1 as io_request_1,
)
from db_functional_service.data.ml_co_gen.get_info_for_co_generation import (
    request_1 as gifcog_request_1,
)
from db_functional_service.data.customer_creator.insert_customer import (
    request_1 as ic_request_1,
)

################################################################################


################################################################################
from db_functional_service.data.init_db import dummy_init_db


def custom_init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()

    print("Removing old tables", flush=True)
    Base.metadata.drop_all(engine)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)

    print("Inserting dummy values", flush=True)
    dummy_init_db()


def main():
    custom_init_database()

    broker = HostBroker()
    dispatcher = Dispatcher(broker)

    # dispatcher.dispatch_function(fnq_request_1)
    # dispatcher.dispatch_function(inq_csv_request_1)
    # dispatcher.dispatch_function(gcl_request_1)
    # dispatcher.dispatch_function(ipq_request_1)
    # dispatcher.dispatch_function(io_request_1)
    # dispatcher.dispatch_function(gifcog_request_1)
    dispatcher.dispatch_function(ic_request_1)
    # # dispatcher.dispatch_function(io_request_1)

    # rmq.RmqHandle.setup_rmq(gateway_callback)
    # rmq.RmqHandle.start_consume()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)


################################################################################


# def text_query():
#     textual_sql = text(
#         "SELECT id, name, fullname FROM user_account ORDER BY id"
#         )
#     textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
#     orm_sql = select(User).from_statement(textual_sql)
#     for user_obj in session.execute(orm_sql).scalars():
#         print(user_obj)
