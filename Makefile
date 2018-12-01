all: compile

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
		-e GITHUB_WEBHOOK_SECRET="$(GITHUB_WEBHOOK_SECRET)" -p 5000:5000 donatello

.PHONY: clean
clean:
	@echo ---- Compiling to donatello.zip ----
	rm -rf donatello.zip
