
start-dev:
	docker compose up --build app

start:
	docker compose -f docker-compose.prod.yml up -d

build:
	docker build -t license-plate-bot . && docker save -o out/image.tar license-plate-bot