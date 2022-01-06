XSA_PATH := ../ultra/ultra.xsa
BOARD := ZCU104

OVERLAY := $(shell basename $(XSA_PATH) | cut -d "." -f 1)

Zynq7000 := 
ZynqUltrascale := Ultra96 ZCU104 KV260
ifneq ($(filter $(BOARD),$(Zynq7000)),)
PROC = ps7_cortexa9
endif
ifneq ($(filter $(BOARD),$(ZynqUltrascale)),)
PROC = psu_cortexa53
endif
ifndef PROC
$(error Please set BOARD to one of the supported boards)
endif

all: clean help $(BOARD)/platforms/$(OVERLAY)/$(OVERLAY).xpfm

.PHONY: clean cleanall help

help:
	@echo "usage: make [target]"
	@echo
	@echo "options:"
	@echo "--------"
	@echo "all:        clean, show help message, and make the platform."
	@echo "help:       show help message."
	@echo "platform:   make the Vitis platform."
	@echo "clean:      clean Vitis platform for a given overlay."
	@echo
	@echo "arguments:"
	@echo "----------"
	@echo "XSA_PATH:   path to the xsa file"
	@echo "            e.g., /home/usr/boards/ZCU104/ultra/ultra.xsa"
	@echo "BOARD:      name of the board"
	@echo "            e.g., ZCU104, Ultra96, KV260"
	@echo
	@echo "current configuration:"
	@echo "----------------------"
	@echo "make XSA_PATH=$(XSA_PATH)"
	@echo "     BOARD=$(BOARD)"
	@echo

$(BOARD)/platforms/$(OVERLAY)/$(OVERLAY).xpfm:
	mkdir -p ./$(BOARD)/platforms
	xsct -sdx build_pfm.tcl $(XSA_PATH) $(OVERLAY) $(BOARD) $(PROC)
	rm -rf ./$(BOARD)/platforms/$(OVERLAY)
	cp -rf ./$(BOARD)/output/$(OVERLAY)/export/$(OVERLAY) \
	$(BOARD)/platforms/$(OVERLAY)
	@echo "Successfully finished building vitis platform."
	@echo "Vitis platform stored in $(BOARD)/platforms/$(OVERLAY)."

clean:
	rm -rf ./*/output

cleanall: clean
	rm -rf ./*/platforms

