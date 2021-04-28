from google.cloud import pubsub_v1


class PubSubPublisher:
    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = None

    def create_topic(self, topic_id):
        self.topic_path = self.publisher.topic_path(self.project_id, topic_id)
        topic = self.publisher.create_topic(request={"name": self.topic_path})
        print("Created topic: {}".format(topic.name))

    def publish_message(self, message):
        def call_back(future):
            message_id = future.result()
            print(f"Published message {message_id} to {self.topic_path}")
        data = message.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        future.add_done_callback(call_back)

    def is_topic_exist(self, topic_id):
        topics = self.publisher.list_topics(request={"project": f"projects/{self.project_id}"})
        for topic in topics:
            if f"projects/{self.project_id}/topics/{topic_id}" == topic.name:
                self.topic_path = f"projects/{self.project_id}/topics/{topic_id}"
                return True
        return False
