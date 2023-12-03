
i = 1

test:
	@python generate.py testfiles/md/test$(i).md

cover:
	coverage run test.py
	coverage html

