while :
do
	deactivate
	git checkout master
	git pull
	rm -r backtickbot-venv
	python3 -m venv backtickbot-venv
	source backtickbot-venv/bin/activate
	touch runtime/optout.json
	touch runtime/responses.json
	pip3 install -r requirements.txt
	python3 backtickbot.py
done
