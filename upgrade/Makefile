PACKAGES = gcc9

.PHONY: all $(PACKAGES)
all: check_env $(PACKAGES)

check_env :
	bash ./check_env.sh

finish:
	@echo ""
	@echo "Upgraded PYNQ image successfully."
	@echo ""

$(PACKAGES): check_env
	@if [ ! -e $@/.success ]; then \
		echo "upgrading $@ ..." &&\
		cd $@ &&\
		bash ./install.sh &&\
		touch .success ;\
	fi

clean:
	rm -rf */.success
