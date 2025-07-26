import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.policies import DCAwareRoundRobinPolicy
import logging

logger = logging.getLogger(__name__)

class DataStaxConnection:
    def __init__(self):
        self.cluster = None
        self.session = None
        self._connected = False

    def connect(self):
        """ Connect to DataStax Astra DB """
        try:
            cloud_config = {
                'secure_connect_bundle': os.getenv('DATASTAX_SECURE_BUNDLE_PATH'),
            }
            if not os.getenv('DATASTAX_SECURE_BUNDLE_PATH'):
                contact_points = [os.getenv('CASSANDRA_HOST', '127.0.0.1')]
                port = int(os.getenv('CASSANDRA_PORT', 9042))
                self.cluster = Cluster(
                    contact_points=contact_points,
                    port=port,
                    load_balancing_policy=DCAwareRoundRobinPolicy()
                )
            else:
                # DataStax Astra Cloud
                auth_provider = PlainTextAuthProvider(
                    username=os.getenv('DATASTAX_CLIENT_ID'),
                    password=os.getenv('DATASTAX_CLIENT_SECRET')
                )
                self.cluster = Cluster(
                    cloud=cloud_config,
                    auth_provider=auth_provider,
                    load_balancing_policy=DCAwareRoundRobinPolicy()
                )

            self.session = self.cluster.connect()

            # Set keyspace
            keyspace = os.getenv('DATASTAX_KEYSPACE', 'whatapp_mcp')
            self.session.set_keyspace(keyspace)

            # Setup CQLEngine connection
            connection.setup(
                hosts=[os.getenv('CASSANDRA_HOST', '127.0.0.1')],
                default_keyspace=keyspace,
                port=int(os.getenv('CASSANDRA_PORT', 9042)),
            )

            self._connected = True
            logger.info(f"Connected to DataStax - Keyspace: {keyspace}")

            return self.session
        
        except Exception as e:
            logger.error(f"Failed to connect to DataStax Astra DB: {str(e)}")
            raise

    def disconnect(self):
        """ Disconnect from DataStax """
        if self.cluster:
            self.cluster.shutdown()
            self._connected = False
            logger.info("Disconnected from DataStax Astra DB")

    def is_connected(self):
        return self._connected
    
    def get_session(self):
        if not self._connected:
            return self.connect()
        return self.session
    
datastax_connection = DataStaxConnection()