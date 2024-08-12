#
# Top Level Mission Makefile
#
MISSION ?= mission_sample
OBSWBUILDDIR ?= $(CURDIR)/build

# The "prep" step requires extra options that are specified via environment variables.
# Certain special ones should be passed via cache (-D) options to CMake.
# These are only needed for the "prep" target but they are computed globally anyway.
PREP_OPTS := -DMISSION=$(MISSION)

ifneq ($(VERBOSE),)
	PREP_OPTS += --trace
endif

# The "LOCALTGTS" defines the top-level targets that are implemented in this makefile
# Any other target may also be given, in that case it will simply be passed through.
LOCALTGTS := clean prep install
OTHERTGTS := $(filter-out $(LOCALTGTS),$(MAKECMDGOALS))

# As this makefile does not build any real files, treat everything as a PHONY target
# This ensures that the rule gets executed even if a file by that name does exist
.PHONY: $(LOCALTGTS) $(OTHERTGTS)

clean:
	rm -rf ${OBSWBUILDDIR}

prep:
	mkdir -p ${OBSWBUILDDIR}
	cd ${MISSION} && cmake -B${OBSWBUILDDIR} -H. ${PREP_OPTS}

install: 
	${MAKE} prep
	cd ${OBSWBUILDDIR} && make install