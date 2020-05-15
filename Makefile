TEMPDIR := $(shell mktemp -t tmp.XXXXXX -d)
FLAKE8 := $(shell which flake8)
UNAME := $(shell uname)
DOCKERTAG = hghotra/email2pdflib

determineversion:
	$(eval GITDESCRIBE := $(shell git describe --dirty))
	sed 's/Version: .*/Version: $(GITDESCRIBE)/' debian/DEBIAN/control_template > debian/DEBIAN/control

ifeq ($(UNAME),Linux)
builddeb: determineversion builddeb_real
else
builddeb: rundocker_getdebs
endif

builddeb_real:
	sudo apt-get install build-essential
	cp -R debian/DEBIAN/ $(TEMPDIR)
	mkdir -p $(TEMPDIR)/usr/bin
	mkdir -p $(TEMPDIR)/usr/share/doc/email2pdf
	cp email2pdf $(TEMPDIR)/usr/bin
	cp README* $(TEMPDIR)/usr/share/doc/email2pdf
	cp LICENSE* $(TEMPDIR)/usr/share/doc/email2pdf
	cp getmailrc.sample $(TEMPDIR)/usr/share/doc/email2pdf
	fakeroot chmod -R u=rwX,go=rX $(TEMPDIR)
	fakeroot chmod -R u+x $(TEMPDIR)/usr/bin
	fakeroot dpkg-deb --build $(TEMPDIR) .

builddocker: determineversion
	docker build -t $(DOCKERTAG) .
	docker tag $(DOCKERTAG):latest $(DOCKERTAG):$(GITDESCRIBE)

builddocker_nocache: determineversion
	docker build --no-cache -t $(DOCKERTAG) .
	docker tag $(DOCKERTAG):latest $(DOCKERTAG):$(GITDESCRIBE)

rundocker_interactive: builddocker
	docker run --rm -i -t $(DOCKERTAG) bash -l

rundocker_testing: builddocker
	docker run --rm -t $(DOCKERTAG) bash -c 'cd /tmp/email2pdf && make unittest && make stylecheck'

rundocker_getdebs: builddocker
	docker run --rm -v ${PWD}:/debs $(DOCKERTAG) sh -c 'cp /tmp/*.deb /debs'
