package ocotpsrelay

import (
	"context"
	"log"
	"net"

	"cloud.google.com/go/pubsub"
)

type RelayServer struct {
	pubsubclient  *pubsub.Client
	topic         *pubsub.Topic
	topicID       string
	collectorHost string
}

func (r *RelayServer) handleMessageUDP(ctx context.Context, m *pubsub.Message) {
	log.Print("handling message ", m.ID)
	conn, err := net.Dial("udp", r.collectorHost)
	if err != nil {
		log.Printf("could not dial %s: %s", r.collectorHost, err)
		m.Nack()
		return
	}
	_, err = conn.Write(m.Data)
	if err != nil {
		log.Print("could not send trace: ", err)
		m.Nack()
	}
	m.Ack()
}

// func (r *RelayServer) handleMessageHTTP(ctx context.Context, m *pubsub.Message) {
// }

func (r *RelayServer) Run(ctx context.Context) error {
	defer r.topic.Stop()

	sub, err := r.pubsubclient.CreateSubscription(ctx, r.topicID, pubsub.SubscriptionConfig{Topic: r.topic})
	if err != nil {
		return err
	}
	for ctx.Err() == nil {
		err = sub.Receive(ctx, r.handleMessageUDP)
		if err != nil {
			return err
		}
	}

	return nil
}

func NewRelay(ctx context.Context, projectID string, topicName string) *RelayServer {

	client, err := pubsub.NewClient(ctx, projectID)
	if err != nil {
		log.Panic(err)
	}

	topic, err := client.CreateTopic(ctx, topicName)
	if err != nil {
		log.Panic(err)
	}

	return &RelayServer{
		collectorHost: "otel:6831",
		pubsubclient:  client,
		topic:         topic,
		topicID:       topicName,
	}
}
