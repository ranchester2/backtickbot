while :
do
	rm -r backtickbot-venv
	source backtickbot-venv/bin/activate
	touch runtime/optout.json
	touch runtime/responses.json
	pip3 install -r requirements.txt
	python3 backtickbot.py
done
