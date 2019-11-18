from requests import Session
from signalr import Connection


def conn_step_6(log='alert', msg='Trabalhador na pista'):
    with Session() as session:
        connection = Connection("http://localhost:5000/signalr", session)

        conn = connection.register_hub('step5')

        connection.start()

        #create error handler
        def print_error(error):
            print('error: ', error)

        #process errors
        connection.error += print_error


    with connection:
        while True:
            #post new message
            conn.server.invoke('alert', 'Trabalhador na pista.')    

            #wait a second before exit
            connection.wait(1)