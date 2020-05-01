PACKAGES = pynq xrt ubuntu_pkg opencv protobuf json_c dpu_clk

.PHONY: all $(PACKAGES)
all: check_env $(PACKAGES) finish

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

ubuntu_pkg : pynq xrt
opencv protobuf json_c dpu_clk: pynq xrt ubuntu_pkg
finish: $(PACKAGES)

clean:
	rm -rf */.success
