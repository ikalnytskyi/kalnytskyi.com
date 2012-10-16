#
# DESCRIPTION: Makefile for managing Pelican based blog.
#      AUTHOR: Igor Kalnitsky <igor@kalnitsky.org>
#
#   Based on Zoresvit's makefile.

PELICAN=pelican
PELICANOPTS=-v

BASEDIR=$(PWD)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/_build
SETTINGSFILE=$(BASEDIR)/settings.py

REMOTE_HOST=igor@kalnitsky.org


install_dependencies:
	pip install pelican webassets
	pip install git+https://github.com/clevercss/clevercss.git

html: clean
	@echo Generating content...
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(SETTINGSFILE) $(PELICANOPTS)
	@echo Done.

regenerate: clean
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(SETTINGSFILE) $(PELICANOPTS) -r

serve:
	@echo Starting up site serving...
	#pkill -f "python -m SimpleHTTPServer" & > /dev/null
	cd $(OUTPUTDIR) && python -m SimpleHTTPServer

deploy:
	@echo Starting deploying...
	git push origin
	ssh $(REMOTE_HOST) 'cd kalnitsky.org; ./deploy.sh'
	@echo Done

clean:
	@echo Cleaning up...
	rm -rf $(OUTPUTDIR)
	@echo Done


help:
	@echo 'Makefile for a pelican Web site                                        '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make install_dependencies        install blog dependencies          '
	@echo '   make html                        (re)generate the web site          '
	@echo '   make regenerate                  auto regeneration on files update  '
	@echo '   make serve                       (re)start developing server        '
	@echo '   make clean                       remove generated files             '
	@echo '   make help                        show this tip                      '
	@echo '                                                                       '

.PHONY: html help clean serve deploy
