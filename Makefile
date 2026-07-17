PYTHON ?= python3
SKILL_DIR := skills/x-insight-cards

.PHONY: demo test validate privacy-check check

demo:
	$(PYTHON) $(SKILL_DIR)/scripts/render_card.py --input examples/demo-post.json --output examples/demo-card.png

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) tests/validate_skill.py $(SKILL_DIR)

privacy-check:
	$(PYTHON) tests/privacy_check.py .

check: test validate privacy-check demo
