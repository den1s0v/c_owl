# jenaClient.py


from jena.jenaService import JenaReasoner
# from jenaService.ttypes import RDF_Graph

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# make special exception type
class ThriftConnectionException(RuntimeError):
    pass

# ThriftConnectionException = Thrift.TException


def handle_thrift_exception(tx):
    print('Thrift error: %s' % tx.message)
    # raise


class JenaClient:
    def __init__(self, host='localhost', port=20299):
        try:
            # Make socket
            self.transport = TSocket.TSocket(host, port)

            # Buffering is critical. Raw sockets are very slow
            self.transport = TTransport.TBufferedTransport(self.transport)

            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

            # Create a client to use the protocol encoder
            self.client = JenaReasoner.Client(protocol)

            # Connect!
            self.transport.open()

        except Thrift.TException as tx:
            handle_thrift_exception(tx)

    def reconnect(self):
        try:
            self.transport.close()
            self.transport.open()
        except Thrift.TException as tx:
            handle_thrift_exception(tx)

    def ping(self):
        try:
            print('ping() ...', end=' ')
            active = self.client.ping()
            assert active
            print('OK.')
        except Thrift.TException as tx:
            handle_thrift_exception(tx)


    def runReasoner(self, rdfData:bytes, rulePaths:str, _retry_count=0) -> bytes:
        try:
            # Send data ...
            print('runReasoner(%d bytes of binary data) ...' % len(rdfData))
            resultBytes = self.client.runReasoner(rdfData, rulePaths)
            print('Received %d bytes' % len(resultBytes))
            return resultBytes

        except TTransport.TTransportException as tx:
            if _retry_count >= 3:
                # stop trying
                print(f"Trift connection: cannot reconnect after {_retry_count} times!")
                raise ThriftConnectionException(tx.message)
            try:
                print("Trift connection: trying to reconnect ...")
                self.reconnect()
                # run again
                return self.runReasoner(rdfData, rulePaths, _retry_count=_retry_count+1)
            except Thrift.TException as tx:
                handle_thrift_exception(tx)
        except Thrift.TException as tx:
            handle_thrift_exception(tx)

        # result = self.client.ping()
        # print('ping():', result)


    def stop(self):
        try:
            self.client.stop()  # interrupt the server listening

            # Close!
            self.transport.close()

        except Thrift.TException as tx:
            handle_thrift_exception(tx)


# if __name__ == '__main__':
#     try:
#         main()
#     except Thrift.TException as tx:
#         print('%s' % tx.message)
