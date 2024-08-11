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

clean:
    # Use a tab here
    rm -rf ${OBSWBUILDDIR}

prep:
    # Use a tab here
    mkdir -p ${OBSWBUILDDIR}
    # Use a tab here
    cd ${MISSION} && cmake -B${OBSWBUILDDIR} -H. ${PREP_OPTS}

install: 
    # Use a tab here
    ${MAKE} prep
    # Use a tab here
    cd ${OBSWBUILDDIR} && make install