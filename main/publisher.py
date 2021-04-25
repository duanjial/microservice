from google.cloud import pubsub_v1


class PubSubPublisher:
    def __init__(self, project_id):
        self.project_id = project_id

    def create_topic(self, topic_id):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, topic_id)
        topic = publisher.create_topic(request={"name": topic_path})
        print("Created topic: {}".format(topic.name))

    def publish_message(self, topic_id, message):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, topic_id)
        data = message.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(f"Published message to {topic_path}")
