build:
	docker build -t train-navi .

run:
	docker run --rm -p 5050:5050 train-navi

run-dev:
	docker run --rm -it -v $(PWD):/app -p 5050:5050 train-navi

install:
	pip install -r requirements.txt

run-local:
	python -m app

clean:
	docker rmi train-navi || true
