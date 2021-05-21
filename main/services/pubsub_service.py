from utils.publisher import PubSubPublisher


class PubSubService:
    def __init__(self, project_id):
        self.pubsub_publisher = PubSubPublisher(project_id)

    def create_topic(self, topic_id):
        self.pubsub_publisher.create_topic(topic_id)

    def publish(self, message):
        self.pubsub_publisher.publish_message(message)
