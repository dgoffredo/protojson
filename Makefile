.PHONY: all
all: README.md example/request.json

README.md: README.md.m4 example/hello.proto *.py
	m4 $< >$@

example/request.json: example/hello.proto *.py
	./tool.py $< | python3 -m json.tool  >$@
