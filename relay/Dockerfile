FROM golang:1.18-alpine as builder
WORKDIR /build
COPY . .
RUN go build -o relay cmd/main.go

FROM alpine
WORKDIR app
COPY --from=builder /build/relay /app/relay
CMD /app/relay
