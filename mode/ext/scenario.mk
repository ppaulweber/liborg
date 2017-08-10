#
#   Copyright (c) 2016-2017 Philipp Paulweber
#   All rights reserved.
#
#   Developed by: Philipp Paulweber
#                 https://github.com/ppaulweber/liborg
#
#   This file is part of liborg.
#
#   liborg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   liborg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with liborg. If not, see <http://www.gnu.org/licenses/>.
#

# searches for :Scenario:*: patterns

scenarios-list: .scenarios
	@cat $^

.scenarios:
	@grep -e "Scenario:[[:alnum:]][[:alnum:]]*" -o $(SRC).org | tr ":" "-" > $@

scenarios: .scenarios
	while read line; do \
	  make $$line; \
	done < $^

Scenario-%:
	@echo $@
	PATTERN=`echo $@ | tr "-" ":"`; \
	FPATH=`echo $@ | tr "-" "\n" | tail -n 1`; \
	BEGIN=`grep -n "Scenario::BEGIN" $(SRC).org | tr ":" "\n" | head -n 1`; \
	END=`grep -n "Scenario::END" $(SRC).org | tr ":" "\n" | head -n 1`; \
	CURRENT=`grep -n "$$PATTERN" $(SRC).org | tr ":" "\n" | head -n 1`; \
	NEXT=`awk "NR>$$CURRENT" $(SRC).org | grep -n "Scenario:" | tr ":" "\n" | head -n 1`; \
	echo $$PATTERN $$BEGIN $$CURRENT $$NEXT $$END; \
	awk "NR<$$BEGIN||(NR>=$$CURRENT&&NR<($$CURRENT+$$NEXT))||NR>$$END" $(SRC).org > $$FPATH.org; \
	make ORG_ARG=$$FPATH; \
	rm -f $$FPATH.tex; \
	rm -f $$FPATH.org
