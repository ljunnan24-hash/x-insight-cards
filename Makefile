PYTHON ?= python3
NODE ?= node
SKILL_DIR := skills/x-insight-cards

.PHONY: demo demo-gif test validate privacy-check check

demo:
	$(PYTHON) $(SKILL_DIR)/scripts/render_card.py --input examples/demo-post.json --output examples/demo-card.png

demo-gif: demo
	$(PYTHON) scripts/build-demo-gif.py

test:
	$(PYTHON) -m unittest discover -s tests -v
	$(NODE) --test $(SKILL_DIR)/scripts/wechat_ilink_delivery.test.mjs $(SKILL_DIR)/scripts/wechat_ilink_listener.test.mjs

validate:
	$(PYTHON) tests/validate_skill.py $(SKILL_DIR)

privacy-check:
	$(PYTHON) tests/privacy_check.py .

check: test validate privacy-check demo-gif
