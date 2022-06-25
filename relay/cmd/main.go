package main

import (
	"context"
	"log"
	"os"
	"os/signal"

	relay "ocotpsrelay"
)

func main() {
	projectID := os.Getenv("PUBSUB_PROJECT_ID")
	pubsubHost := os.Getenv("PUBSUB_EMULATOR_HOST")
	topic := os.Getenv("PUBSUB_TOPIC")
	log.Printf("project: %s, host: %s, topic: %s", projectID, pubsubHost, topic)

	ctx, cancel := context.WithCancel(context.Background())
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, os.Interrupt)
		<-sig
		signal.Reset()
		cancel()
	}()

	svr := relay.NewRelay(ctx, projectID, topic)
	log.Println(svr.Run(ctx))
	cancel()
}
