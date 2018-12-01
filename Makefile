all: compile deploy

.PHONY: compile
compile:
	@echo ---- Compiling to donatello.zip ----
	rm -rf donatello.zip
	zip -j donatello.zip donatello/* requirements.txt

.PHONY: runlocally
runlocally:
	docker build -t donatello .
	docker run -it --rm -u $(shell id -u) -e BINANCE_API_KEY="$(BINANCE_API_KEY)" \
	 	-e BINANCE_SECRET_KEY="$(BINANCE_SECRET_KEY)" -e GITHUB_TOKEN="$(GITHUB_TOKEN)" \
		-e GITHUB_WEBHOOK_SECRET="$(GITHUB_WEBHOOK_SECRET)" donatello

.PHONY: clean
clean:
	@echo ---- Compiling to donatello.zip ----
	rm -rf donatello.zip

.PHONY: deploy
deploy:
	@echo ---- Deploying to gcloud ----
	mkdir -p dist/
	cp requirements.txt dist/
	cp donatello/*.py dist/
	gcloud beta functions deploy DonatelloListener --runtime python37 --region=europe-west1 --memory=128MB \
	  --project="${GCLOUD_PROJECT_ID}" --entry-point=main --trigger-http --source=./dist/ \
		--set-env-vars BINANCE_API_KEY="${BINANCE_API_KEY}",BINANCE_SECRET_KEY="${BINANCE_SECRET_KEY}",\
	GITHUB_TOKEN="${GITHUB_TOKEN}",GITHUB_WEBHOOK_SECRET="${GITHUB_WEBHOOK_SECRET}"

	rm -rf dist/
